import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/db'

export async function GET() {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user || (session.user.role !== 'ADMIN' && session.user.role !== 'IT COORDINATOR')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Get all WFH requests with user details using raw SQL
    const wfhRequests = await prisma.$queryRaw`
      SELECT 
        w.*,
        u.EMP_NAME,
        u.EMP_ID
      FROM attendance_wfh w
      JOIN users_master u ON w.user_id = u.ID
      ORDER BY w.requested_at DESC
    `

    return NextResponse.json(wfhRequests)
  } catch (error) {
    console.error('Error fetching WFH requests:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}