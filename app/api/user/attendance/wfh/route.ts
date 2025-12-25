import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/db'

export async function GET() {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Get user's WFH requests using raw SQL
    const wfhRequests = await prisma.$queryRaw`
      SELECT * FROM attendance_wfh 
      WHERE user_id = ${session.user.id}
      ORDER BY requested_at DESC
    `

    return NextResponse.json(wfhRequests)
  } catch (error) {
    console.error('Error fetching WFH requests:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { wfhDate, reason, notes } = await request.json()

    if (!wfhDate || !reason) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    // Create new WFH request using raw SQL
    await prisma.$executeRaw`
      INSERT INTO attendance_wfh (
        user_id, wfh_date, reason, notes, is_approved, requested_at, updated_at
      )
      VALUES (
        ${session.user.id}, ${wfhDate}, ${reason}, ${notes || null}, 'PENDING', NOW(), NOW()
      )
    `

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error creating WFH request:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}