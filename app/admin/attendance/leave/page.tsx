'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Calendar, Search, Filter, Check, X, Clock } from 'lucide-react'
import { useEffect, useState } from 'react'

interface LeaveRequest {
  id: number
  user_id: number
  leave_date: string
  leave_type: string
  notes: string
  status: string
  created_at: string
  EMP_NAME: string
  EMP_ID: string
}

export default function AdminLeaveManagementPage() {
  const { data: session } = useSession()
  const [leaves, setLeaves] = useState<LeaveRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchLeaves()
  }, [])

  const fetchLeaves = async () => {
    try {
      const response = await fetch('/api/admin/attendance/leave')
      if (response.ok) {
        const data = await response.json()
        setLeaves(data)
      }
    } catch (error) {
      console.error('Failed to fetch leaves:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApproval = async (leaveId: number, action: 'approve' | 'reject') => {
    try {
      const response = await fetch(`/api/admin/attendance/leave/${leaveId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action }),
      })

      if (response.ok) {
        fetchLeaves() // Refresh the list
      }
    } catch (error) {
      console.error('Failed to update leave:', error)
    }
  }

  const filteredLeaves = leaves.filter(leave =>
    leave.EMP_NAME.toLowerCase().includes(searchTerm.toLowerCase()) ||
    leave.leave_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    leave.notes.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING': return 'bg-yellow-100 text-yellow-800'
      case 'APPROVED': return 'bg-green-100 text-green-800'
      case 'REJECTED': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getLeaveTypeColor = (type: string) => {
    switch (type) {
      case 'PLANNED': return 'bg-blue-100 text-blue-800'
      case 'CASUAL': return 'bg-green-100 text-green-800'
      case 'EMERGENCY': return 'bg-red-100 text-red-800'
      case 'SICK': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Leave Management</h1>
            <p className="text-gray-600 mt-2">Review and manage employee leave requests</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Requests</p>
                  <p className="text-2xl font-bold">{leaves.length}</p>
                </div>
                <Calendar className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Pending</p>
                  <p className="text-2xl font-bold text-yellow-600">
                    {leaves.filter(l => l.status === 'PENDING').length}
                  </p>
                </div>
                <Clock className="h-8 w-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Approved</p>
                  <p className="text-2xl font-bold text-green-600">
                    {leaves.filter(l => l.status === 'APPROVED').length}
                  </p>
                </div>
                <Check className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Rejected</p>
                  <p className="text-2xl font-bold text-red-600">
                    {leaves.filter(l => l.status === 'REJECTED').length}
                  </p>
                </div>
                <X className="h-8 w-8 text-red-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search leave requests..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Leave Requests Table */}
        <Card>
          <CardHeader>
            <CardTitle>Leave Requests</CardTitle>
            <CardDescription>All employee leave requests</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">Loading leave requests...</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-3">Employee</th>
                      <th className="text-left p-3">Leave Date</th>
                      <th className="text-left p-3">Type</th>
                      <th className="text-left p-3">Reason</th>
                      <th className="text-left p-3">Status</th>
                      <th className="text-left p-3">Requested</th>
                      <th className="text-left p-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredLeaves.map((leave) => (
                      <tr key={leave.id} className="border-b hover:bg-gray-50">
                        <td className="p-3">
                          <div>
                            <div className="font-medium">{leave.EMP_NAME}</div>
                            <div className="text-sm text-gray-500">{leave.EMP_ID}</div>
                          </div>
                        </td>
                        <td className="p-3">
                          {new Date(leave.leave_date).toLocaleDateString()}
                        </td>
                        <td className="p-3">
                          <span className={`px-2 py-1 rounded-full text-xs ${getLeaveTypeColor(leave.leave_type)}`}>
                            {leave.leave_type}
                          </span>
                        </td>
                        <td className="p-3 max-w-xs">
                          <div className="truncate" title={leave.notes}>
                            {leave.notes || 'No reason provided'}
                          </div>
                        </td>
                        <td className="p-3">
                          <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(leave.status)}`}>
                            {leave.status}
                          </span>
                        </td>
                        <td className="p-3 text-sm text-gray-500">
                          {new Date(leave.created_at).toLocaleDateString()}
                        </td>
                        <td className="p-3">
                          {leave.status === 'PENDING' ? (
                            <div className="flex space-x-2">
                              <Button
                                size="sm"
                                onClick={() => handleApproval(leave.id, 'approve')}
                                className="bg-green-600 hover:bg-green-700"
                              >
                                <Check className="h-4 w-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant="destructive"
                                onClick={() => handleApproval(leave.id, 'reject')}
                              >
                                <X className="h-4 w-4" />
                              </Button>
                            </div>
                          ) : (
                            <span className="text-sm text-gray-500">
                              {leave.status.toLowerCase()}
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}