import React from 'react';
import axios from 'axios';
import { EscalatedApplication, AdminReviewAction } from '@/app/types';

export const AdminReviewQueue: React.FC = () => {
  const [escalated, setEscalated] = React.useState<EscalatedApplication[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [reviewingId, setReviewingId] = React.useState<string | null>(null);
  const [reviewNotes, setReviewNotes] = React.useState('');

  React.useEffect(() => {
    fetchQueue();
  }, []);

  const fetchQueue = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/admin/review-queue');
      setEscalated(res.data);
    } catch (error) {
      console.error('Failed to fetch review queue:', error);
    }
    setLoading(false);
  };

  const handleApprove = async (applicationId: string) => {
    try {
      const action: AdminReviewAction = {
        application_id: applicationId,
        decision: 'APPROVE',
        notes: reviewNotes || 'Approved by admin'
      };
      await axios.post(`/api/admin/review/${applicationId}`, action);
      setReviewingId(null);
      setReviewNotes('');
      await fetchQueue();
    } catch (error) {
      console.error('Failed to approve application:', error);
    }
  };

  const handleReject = async (applicationId: string) => {
    try {
      const action: AdminReviewAction = {
        application_id: applicationId,
        decision: 'REJECT',
        notes: reviewNotes || 'Rejected by admin - requires modification'
      };
      await axios.post(`/api/admin/review/${applicationId}`, action);
      setReviewingId(null);
      setReviewNotes('');
      await fetchQueue();
    } catch (error) {
      console.error('Failed to reject application:', error);
    }
  };

  return (
    <div className="admin-review-container">
      <h2>Escalated Applications for Review</h2>
      
      {loading ? (
        <p className="loading">Loading escalated applications...</p>
      ) : escalated.length === 0 ? (
        <p className="empty-queue">No escalated applications at this time.</p>
      ) : (
        <div className="review-queue">
          {escalated.map((app) => (
            <div key={app.id} className="review-item">
              <div className="review-header">
                <h3>{app.applicant_name}</h3>
                <span className="email-badge">{app.applicant_email}</span>
              </div>

              <div className="bias-scores">
                <div className="score">
                  <p><strong>Bias Score Level 1:</strong></p>
                  <p className={`score-value ${app.bias_score_l1 > 0.6 ? 'high' : 'medium'}`}>
                    {app.bias_score_l1.toFixed(2)}
                  </p>
                </div>

                {app.bias_score_l2 !== undefined && (
                  <div className="score">
                    <p><strong>Bias Score Level 2:</strong></p>
                    <p className={`score-value ${app.bias_score_l2 > 0.7 ? 'high' : 'medium'}`}>
                      {app.bias_score_l2.toFixed(2)}
                    </p>
                  </div>
                )}
              </div>

              <div className="email-preview">
                <h4>Generated Email:</h4>
                <div className="email-content">
                  <p>{app.generated_email}</p>
                </div>
              </div>

              <div className="escalation-reason">
                <p><strong>Reason for Escalation:</strong> {app.reason_escalated}</p>
              </div>

              {reviewingId === app.id ? (
                <div className="review-form">
                  <textarea
                    placeholder="Add notes for this review..."
                    value={reviewNotes}
                    onChange={(e) => setReviewNotes(e.target.value)}
                    className="review-notes"
                  />
                  <div className="review-buttons">
                    <button
                      className="approve-btn"
                      onClick={() => handleApprove(app.id)}
                    >
                      Approve & Send
                    </button>
                    <button
                      className="reject-btn"
                      onClick={() => handleReject(app.id)}
                    >
                      Reject & Modify
                    </button>
                    <button
                      className="cancel-btn"
                      onClick={() => {
                        setReviewingId(null);
                        setReviewNotes('');
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <button
                  className="review-btn"
                  onClick={() => setReviewingId(app.id)}
                >
                  Review Application
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};