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

    // Get all leave requests with user details using raw SQL
    const leaves = await prisma.$queryRaw`
      SELECT 
        l.*,
        u.EMP_NAME,
        u.EMP_ID
      FROM attendance_leave_v2 l
      JOIN users_master u ON l.user_id = u.ID
      ORDER BY l.created_at DESC
    `

    return NextResponse.json(leaves)
  } catch (error) {
    console.error('Error fetching leaves:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}