import { NextRequest, NextResponse } from 'next/server';
import { randomUUID } from 'crypto';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { name, age, income, credit_score, loan_amount, employment_years, existing_debt } = body;

    // Basic validation
    if (!name || age < 18 || age > 120 || income <= 0 || credit_score < 300 || credit_score > 850 || loan_amount <= 0 || employment_years < 0 || existing_debt < 0) {
      return NextResponse.json({ detail: 'Invalid request data' }, { status: 422 });
    }

    const appId = randomUUID().slice(0, 8);

    // Scoring logic (ported from backend/main.py)
    const incomeToLoan = income / loan_amount;
    const debtToIncome = existing_debt / income;
    let score = 0.0;
    score += credit_score >= 700 ? 0.35 : credit_score >= 650 ? 0.2 : 0.05;
    score += incomeToLoan >= 2 ? 0.3 : incomeToLoan >= 1.5 ? 0.2 : 0.05;
    score += debtToIncome <= 0.3 ? 0.2 : debtToIncome <= 0.45 ? 0.1 : 0.0;
    score += employment_years >= 5 ? 0.15 : employment_years >= 2 ? 0.1 : 0.05;

    const approved = score >= 0.65;
    const decision = approved ? 'APPROVED' : 'DENIED';
    const confidence = Math.round(Math.min(0.98, Math.max(0.55, 0.55 + Math.abs(score - 0.5) * 0.8)) * 100) / 100;

    let email: string;
    let offers: { loan_amount: number; interest_rate: number; term_months: number; reason: string }[] | undefined;
    let next_steps: string;

    if (approved) {
      email =
        `Hi ${name},\n\n` +
        `Good news: your loan application for £${loan_amount.toLocaleString('en-GB', { maximumFractionDigits: 0 })} has been approved. ` +
        `We will contact you with the final documents and funding details.\n\nThank you,\nLendwise`;
      offers = undefined;
      next_steps = 'Review the final documents when they arrive and confirm your funding details.';
    } else {
      email =
        `Hi ${name},\n\n` +
        `We are unable to approve your request for £${loan_amount.toLocaleString('en-GB', { maximumFractionDigits: 0 })} at this time. ` +
        `Here are options that may better fit your current profile.\n\nThank you,\nLendwise`;
      offers = [
        {
          loan_amount: Math.round(loan_amount * 0.7 * 100) / 100,
          interest_rate: 9.99,
          term_months: 48,
          reason: 'A smaller loan amount may reduce the payment-to-income burden.',
        },
        {
          loan_amount: Math.round(loan_amount * 0.85 * 100) / 100,
          interest_rate: 11.49,
          term_months: 60,
          reason: 'A longer term can make monthly payments more manageable.',
        },
      ];
      next_steps = 'Review the alternative offers and consider reapplying after improving your credit or debt profile.';
    }

    return NextResponse.json({
      application_id: appId,
      status: decision,
      decision,
      confidence,
      email,
      offers,
      next_steps,
    });
  } catch (err) {
    console.error('Error processing application:', err);
    return NextResponse.json({ detail: 'Error processing application' }, { status: 500 });
  }
}
