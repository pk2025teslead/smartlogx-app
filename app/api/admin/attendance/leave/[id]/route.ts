import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { prisma } from '@/lib/db'

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)
    
    if (!session?.user || (session.user.role !== 'ADMIN' && session.user.role !== 'IT COORDINATOR')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { action } = await request.json()
    const leaveId = parseInt(params.id)

    if (!action || !['approve', 'reject'].includes(action)) {
      return NextResponse.json({ error: 'Invalid action' }, { status: 400 })
    }

    const status = action === 'approve' ? 'APPROVED' : 'REJECTED'

    // Update leave status using raw SQL
    await prisma.$executeRaw`
      UPDATE attendance_leave_v2 
      SET 
        status = ${status},
        approved_by = ${session.user.id},
        approved_at = NOW()
      WHERE id = ${leaveId}
    `

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Error updating leave:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}