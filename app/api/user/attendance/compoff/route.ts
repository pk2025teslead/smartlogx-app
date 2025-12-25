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

    // Get user's comp-off requests using raw SQL
    const compOffs = await prisma.$queryRaw`
      SELECT * FROM attendance_compoff 
      WHERE user_id = ${session.user.id}
      ORDER BY requested_at DESC
    `

    return NextResponse.json(compOffs)
  } catch (error) {
    console.error('Error fetching comp-offs:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { sundayDate, workPurpose, compOffDate, noCompOff, notes } = await request.json()

    if (!sundayDate || !workPurpose) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    // Create new comp-off request using raw SQL
    await prisma.$executeRaw`
      INSERT INTO attendance_compoff (
        user_id, sunday_date, work_purpose, compoff_date, no_compoff, 
        notes, is_approved, requested_at, updated_at
      )
      VALUES (
        ${session.user.id}, ${sundayDate}, ${workPurpose}, ${compOffDate || null}, ${noCompOff || false},
        ${notes || null}, 'PENDING', NOW(), NOW()
      )
    `

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error creating comp-off request:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}