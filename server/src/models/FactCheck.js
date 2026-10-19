import mongoose from 'mongoose';

const SourceSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true,
  },
  url: {
    type: String,
    required: true,
    trim: true,
  },
  snippet: {
    type: String,
    default: '',
    trim: true,
  },
  date: {
    type: String,
    default: 'Date not available',
  },
  relevance: {
    type: String,
    default: 'Web search evidence',
  },
}, { _id: false });

const FactCheckSchema = new mongoose.Schema({
  claimText: {
    type: String,
    required: [true, 'Claim text is required'],
    trim: true,
    maxlength: [1000, 'Claim text cannot exceed 1000 characters'],
  },
  extractedClaim: {
    type: String,
    default: '',
    trim: true,
  },
  entities: {
    type: [String],
    default: [],
  },
  verdict: {
    type: String,
    required: [true, 'Verdict is required'],
    enum: {
      values: ['True', 'False', 'Misleading', 'Disputed', 'Unverified'],
      message: '{VALUE} is not a valid verdict category',
    },
  },
  confidence: {
    type: Number,
    required: [true, 'Confidence score is required'],
    min: [0, 'Confidence must be at least 0'],
    max: [100, 'Confidence cannot exceed 100'],
  },
  explanation: {
    type: String,
    required: [true, 'Explanation is required'],
    trim: true,
  },
  supportingEvidence: {
    type: [String],
    default: [],
  },
  contradictingEvidence: {
    type: [String],
    default: [],
  },
  sources: {
    type: [SourceSchema],
    default: [],
  },
  limitations: {
    type: [String],
    default: [],
  },
  createdAt: {
    type: Date,
    default: Date.now,
    index: true,
  },
});

export const FactCheck = mongoose.model('FactCheck', FactCheckSchema);
