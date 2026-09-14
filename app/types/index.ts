
export type ApplicationData = {
  name: string;
  age: number;
  income: number;
  credit_score: number;
  loan_amount: number;
  employment_years: number;
  existing_debt: number;
};

export type LoanApplicationRequest = ApplicationData;

export type LoanOffer = {
  loan_amount: number;
  interest_rate: number;
  term_months: number;
  reason: string;
};

export type LoanApplicationResponse = {
  application_id: string;
  status: string;
  decision: "APPROVED" | "DENIED" | "PENDING";
  confidence: number;
  email?: string;
  offers?: LoanOffer[];
  next_steps: string;
};

export type EscalatedApplication = {
  id: string;
  applicant_name: string;
  applicant_email: string;
  bias_score_l1: number;
  bias_score_l2?: number;
  generated_email: string;
  reason_escalated: string;
  application_data: ApplicationData;
};

export type AdminReviewAction = {
  application_id: string;
  decision: "APPROVE" | "REJECT";
  notes: string;
};
