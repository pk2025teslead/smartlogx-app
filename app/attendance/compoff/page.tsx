'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Checkbox } from '@/components/ui/checkbox'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Clock, Plus, Search, Calendar, Check, X } from 'lucide-react'
import { useEffect, useState } from 'react'

interface CompOffRequest {
  id: string
  sunday_date: string
  work_purpose: string
  compoff_date: string | null
  no_compoff: boolean
  notes: string | null
  status: string
  created_at: string
}

export default function UserCompOffPage() {
  const { data: session } = useSession()
  const [compOffs, setCompOffs] = useState<CompOffRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)

  // Form state
  const [formData, setFormData] = useState({
    sundayDate: '',
    workPurpose: '',
    compOffDate: '',
    noCompOff: false,
    notes: ''
  })

  useEffect(() => {
    fetchCompOffs()
  }, [])

  const fetchCompOffs = async () => {
    try {
      const response = await fetch('/api/user/attendance/compoff')
      if (response.ok) {
        const data = await response.json()
        setCompOffs(data)
      }
    } catch (error) {
      console.error('Failed to fetch comp-offs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const response = await fetch('/api/user/attendance/compoff', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        fetchCompOffs()
        setIsDialogOpen(false)
        setFormData({
          sundayDate: '',
          workPurpose: '',
          compOffDate: '',
          noCompOff: false,
          notes: ''
        })
      }
    } catch (error) {
      console.error('Failed to submit comp-off request:', error)
    }
  }

  const filteredCompOffs = compOffs.filter(compOff =>
    compOff.work_purpose.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (compOff.notes && compOff.notes.toLowerCase().includes(searchTerm.toLowerCase()))
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
            <h1 className="text-3xl font-bold text-gray-900">Comp-Off Requests</h1>
            <p className="text-gray-600 mt-2">Request comp-off for weekend work</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Request Comp-Off
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Request Comp-Off</DialogTitle>
                <DialogDescription>
                  Submit a comp-off request for weekend work
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="sundayDate">Sunday Worked</Label>
                  <Input
                    id="sundayDate"
                    type="date"
                    value={formData.sundayDate}
                    onChange={(e) => setFormData({ ...formData, sundayDate: e.target.value })}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="workPurpose">Work Purpose</Label>
                  <Textarea
                    id="workPurpose"
                    value={formData.workPurpose}
                    onChange={(e) => setFormData({ ...formData, workPurpose: e.target.value })}
                    placeholder="Describe the work done on Sunday"
                    rows={3}
                    required
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="noCompOff"
                    checked={formData.noCompOff}
                    onCheckedChange={(checked) => setFormData({ ...formData, noCompOff: checked as boolean })}
                  />
                  <Label htmlFor="noCompOff">I don't want comp-off for this work</Label>
                </div>

                {!formData.noCompOff && (
                  <div>
                    <Label htmlFor="compOffDate">Preferred Comp-Off Date</Label>
                    <Input
                      id="compOffDate"
                      type="date"
                      value={formData.compOffDate}
                      onChange={(e) => setFormData({ ...formData, compOffDate: e.target.value })}
                    />
                  </div>
                )}

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
                  <p className="text-2xl font-bold">{compOffs.length}</p>
                </div>
                <Clock className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Pending</p>
                  <p className="text-2xl font-bold text-yellow-600">
                    {compOffs.filter(c => c.status === 'PENDING').length}
                  </p>
                </div>
                <Calendar className="h-8 w-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Approved</p>
                  <p className="text-2xl font-bold text-green-600">
                    {compOffs.filter(c => c.status === 'APPROVED').length}
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
                    {compOffs.filter(c => c.status === 'REJECTED').length}
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
              placeholder="Search comp-off requests..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Comp-Off Requests */}
        <Card>
          <CardHeader>
            <CardTitle>Your Comp-Off Requests</CardTitle>
            <CardDescription>All your submitted comp-off requests</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">Loading comp-off requests...</div>
            ) : filteredCompOffs.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                {searchTerm ? 'No comp-off requests found matching your search' : 'No comp-off requests yet. Submit your first request!'}
              </div>
            ) : (
              <div className="space-y-4">
                {filteredCompOffs.map((compOff) => (
                  <div key={compOff.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="font-medium text-gray-900">
                            Sunday: {new Date(compOff.sunday_date).toLocaleDateString()}
                          </h3>
                          <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(compOff.status)}`}>
                            {compOff.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-700 mb-2">{compOff.work_purpose}</p>
                        {compOff.no_compoff ? (
                          <p className="text-sm text-gray-500 mb-2">No comp-off requested</p>
                        ) : compOff.compoff_date ? (
                          <p className="text-sm text-gray-500 mb-2">
                            Comp-off date: {new Date(compOff.compoff_date).toLocaleDateString()}
                          </p>
                        ) : (
                          <p className="text-sm text-gray-500 mb-2">Comp-off date not specified</p>
                        )}
                        {compOff.notes && (
                          <p className="text-sm text-gray-600 mb-2">{compOff.notes}</p>
                        )}
                        <p className="text-xs text-gray-500">
                          Requested on {new Date(compOff.created_at).toLocaleDateString()}
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