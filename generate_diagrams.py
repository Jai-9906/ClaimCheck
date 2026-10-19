import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background title
    ax.text(50, 96, 'CLAIMCHECK - SYSTEM ARCHITECTURE', fontsize=14, fontweight='bold', ha='center', color='#1e3a8a')
    
    # 1. Client Layer Box
    rect1 = patches.FancyBboxPatch((5, 68), 90, 24, boxstyle="round,pad=1", ec="#3b82f6", fc="#eff6ff", lw=2)
    ax.add_patch(rect1)
    ax.text(7, 88, 'PRESENTATION TIER (FRONTEND - REACT 19 + VITE)', fontsize=10, fontweight='bold', color='#1e40af')
    
    comp_boxes = [
        (8, 71, 16, 14, 'ClaimForm\nInput & Presets'),
        (26, 71, 18, 14, 'CheckingProgress\n4-Stage State Machine'),
        (46, 71, 16, 14, 'ResultCard\nVerdict & Evidence'),
        (64, 71, 15, 14, 'HistoryList\nRecent Checks'),
        (81, 71, 12, 14, 'ReportModal\nDeep Inspect')
    ]
    for x, y, w, h, text in comp_boxes:
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", ec="#93c5fd", fc="#ffffff", lw=1.5)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, fontsize=7.5, ha='center', va='center', color='#1e3a8a')

    # Arrow Down from Frontend to Backend
    ax.annotate('', xy=(50, 58), xytext=(50, 68), arrowprops=dict(arrowstyle="<->", color="#2563eb", lw=2))
    ax.text(51, 63, 'HTTP / REST (JSON) via /api Reverse Proxy', fontsize=8, color='#1e40af', fontweight='semibold')

    # 2. Application Layer Box
    rect2 = patches.FancyBboxPatch((5, 34), 90, 24, boxstyle="round,pad=1", ec="#059669", fc="#ecfdf5", lw=2)
    ax.add_patch(rect2)
    ax.text(7, 54, 'APPLICATION TIER (NODE.JS & EXPRESS REST API)', fontsize=10, fontweight='bold', color='#065f46')
    
    srv_boxes = [
        (8, 37, 24, 14, 'API Routes & Middleware\n• /api/verify | /api/history\n• Centralized Error Handler'),
        (35, 37, 28, 14, 'Controllers\n• verifyController.js\n• historyController.js\n• healthController.js'),
        (66, 37, 27, 14, 'Service Layer\n• geminiService.js\n• serpApiService.js')
    ]
    for x, y, w, h, text in srv_boxes:
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", ec="#a7f3d0", fc="#ffffff", lw=1.5)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, fontsize=7.5, ha='center', va='center', color='#065f46')

    # Arrow down-left to Database, down-right to AI/Search services
    ax.annotate('', xy=(28, 24), xytext=(28, 34), arrowprops=dict(arrowstyle="<->", color="#059669", lw=2))
    ax.text(30, 29, 'Mongoose ODM', fontsize=8, color='#047857')

    ax.annotate('', xy=(75, 24), xytext=(75, 34), arrowprops=dict(arrowstyle="<->", color="#7c3aed", lw=2))
    ax.text(77, 29, 'HTTPS SDK Calls', fontsize=8, color='#6d28d9')

    # 3. Persistence Tier Box (Left)
    rect3 = patches.FancyBboxPatch((5, 4), 42, 20, boxstyle="round,pad=1", ec="#d97706", fc="#fffbeb", lw=2)
    ax.add_patch(rect3)
    ax.text(7, 20.5, 'DATA PERSISTENCE TIER', fontsize=9.5, fontweight='bold', color='#92400e')
    ax.text(26, 11, 'Local MongoDB Community Server\n• Database: claimcheck (port 27017)\n• Collection: factchecks\n• Schema: FactCheck + embedded Sources\n• MongoDB Compass GUI Inspector',
            fontsize=7.5, ha='center', va='center', color='#78350f')

    # 4. External Intelligence Tier Box (Right)
    rect4 = patches.FancyBboxPatch((53, 4), 42, 20, boxstyle="round,pad=1", ec="#7c3aed", fc="#f5f3ff", lw=2)
    ax.add_patch(rect4)
    ax.text(55, 20.5, 'AI & REAL-TIME WEB EVIDENCE TIER', fontsize=9.5, fontweight='bold', color='#5b21b6')
    ax.text(74, 11, '• Google Gemini API (@google/genai)\n  Task 1: Claim extraction & query plan\n  Task 2: Multi-source evidence synthesis\n• SerpApi Engine (Google Search API)\n  Organic news & institutional retrieval',
            fontsize=7.5, ha='center', va='center', color='#4c1d95')

    plt.tight_layout()
    plt.savefig('architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created architecture.png")

def create_class_diagram():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, 'DATA MODEL & CLASS SCHEMA DIAGRAM', fontsize=14, fontweight='bold', ha='center', color='#1e3a8a')

    # Box 1: FactCheck Model
    rect1 = patches.FancyBboxPatch((5, 30), 45, 63, boxstyle="round,pad=0.5", ec="#1e40af", fc="#f8fafc", lw=2)
    ax.add_patch(rect1)
    
    # Header
    hdr1 = patches.Rectangle((5, 87), 45, 6, ec="#1e40af", fc="#1e40af")
    ax.add_patch(hdr1)
    ax.text(27.5, 90, '«Mongoose Document»\nFactCheck', fontsize=9, fontweight='bold', ha='center', va='center', color='#ffffff')

    factcheck_fields = (
        "+ _id: ObjectId\n"
        "+ claimText: String [required, max 1000]\n"
        "+ extractedClaim: String\n"
        "+ entities: String[]\n"
        "+ verdict: Enum ('True','False','Misleading',\n"
        "                'Disputed','Unverified')\n"
        "+ confidence: Number [0 - 100]\n"
        "+ explanation: String [required]\n"
        "+ supportingEvidence: String[]\n"
        "+ contradictingEvidence: String[]\n"
        "+ sources: SourceSchema[]\n"
        "+ limitations: String[]\n"
        "+ createdAt: Date [default: now, indexed]\n"
        "---------------------------------------\n"
        "+ save(): Promise<FactCheck>\n"
        "+ static find(query): Query\n"
        "+ static findById(id): Query"
    )
    ax.text(7, 57, factcheck_fields, fontsize=7.5, family='monospace', va='center', color='#0f172a')

    # Box 2: SourceSchema
    rect2 = patches.FancyBboxPatch((56, 60), 40, 33, boxstyle="round,pad=0.5", ec="#059669", fc="#f8fafc", lw=2)
    ax.add_patch(rect2)
    hdr2 = patches.Rectangle((56, 87), 40, 6, ec="#059669", fc="#059669")
    ax.add_patch(hdr2)
    ax.text(76, 90, '«Mongoose Embedded Schema»\nSourceSchema', fontsize=9, fontweight='bold', ha='center', va='center', color='#ffffff')

    source_fields = (
        "+ title: String [required]\n"
        "+ url: String [required]\n"
        "+ snippet: String\n"
        "+ date: String\n"
        "+ relevance: String\n"
        "+ _id: false (embedded document)"
    )
    ax.text(58, 73, source_fields, fontsize=8, family='monospace', va='center', color='#0f172a')

    # Embedded relationship line
    ax.annotate('1..* (contains)', xy=(56, 75), xytext=(50, 75),
                arrowprops=dict(arrowstyle="<|-", color="#1e40af", lw=2))

    # Box 3: verifyController & services
    rect3 = patches.FancyBboxPatch((56, 5), 40, 48, boxstyle="round,pad=0.5", ec="#7c3aed", fc="#f8fafc", lw=2)
    ax.add_patch(rect3)
    hdr3 = patches.Rectangle((56, 47), 40, 6, ec="#7c3aed", fc="#7c3aed")
    ax.add_patch(hdr3)
    ax.text(76, 50, '«Controllers & Service Layer»', fontsize=9, fontweight='bold', ha='center', va='center', color='#ffffff')

    ctrl_methods = (
        "«verifyController»\n"
        "+ verifyClaim(req, res, next): Promise\n\n"
        "«historyController»\n"
        "+ getHistory(req, res, next): Promise\n"
        "+ getHistoryById(req, res, next): Promise\n\n"
        "«geminiService»\n"
        "+ extractClaimAndQueries(claim): Promise\n"
        "+ analyzeEvidenceAndDetermineVerdict(): Promise\n\n"
        "«serpApiService»\n"
        "+ fetchEvidenceForQueries(queries): Promise"
    )
    ax.text(58, 25, ctrl_methods, fontsize=7.5, family='monospace', va='center', color='#0f172a')

    # Association between controller and FactCheck
    ax.annotate('instantiates & persists', xy=(50, 40), xytext=(56, 40),
                arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2, ls='--'))

    plt.tight_layout()
    plt.savefig('class_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created class_diagram.png")

def create_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, 'CLAIM VERIFICATION TRANSACTION SEQUENCE', fontsize=14, fontweight='bold', ha='center', color='#1e3a8a')

    # Participants
    participants = [
        (10, 'User / Client\n(React UI)', '#3b82f6'),
        (30, 'Express API\n(/api/verify)', '#059669'),
        (50, 'Gemini Task 1\n(Claim Parser)', '#7c3aed'),
        (70, 'SerpApi Engine\n(Google Search)', '#ea580c'),
        (90, 'MongoDB\n(claimcheck DB)', '#ca8a04')
    ]

    for x, label, color in participants:
        # Header box
        rect = patches.FancyBboxPatch((x-8, 88), 16, 6, boxstyle="round,pad=0.3", ec=color, fc=color)
        ax.add_patch(rect)
        ax.text(x, 91, label, fontsize=7, fontweight='bold', ha='center', va='center', color='#ffffff')
        # Lifeline
        ax.plot([x, x], [8, 88], color='#cbd5e1', linestyle='--', lw=1.5, zorder=1)

    # Messages
    steps = [
        (84, 10, 30, '1: POST /api/verify { claim }', '#1e40af'),
        (76, 30, 50, '2: extractClaimAndQueries(claim)', '#6d28d9'),
        (68, 50, 30, '3: Return { extractedClaim, queries }', '#6d28d9', True),
        (60, 30, 70, '4: fetchEvidenceForQueries(queries)', '#c2410c'),
        (52, 70, 30, '5: Return Organic Search Snippets', '#c2410c', True),
        (44, 30, 50, '6: analyzeEvidenceAndDetermineVerdict()', '#6d28d9'),
        (36, 50, 30, '7: Return Structured Verdict & Points', '#6d28d9', True),
        (28, 30, 90, '8: new FactCheck(...).save()', '#a16207'),
        (20, 90, 30, '9: Return saved document with _id', '#a16207', True),
        (12, 30, 10, '10: 201 Created { success: true, data }', '#1e40af', True)
    ]

    for step in steps:
        y = step[0]
        x1 = step[1]
        x2 = step[2]
        msg = step[3]
        color = step[4]
        is_return = len(step) > 5 and step[5]

        ls = '--' if is_return else '-'
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.8, linestyle=ls))
        
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 1.5, msg, fontsize=7.2, fontweight='bold', ha='center', color=color)

    plt.tight_layout()
    plt.savefig('sequence_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created sequence_diagram.png")

def create_ui_screenshots():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 6), dpi=300)
    
    # UI 1: Dashboard with Input & Checking Progress
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.add_patch(patches.Rectangle((0, 0), 100, 100, fc="#f8fafc", ec="#cbd5e1", lw=2))
    
    # Navbar
    ax1.add_patch(patches.Rectangle((0, 88), 100, 12, fc="#1e293b"))
    ax1.text(6, 94, 'ClaimCheck', fontsize=12, fontweight='bold', color='#ffffff', va='center')
    ax1.text(94, 94, 'MongoDB: Connected', fontsize=8, color='#4ade80', ha='right', va='center')

    # Card
    ax1.add_patch(patches.FancyBboxPatch((6, 42), 88, 42, boxstyle="round,pad=1", fc="#ffffff", ec="#e2e8f0", lw=1.5))
    ax1.text(10, 78, 'Verify Any Claim in Real Time', fontsize=11, fontweight='bold', color='#0f172a')
    ax1.text(10, 72, 'Evidence-grounded verification against live web sources', fontsize=7.5, color='#64748b')
    
    ax1.add_patch(patches.FancyBboxPatch((10, 52), 80, 16, boxstyle="round,pad=0.5", fc="#f1f5f9", ec="#cbd5e1"))
    ax1.text(12, 60, '"NASA discovered alien life on Mars in October 2026"', fontsize=8, color='#334155')

    ax1.add_patch(patches.FancyBboxPatch((10, 44), 30, 6, boxstyle="round,pad=0.3", fc="#2563eb", ec="#2563eb"))
    ax1.text(25, 47, 'Verify Claim', fontsize=8, fontweight='bold', color='#ffffff', ha='center', va='center')

    # Progress state machine card
    ax1.add_patch(patches.FancyBboxPatch((6, 6), 88, 32, boxstyle="round,pad=1", fc="#ffffff", ec="#3b82f6", lw=1.5))
    ax1.text(10, 32, 'Verification in Progress...', fontsize=10, fontweight='bold', color='#1e40af')
    
    stages = [
        ('[Done]', 'Stage 1: Deconstructing Claim & Entities', '#10b981'),
        ('[Done]', 'Stage 2: Retrieving Live Organic Web Evidence (SerpApi)', '#10b981'),
        ('[Active]', 'Stage 3: Cross-Referencing Evidence & Synthesizing (Gemini)', '#3b82f6'),
        ('[Pending]', 'Stage 4: Persisting Record to MongoDB', '#94a3b8')
    ]
    for idx, (icon, text, col) in enumerate(stages):
        y_pos = 25 - (idx * 6)
        ax1.text(10, y_pos, f'{icon}  {text}', fontsize=7.5, fontweight='bold', color=col)

    ax1.text(50, 2, 'Figure 16.1: Submission Interface & Live Verification Pipeline', fontsize=9, fontweight='bold', ha='center', color='#1e293b')

    # UI 2: Detailed Result Card & Verdict
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.add_patch(patches.Rectangle((0, 0), 100, 100, fc="#f8fafc", ec="#cbd5e1", lw=2))

    # Navbar
    ax2.add_patch(patches.Rectangle((0, 88), 100, 12, fc="#1e293b"))
    ax2.text(6, 94, 'ClaimCheck - Report Details', fontsize=11, fontweight='bold', color='#ffffff', va='center')

    # Verdict Card
    ax2.add_patch(patches.FancyBboxPatch((6, 8), 88, 76, boxstyle="round,pad=1", fc="#ffffff", ec="#e2e8f0", lw=1.5))
    
    # Verdict Badge
    ax2.add_patch(patches.FancyBboxPatch((10, 74), 28, 7, boxstyle="round,pad=0.3", fc="#fee2e2", ec="#ef4444", lw=1.5))
    ax2.text(24, 77.5, '✕  FALSE', fontsize=9, fontweight='bold', color='#dc2626', ha='center', va='center')
    ax2.text(84, 77.5, 'Confidence: 96%', fontsize=8.5, fontweight='bold', color='#0f172a', ha='right', va='center')

    ax2.text(10, 68, 'Claim: "NASA discovered alien life on Mars in October 2026"', fontsize=8, fontweight='bold', color='#0f172a')
    ax2.text(10, 62, 'Explanation:', fontsize=7.5, fontweight='bold', color='#475569')
    ax2.text(10, 53, 'No scientific announcement or peer-reviewed publication confirms discovery\nof extraterrestrial life on Mars. Official NASA rover missions report no such findings.', fontsize=7, color='#334155')

    # Contradicting points box
    ax2.add_patch(patches.FancyBboxPatch((10, 29), 80, 19, boxstyle="round,pad=0.5", fc="#fef2f2", ec="#fecaca"))
    ax2.text(12, 44, 'Contradicting Evidence:', fontsize=7.5, fontweight='bold', color='#991b1b')
    ax2.text(12, 38, '• NASA official astrobiology press releases confirm no extraterrestrial life identified.', fontsize=6.8, color='#7f1d1d')
    ax2.text(12, 32, '• Major science journals (Nature, Science) have no publications corroborating the claim.', fontsize=6.8, color='#7f1d1d')

    # Sources box
    ax2.add_patch(patches.FancyBboxPatch((10, 11), 80, 15, boxstyle="round,pad=0.5", fc="#f0fdf4", ec="#bbf7d0"))
    ax2.text(12, 22, 'Verified Evidence Sources (SerpApi Organic Web):', fontsize=7.5, fontweight='bold', color='#166534')
    ax2.text(12, 17, '1. NASA Mars Exploration Program (nasa.gov/mars)', fontsize=6.8, color='#15803d')
    ax2.text(12, 13, '2. Reuters Fact Check (reuters.com/fact-check)', fontsize=6.8, color='#15803d')

    ax2.text(50, 2, 'Figure 16.2: Complete Evidence Verdict Report & Source Citations', fontsize=9, fontweight='bold', ha='center', color='#1e293b')

    plt.tight_layout()
    plt.savefig('screenshots.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created screenshots.png")

if __name__ == '__main__':
    create_architecture_diagram()
    create_class_diagram()
    create_sequence_diagram()
    create_ui_screenshots()
