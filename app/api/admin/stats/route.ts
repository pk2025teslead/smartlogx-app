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

    // Get statistics using raw SQL queries for MySQL
    const [userCount] = await prisma.$queryRaw`SELECT COUNT(*) as count FROM users_master` as any[]
    const [logCount] = await prisma.$queryRaw`SELECT COUNT(*) as count FROM user_logs WHERE MONTH(LOG_DATE) = MONTH(CURDATE()) AND YEAR(LOG_DATE) = YEAR(CURDATE())` as any[]
    const [pendingLeaves] = await prisma.$queryRaw`SELECT COUNT(*) as count FROM attendance_leave_v2 WHERE status = 'PENDING'` as any[]
    const [pendingCompOffs] = await prisma.$queryRaw`SELECT COUNT(*) as count FROM attendance_compoff WHERE IS_APPROVED IS NULL` as any[]
    const [pendingWFH] = await prisma.$queryRaw`SELECT COUNT(*) as count FROM attendance_wfh WHERE IS_APPROVED IS NULL` as any[]

    const stats = {
      totalUsers: Number(userCount.count),
      totalLogs: Number(logCount.count),
      pendingLeaves: Number(pendingLeaves.count),
      pendingCompOffs: Number(pendingCompOffs.count),
      pendingWFH: Number(pendingWFH.count)
    }

    return NextResponse.json(stats)
  } catch (error) {
    console.error('Error fetching admin stats:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}