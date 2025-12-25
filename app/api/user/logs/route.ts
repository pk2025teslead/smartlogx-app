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

    // Get user's work logs using raw SQL
    const logs = await prisma.$queryRaw`
      SELECT * FROM user_logs 
      WHERE user_id = ${session.user.id}
      ORDER BY log_date DESC, created_at DESC
    `

    return NextResponse.json(logs)
  } catch (error) {
    console.error('Error fetching logs:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { projectTitle, logHeading, logDetails, logDate, sessionType } = await request.json()

    if (!projectTitle || !logHeading || !logDetails || !logDate || !sessionType) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    // Create new work log using raw SQL
    await prisma.$executeRaw`
      INSERT INTO user_logs (user_id, project_title, log_heading, log_details, log_date, session_type, created_at, updated_at)
      VALUES (${session.user.id}, ${projectTitle}, ${logHeading}, ${logDetails}, ${logDate}, ${sessionType}, NOW(), NOW())
    `

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error creating log:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}