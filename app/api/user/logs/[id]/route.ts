import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/db'

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { projectTitle, logHeading, logDetails, logDate, sessionType } = await request.json()
    const logId = params.id

    if (!projectTitle || !logHeading || !logDetails || !logDate || !sessionType) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    // Update work log using raw SQL
    await prisma.$executeRaw`
      UPDATE user_logs 
      SET 
        project_title = ${projectTitle},
        log_heading = ${logHeading},
        log_details = ${logDetails},
        log_date = ${logDate},
        session_type = ${sessionType},
        updated_at = NOW()
      WHERE id = ${logId} AND user_id = ${session.user.id}
    `

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error updating log:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const logId = params.id

    // Delete work log using raw SQL
    await prisma.$executeRaw`
      DELETE FROM user_logs 
      WHERE id = ${logId} AND user_id = ${session.user.id}
    `

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error deleting log:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}