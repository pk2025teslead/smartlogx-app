'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Calendar, Plus, Search, Clock, Check, X } from 'lucide-react'
import { useEffect, useState } from 'react'

interface LeaveRequest {
  id: string
  leave_date: string
  leave_type: string
  notes: string
  status: string
  created_at: string
}

export default function UserLeavePage() {
  const { data: session } = useSession()
  const [leaves, setLeaves] = useState<LeaveRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  // Form state
  const [formData, setFormData] = useState({
    leaveDate: '',
    leaveType: 'PLANNED',
    notes: ''
  })

  useEffect(() => {
    fetchLeaves()
  }, [])

  const fetchLeaves = async () => {
    try {
      const response = await fetch('/api/user/attendance/leave')
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const response = await fetch('/api/user/attendance/leave', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        fetchLeaves()
        setIsDialogOpen(false)
        setFormData({
          leaveDate: '',
          leaveType: 'PLANNED',
          notes: ''
        })
      }
    } catch (error) {
      console.error('Failed to submit leave request:', error)
    }
  }

  const filteredLeaves = leaves.filter(leave =>
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
            <h1 className="text-3xl font-bold text-gray-900">Leave Requests</h1>
            <p className="text-gray-600 mt-2">Manage your leave requests and view status</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Request Leave
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Request Leave</DialogTitle>
                <DialogDescription>
                  Submit a new leave request for approval
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="leaveDate">Leave Date</Label>
                  <Input
                    id="leaveDate"
                    type="date"
                    value={formData.leaveDate}
                    onChange={(e) => setFormData({ ...formData, leaveDate: e.target.value })}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="leaveType">Leave Type</Label>
                  <Select value={formData.leaveType} onValueChange={(value) => setFormData({ ...formData, leaveType: value })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="PLANNED">Planned Leave</SelectItem>
                      <SelectItem value="CASUAL">Casual Leave</SelectItem>
                      <SelectItem value="EMERGENCY">Emergency Leave</SelectItem>
                      <SelectItem value="SICK">Sick Leave</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="notes">Reason</Label>
                  <Textarea
                    id="notes"
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    placeholder="Please provide reason for leave"
                    rows={3}
                    required
                  />
                </div>

                <div className="flex justify-end space-x-2">
                  <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">
                    Submit Request
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Stats */}
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

        {/* Leave Requests */}
        <Card>
          <CardHeader>
            <CardTitle>Your Leave Requests</CardTitle>
            <CardDescription>All your submitted leave requests</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">Loading leave requests...</div>
            ) : filteredLeaves.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                {searchTerm ? 'No leave requests found matching your search' : 'No leave requests yet. Submit your first request!'}
              </div>
            ) : (
              <div className="space-y-4">
                {filteredLeaves.map((leave) => (
                  <div key={leave.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="font-medium text-gray-900">
                            {new Date(leave.leave_date).toLocaleDateString()}
                          </h3>
                          <span className={`px-2 py-1 rounded-full text-xs ${getLeaveTypeColor(leave.leave_type)}`}>
                            {leave.leave_type}
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(leave.status)}`}>
                            {leave.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">{leave.notes}</p>
                        <p className="text-xs text-gray-500">
                          Requested on {new Date(leave.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}