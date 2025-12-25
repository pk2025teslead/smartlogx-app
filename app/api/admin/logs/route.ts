import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/db'

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions)

    if (!session || (session.user.role !== 'ADMIN' && session.user.role !== 'IT COORDINATOR')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Get all logs with user information using raw SQL for MySQL
    const logs = await prisma.$queryRaw`
      SELECT 
        ul.ID, ul.USER_ID, ul.PROJECT_TITLE, ul.LOG_HEADING, ul.LOG_DETAILS,
        ul.LOG_DATE, ul.SESSION_TYPE, ul.APPROVAL_REQUIRED, ul.APPROVAL_CODE, ul.CREATED_AT,
        um.EMP_NAME, um.EMP_ID
      FROM user_logs ul
      JOIN users_master um ON ul.USER_ID = um.ID
      ORDER BY ul.LOG_DATE DESC, ul.CREATED_AT DESC
    `

    return NextResponse.json(logs)
  } catch (error) {
    console.error('Error fetching logs:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}