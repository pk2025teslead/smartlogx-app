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

    const userId = session.user.id

    // Get dashboard stats using raw SQL
    const [
      totalLogsResult,
      thisMonthLogsResult,
      pendingLeavesResult,
      approvedLeavesResult,
      pendingCompOffsResult,
      pendingWFHResult
    ] = await Promise.all([
      // Total logs
      prisma.$queryRaw`SELECT COUNT(*) as count FROM user_logs WHERE user_id = ${userId}`,
      
      // This month logs
      prisma.$queryRaw`
        SELECT COUNT(*) as count 
        FROM user_logs 
        WHERE user_id = ${userId} 
        AND MONTH(log_date) = MONTH(CURDATE()) 
        AND YEAR(log_date) = YEAR(CURDATE())
      `,
      
      // Pending leaves
      prisma.$queryRaw`
        SELECT COUNT(*) as count 
        FROM attendance_leave_v2 
        WHERE user_id = ${userId} AND status = 'PENDING'
      `,
      
      // Approved leaves
      prisma.$queryRaw`
        SELECT COUNT(*) as count 
        FROM attendance_leave_v2 
        WHERE user_id = ${userId} AND status = 'APPROVED'
      `,
      
      // Pending comp-offs
      prisma.$queryRaw`
        SELECT COUNT(*) as count 
        FROM attendance_compoff 
        WHERE user_id = ${userId} AND is_approved = 'PENDING'
      `,
      
      // Pending WFH
      prisma.$queryRaw`
        SELECT COUNT(*) as count 
        FROM attendance_wfh 
        WHERE user_id = ${userId} AND is_approved = 'PENDING'
      `
    ])

    const stats = {
      totalLogs: Number((totalLogsResult as any)[0]?.count || 0),
      thisMonthLogs: Number((thisMonthLogsResult as any)[0]?.count || 0),
      pendingLeaves: Number((pendingLeavesResult as any)[0]?.count || 0),
      approvedLeaves: Number((approvedLeavesResult as any)[0]?.count || 0),
      pendingCompOffs: Number((pendingCompOffsResult as any)[0]?.count || 0),
      pendingWFH: Number((pendingWFHResult as any)[0]?.count || 0)
    }

    return NextResponse.json(stats)
  } catch (error) {
    console.error('Error fetching dashboard stats:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}