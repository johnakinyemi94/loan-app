"use client";

import React from 'react';
import { useForm } from 'react-hook-form';
import { apiClient } from '@/app/api/client';
import { ApplicationData, LoanApplicationResponse } from '@/app/types';

export const ApplicationForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<ApplicationData>();
  const [result, setResult] = React.useState<LoanApplicationResponse | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [submissionError, setSubmissionError] = React.useState<string | null>(null);

  const onSubmit = async (data: ApplicationData) => {
    setLoading(true);
    setSubmissionError(null);
    try {
      const response = await apiClient.submitApplication(data);
      setResult(response.data);
    } catch (error) {
      console.error('Application submission failed', error);
      setSubmissionError('We could not submit your application. Make sure the backend is running on port 8000 and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="loan-application-form">
      {/* Form fields */}
      <div className="form-group">
        <label>Full Name</label>
        <input 
          {...register('name', { required: 'Name is required' })} 
          placeholder="John Doe"
          className="form-input"
        />
        {errors.name && <span className="error">{errors.name.message}</span>}
      </div>

      <div className="form-group">
        <label>Age</label>
        <input 
          {...register('age', { required: 'Age is required', min: 18 })} 
          type="number" 
          placeholder="30"
          className="form-input"
        />
        {errors.age && <span className="error">{errors.age.message}</span>}
      </div>

      <div className="form-group">
        <label>Annual Income (£)</label>
        <input 
          {...register('income', { required: 'Income is required', min: 0 })} 
          type="number" 
          placeholder="75000"
          className="form-input"
        />
        {errors.income && <span className="error">{errors.income.message}</span>}
      </div>

      <div className="form-group">
        <label>Credit Score</label>
        <input 
          {...register('credit_score', { required: 'Credit score is required', min: 300, max: 850 })} 
          type="number" 
          placeholder="750"
          className="form-input"
        />
        {errors.credit_score && <span className="error">{errors.credit_score.message}</span>}
      </div>

      <div className="form-group">
        <label>Requested Loan Amount (£)</label>
        <input 
          {...register('loan_amount', { required: 'Loan amount is required', min: 0 })} 
          type="number" 
          placeholder="50000"
          className="form-input"
        />
        {errors.loan_amount && <span className="error">{errors.loan_amount.message}</span>}
      </div>

      <div className="form-group">
        <label>Employment Years</label>
        <input 
          {...register('employment_years', { required: 'Employment years is required', min: 0 })} 
          type="number" 
          placeholder="5"
          className="form-input"
        />
        {errors.employment_years && <span className="error">{errors.employment_years.message}</span>}
      </div>

      <div className="form-group">
        <label>Existing Debt (£)</label>
        <input 
          {...register('existing_debt', { required: 'Existing debt is required', min: 0 })} 
          type="number" 
          placeholder="15000"
          className="form-input"
        />
        {errors.existing_debt && <span className="error">{errors.existing_debt.message}</span>}
      </div>

      <button type="submit" disabled={loading} className="submit-btn">
        {loading ? 'Processing...' : 'Submit Application'}
      </button>

      {submissionError && (
        <p role="alert" className="mt-4 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium leading-6 text-rose-700">
          {submissionError}
        </p>
      )}

      {result && (
        <div className="result-container">
          <div className={`result ${result.decision.toLowerCase()}`}>
            <h3>Decision: {result.decision}</h3>
            <p>Status: {result.status}</p>
            <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
            <p>Next Steps: {result.next_steps}</p>
            
            {result.email && (
              <div className="email-section">
                <h4>Decision Email:</h4>
                <p className="email-preview">{result.email}</p>
              </div>
            )}

            {result.offers && result.offers.length > 0 && (
              <div className="offers-section">
                <h4>Alternative Offers:</h4>
                <div className="offers-list">
                  {result.offers.map((offer, index) => (
                    <div key={index} className="offer-card">
                      <p><strong>Amount:</strong> £{offer.loan_amount.toLocaleString()}</p>
                      <p><strong>Interest Rate:</strong> {offer.interest_rate}%</p>
                      <p><strong>Term:</strong> {offer.term_months} months</p>
                      <p><strong>Reason:</strong> {offer.reason}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <p className="application-id">Application ID: {result.application_id}</p>
          </div>
        </div>
      )}
    </form>
  );
};