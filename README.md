# Loan Approval App

## Project Brief

This project is a UK-focused loan approval prototype. A customer enters their financial details and receives:

- An approval or denial decision
- A confidence score
- A clear explanation and next steps
- Alternative offers when the requested loan is not suitable

The project also plans for responsible AI: decisions should be explainable, potentially biased messages should be checked, and uncertain cases should be sent to a human reviewer.

## Planning Before Code

Before building features, I broke the product into five simple responsibilities:

1. **Collect**: capture and validate an applicant's information.
2. **Assess**: calculate a decision from measurable financial factors.
3. **Explain**: show the result in plain language rather than returning a model score alone.
4. **Protect**: check generated messages for unsafe or unfair wording.
5. **Review**: give staff a queue for decisions that need human attention.

This separation makes the system easier to test and replace. For example, the initial scoring rules can later be replaced by a trained model without rebuilding the form or the review interface.

## Current User Journey

```text
Customer completes form
        |
        v
Frontend validates the input
        |
        v
FastAPI receives the application
        |
        v
Decision service calculates APPROVED or DENIED
        |
        +--> Approved: show decision and next steps
        |
        +--> Denied: show explanation and alternative offers
        |
        +--> Uncertain or flagged: send to human review
```

## Technical Strategy

### Frontend

- Next.js and React with TypeScript
- Tailwind CSS for a responsive, accessible interface
- React Hook Form for field validation
- Axios client for communication with the API
- Shared TypeScript types for request and response contracts

### Backend

- FastAPI for a small, typed REST API
- Pydantic models for request validation
- In-memory storage for the prototype
- A transparent baseline scoring method while the production ML model is developed
- Decision records that can later be moved to PostgreSQL

### Decision Process

The current baseline score uses four understandable signals:

- Credit score
- Income compared with the requested loan
- Existing debt compared with income
- Years of employment

The score is deliberately easy to inspect. A later version can introduce Gradient Boosting, model evaluation, and feature importance while keeping the same API response shape.

## Expected Problems and Mitigations

| Possible problem | Planned response |
| --- | --- |
| Invalid or incomplete customer data | Validate in the browser and again with Pydantic on the server. |
| Frontend cannot reach the API | Use one API client, environment-based URLs, CORS configuration, and visible error messages. |
| A model gives an unfair result | Measure outcomes across groups, log features and decisions, and route uncertain cases to a person. |
| Generated emails contain harmful or biased wording | Run a lightweight check first, then a stricter check for flagged messages. |
| The LLM is unavailable or too expensive | Add timeouts, retries, rate limits, and a safe template fallback. |
| A decision cannot be explained later | Save the input summary, score, decision, confidence, and timestamp in an audit trail. |
| A database or model changes the response shape | Keep stable request and response schemas and cover them with integration tests. |
| Sensitive financial information is exposed | Keep secrets in environment variables, minimise stored data, and restrict admin access. |

## Delivery Plan

### Milestone 1: Working Prototype

- [ ] Create the Next.js frontend and FastAPI backend
- [ ] Build and style the customer application form
- [ ] Validate the shared request and response types
- [ ] Connect the form to the API
- [ ] Return an immediate baseline decision
- [ ] Display approval, denial, confidence, and alternative offers

### Milestone 2: Reliable Product Behaviour

- [ ] Add automated frontend and backend tests
- [ ] Add a real database and migrations
- [ ] Add structured audit records
- [ ] Improve loading, empty, and error states
- [ ] Add authentication for staff features

### Milestone 3: Responsible AI Workflow

- [ ] Prepare and document a representative training dataset
- [ ] Train and evaluate the Gradient Boosting model
- [ ] Compare model output with the baseline rules
- [ ] Add Level 1 and Level 2 message checks
- [ ] Route flagged cases to the admin review queue
- [ ] Record fairness and performance metrics

### Milestone 4: Production Readiness

- [ ] Add secure deployment configuration
- [ ] Add CI checks for type errors, tests, and linting
- [ ] Add monitoring and alerting
- [ ] Run load, security, and bias validation
- [ ] Document support and incident procedures

## Definition of Done

A feature is ready when:

- A valid user journey works from form submission to response.
- Invalid input produces a useful message.
- API errors are visible to the user and logged for developers.
- The behaviour is covered by an appropriate test.
- Decisions are explainable and auditable.
- Sensitive configuration is not committed to source control.
