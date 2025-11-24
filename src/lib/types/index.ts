export interface Opportunity {
  id: string;
  title: string;
  description: string;
  market: string;
  score: number;
  trend: number;
  competition: 'low' | 'medium' | 'high';
  revenue_potential: string;
  validated: boolean;
  source: string;
  discovered_at: string;
}

export interface Capability {
  id: string;
  name: string;
  category: 'research' | 'analysis' | 'development' | 'marketing' | 'operations';
  confidence: number;
  learned_at: string;
  usage_count: number;
}

export interface PipelineStage {
  id: string;
  name: string;
  description: string;
  opportunities: number;
  color: string;
}

export interface MetaProofEntry {
  id: string;
  timestamp: string;
  action: string;
  agent: string;
  result: string;
  verified: boolean;
}

export interface AIStatus {
  status: 'idle' | 'thinking' | 'researching' | 'building' | 'deploying';
  current_task: string;
  progress: number;
}