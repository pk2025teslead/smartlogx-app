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

    // Get all comp-off requests with user details using raw SQL
    const compOffs = await prisma.$queryRaw`
      SELECT 
        c.*,
        u.EMP_NAME,
        u.EMP_ID
      FROM attendance_compoff c
      JOIN users_master u ON c.user_id = u.ID
      ORDER BY c.requested_at DESC
    `

    return NextResponse.json(compOffs)
  } catch (error) {
    console.error('Error fetching comp-offs:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}