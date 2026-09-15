import { NextResponse } from 'next/server';

// In-memory store is not persistent across serverless invocations.
// Replace with a real database for production use.
export async function GET() {
  return NextResponse.json([]);
}
