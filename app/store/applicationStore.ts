import { create } from 'zustand';
import { LoanApplicationResponse, EscalatedApplication } from '@/app/types';

interface ApplicationState {
  applications: Record<string, LoanApplicationResponse>;
  currentApplication: LoanApplicationResponse | null;
  loading: boolean;
  error: string | null;
  
  setCurrentApplication: (app: LoanApplicationResponse) => void;
  addApplication: (app: LoanApplicationResponse) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useApplicationStore = create<ApplicationState>((set) => ({
  applications: {},
  currentApplication: null,
  loading: false,
  error: null,
  
  setCurrentApplication: (app) => set({ currentApplication: app }),
  addApplication: (app) => set((state) => ({
    applications: { ...state.applications, [app.application_id]: app }
  })),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));

interface AdminState {
  escalatedApplications: EscalatedApplication[];
  selectedApplication: EscalatedApplication | null;
  loading: boolean;
  error: string | null;
  
  setEscalatedApplications: (apps: EscalatedApplication[]) => void;
  setSelectedApplication: (app: EscalatedApplication | null) => void;
  removeFromQueue: (appId: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useAdminStore = create<AdminState>((set) => ({
  escalatedApplications: [],
  selectedApplication: null,
  loading: false,
  error: null,
  
  setEscalatedApplications: (apps) => set({ escalatedApplications: apps }),
  setSelectedApplication: (app) => set({ selectedApplication: app }),
  removeFromQueue: (appId) => set((state) => ({
    escalatedApplications: state.escalatedApplications.filter(app => app.id !== appId)
  })),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));

interface MetricsState {
  totalApplications: number;
  approvalRate: number;
  escalationRate: number;
  averageBiasScore: number;
  loading: boolean;
  
  updateMetrics: (data: any) => void;
  setLoading: (loading: boolean) => void;
}

export const useMetricsStore = create<MetricsState>((set) => ({
  totalApplications: 0,
  approvalRate: 0,
  escalationRate: 0,
  averageBiasScore: 0,
  loading: false,
  
  updateMetrics: (data) => set({
    totalApplications: data.total_applications || 0,
    approvalRate: data.approval_rate || 0,
    escalationRate: data.escalation_rate || 0,
    averageBiasScore: data.average_bias_score_l1 || 0,
  }),
  setLoading: (loading) => set({ loading }),
}));
