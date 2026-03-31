import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface FormData {
  first_name: string;
  last_name: string;
  nationality: string;
  date_of_birth: string;
}

export interface ComparisonResult {
  id: number;
  similarity_score: number;
  form_data: FormData;
  extracted_data: Record<string, string>;
  field_scores: Record<string, number>;
  timestamp: string;
}

export const compareData = async (formData: FormData, imageFile: File): Promise<ComparisonResult> => {
  const data = new FormData();
  data.append('first_name', formData.first_name);
  data.append('last_name', formData.last_name);
  data.append('nationality', formData.nationality);
  data.append('date_of_birth', formData.date_of_birth);
  data.append('image', imageFile);

  const response = await axios.post(`${API_URL}/api/compare`, data, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data.result;
};

export const getHistory = async (limit: number = 10) => {
  const response = await axios.get(`${API_URL}/api/history?limit=${limit}`);
  return response.data.history;
};

export const getComparison = async (id: number) => {
  const response = await axios.get(`${API_URL}/api/comparison/${id}`);
  return response.data.comparison;
};

