import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface BugPredictionRequest {
  title: string;
  description: string;
}

export interface BugPredictionResponse {
  assigned_to: string;
  assignment_confidence: number;
  priority: string;
  priority_confidence: number;
  is_duplicate: boolean;
  duplicate_info: {
    id?: number;
    title?: string;
    similarity?: number;
  };
}

export interface BugHistoryItem {
  id: number;
  title: string;
  description: string;
  assigned_to: string;
  assignment_confidence: number;
  priority: string;
  priority_confidence: number;
  confidence: number;
  created_at: string;
  is_duplicate: boolean;
  duplicate_of: number | null;
}

export const bugService = {
  predict: async (data: BugPredictionRequest): Promise<BugPredictionResponse> => {
    const response = await api.post<BugPredictionResponse>('/predict', data);
    return response.data;
  },
  
  getHistory: async (): Promise<BugHistoryItem[]> => {
    const response = await api.get<BugHistoryItem[]>('/bugs');
    return response.data;
  },
};

export default api;
