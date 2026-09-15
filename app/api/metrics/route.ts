import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    total_applications: 0,
    approved_count: 0,
    denied_count: 0,
    escalated_count: 0,
    approval_rate: 0,
    average_bias_score_l1: 0,
    average_bias_score_l2: null,
    escalation_rate: 0,
  });
}
