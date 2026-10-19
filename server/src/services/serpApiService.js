import { config } from '../config/env.js';

/**
 * Executes a search query using SerpApi (Google Search Engine)
 * @param {string} query
 * @returns {Promise<Array<{ title: string, url: string, snippet: string, date: string }>>}
 */
const searchSingleQuery = async (query) => {
  if (!config.serpApiKey || config.serpApiKey.trim() === '' || config.serpApiKey === 'your_serpapi_key_here') {
    throw new Error(
      'SERPAPI_KEY is missing or invalid in server/.env. Please configure a valid SerpApi key from https://serpapi.com.'
    );
  }

  const endpoint = new URL('https://serpapi.com/search.json');
  endpoint.searchParams.set('engine', 'google');
  endpoint.searchParams.set('q', query);
  endpoint.searchParams.set('api_key', config.serpApiKey);
  endpoint.searchParams.set('num', '5'); // Fetch top 5 per query
  endpoint.searchParams.set('hl', 'en');
  endpoint.searchParams.set('gl', 'us');

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 12000);

  try {
    const res = await fetch(endpoint.toString(), {
      signal: controller.signal,
      headers: { 'Accept': 'application/json' },
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      throw new Error(errBody.error || `SerpApi HTTP error status ${res.status}`);
    }

    const data = await res.json();

    if (data.error) {
      throw new Error(`SerpApi error: ${data.error}`);
    }

    const organic = data.organic_results || [];
    return organic.map((item) => ({
      title: item.title || 'Untitled Source',
      url: item.link || item.displayed_link || '#',
      snippet: item.snippet || item.snippet_highlighted_words?.join(' ') || '',
      date: item.date || item.publication_info?.summary || 'Date not available',
    }));
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error(`SerpApi search timed out for query: "${query}"`);
    }
    throw err;
  }
};

/**
 * Searches across multiple queries, deduplicates by URL domain and path,
 * and returns capped organic results list.
 * @param {string[]} queries - Array of search queries from Gemini Task 1
 * @param {number} maxResults - Max items to return (default 8)
 * @returns {Promise<{ evidence: Array, totalFound: number, queriesUsed: string[] }>}
 */
export const fetchEvidenceForQueries = async (queries = [], maxResults = 8) => {
  if (!Array.isArray(queries) || queries.length === 0) {
    return { evidence: [], totalFound: 0, queriesUsed: [] };
  }

  // Use up to 2 focused queries to run in parallel and save SerpApi credits
  const targetQueries = queries.slice(0, 2);
  const settled = await Promise.allSettled(targetQueries.map((q) => searchSingleQuery(q)));
  const allResults = [];
  const errors = [];

  settled.forEach((res, idx) => {
    if (res.status === 'fulfilled') {
      allResults.push(...res.value);
    } else {
      console.warn(`[SerpApi] Search failed for query "${targetQueries[idx]}":`, res.reason.message);
      errors.push({ query: targetQueries[idx], error: res.reason.message });
    }
  });

  // If all queries failed due to missing API key, throw to let the controller report clearly
  if (allResults.length === 0 && errors.length > 0 && errors[0].error.includes('SERPAPI_KEY is missing')) {
    throw new Error(errors[0].error);
  }

  // Deduplicate results by URL
  const seenUrls = new Set();
  const deduplicated = [];

  for (const item of allResults) {
    if (!item.url || item.url === '#') continue;
    // Normalize URL
    const normalizedUrl = item.url.replace(/\/$/, '').toLowerCase();
    if (!seenUrls.has(normalizedUrl)) {
      seenUrls.add(normalizedUrl);
      deduplicated.push(item);
    }
  }

  const capped = deduplicated.slice(0, maxResults);

  return {
    evidence: capped,
    totalFound: deduplicated.length,
    queriesUsed: targetQueries,
  };
};
