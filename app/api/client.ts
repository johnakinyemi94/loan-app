import axios from 'axios';
import { LoanApplicationRequest, LoanApplicationResponse, EscalatedApplication, AdminReviewAction } from '@/app/types';

const API_URL = (process.env.NEXT_PUBLIC_API_URL || 'https://loan-app-ivory-zeta.vercel.app').replace(/\/$/, '');

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

client.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    throw error;
  }
);

export const apiClient = {
  
  submitApplication: (data: LoanApplicationRequest) =>
    client.post<LoanApplicationResponse>('/api/applications/submit', data),
  
  getApplicationStatus: (appId: string) =>
    client.get<LoanApplicationResponse>(`/api/applications/${appId}`),
  

  getReviewQueue: () =>
    client.get<EscalatedApplication[]>('/api/admin/review-queue'),
  
  reviewApplication: (appId: string, action: AdminReviewAction) =>
    client.post(`/api/admin/review/${appId}`, action),
  

  getMetrics: () =>
    client.get('/api/metrics'),
  

  healthCheck: () =>
    client.get('/api/health'),
};
