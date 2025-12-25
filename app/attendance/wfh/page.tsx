'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Home, Plus, Search, Calendar, Check, X, Clock } from 'lucide-react'
import { useEffect, useState } from 'react'

interface WFHRequest {
  id: string
  wfh_date: string
  reason: string
  notes: string | null
  status: string
  created_at: string
}

export default function UserWFHPage() {
  const { data: session } = useSession()
  const [wfhRequests, setWfhRequests] = useState<WFHRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  // Form state
  const [formData, setFormData] = useState({
    wfhDate: '',
    reason: '',
    notes: ''
  })

  useEffect(() => {
    fetchWFHRequests()
  }, [])

  const fetchWFHRequests = async () => {
    try {
      const response = await fetch('/api/user/attendance/wfh')
      if (response.ok) {
        const data = await response.json()
        setWfhRequests(data)
      }
    } catch (error) {
      console.error('Failed to fetch WFH requests:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const response = await fetch('/api/user/attendance/wfh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        fetchWFHRequests()
        setIsDialogOpen(false)
        setFormData({
          wfhDate: '',
          reason: '',
          notes: ''
        })
      }
    } catch (error) {
      console.error('Failed to submit WFH request:', error)
    }
  }

  const filteredWFHRequests = wfhRequests.filter(wfh =>
    wfh.reason.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (wfh.notes && wfh.notes.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING': return 'bg-yellow-100 text-yellow-800'
      case 'APPROVED': return 'bg-green-100 text-green-800'
      case 'REJECTED': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Work From Home</h1>
            <p className="text-gray-600 mt-2">Request to work from home</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Request WFH
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Work From Home Request</DialogTitle>
                <DialogDescription>
                  Submit a request to work from home
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="wfhDate">WFH Date</Label>
                  <Input
                    id="wfhDate"
                    type="date"
                    value={formData.wfhDate}
                    onChange={(e) => setFormData({ ...formData, wfhDate: e.target.value })}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="reason">Reason</Label>
                  <Textarea
                    id="reason"
                    value={formData.reason}
                    onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                    placeholder="Please provide reason for working from home"
                    rows={3}
                    required
                  />
                </div>

                <div>
                  <Label htmlFor="notes">Additional Notes</Label>
                  <Textarea
                    id="notes"
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    placeholder="Any additional information"
                    rows={2}
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
                  <p className="text-2xl font-bold">{wfhRequests.length}</p>
                </div>
                <Home className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Pending</p>
                  <p className="text-2xl font-bold text-yellow-600">
                    {wfhRequests.filter(w => w.status === 'PENDING').length}
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
                    {wfhRequests.filter(w => w.status === 'APPROVED').length}
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
                    {wfhRequests.filter(w => w.status === 'REJECTED').length}
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
              placeholder="Search WFH requests..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* WFH Requests */}
        <Card>
          <CardHeader>
            <CardTitle>Your WFH Requests</CardTitle>
            <CardDescription>All your submitted work from home requests</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">Loading WFH requests...</div>
            ) : filteredWFHRequests.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                {searchTerm ? 'No WFH requests found matching your search' : 'No WFH requests yet. Submit your first request!'}
              </div>
            ) : (
              <div className="space-y-4">
                {filteredWFHRequests.map((wfh) => (
                  <div key={wfh.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="font-medium text-gray-900">
                            {new Date(wfh.wfh_date).toLocaleDateString()}
                          </h3>
                          <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(wfh.status)}`}>
                            {wfh.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">{wfh.reason}</p>
                        {wfh.notes && (
                          <p className="text-sm text-gray-600 mb-2">{wfh.notes}</p>
                        )}
                        <p className="text-xs text-gray-500">
                          Requested on {new Date(wfh.created_at).toLocaleDateString()}
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