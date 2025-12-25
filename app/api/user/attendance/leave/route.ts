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

    // Get user's leave requests using raw SQL
    const leaves = await prisma.$queryRaw`
      SELECT * FROM attendance_leave_v2 
      WHERE user_id = ${session.user.id}
      ORDER BY created_at DESC
    `

    return NextResponse.json(leaves)
  } catch (error) {
    console.error('Error fetching leaves:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { leaveDate, leaveType, notes } = await request.json()

    if (!leaveDate || !leaveType || !notes) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    // Calculate editable until date (24 hours from now)
    const editableUntil = new Date()
    editableUntil.setHours(editableUntil.getHours() + 24)

    // Create new leave request using raw SQL
    await prisma.$executeRaw`
      INSERT INTO attendance_leave_v2 (
        user_id, leave_date, leave_type, notes, status, 
        is_editable, editable_until, created_by, created_at, updated_at
      )
      VALUES (
        ${session.user.id}, ${leaveDate}, ${leaveType}, ${notes}, 'PENDING',
        1, ${editableUntil}, ${session.user.id}, NOW(), NOW()
      )
    `

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error creating leave request:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}