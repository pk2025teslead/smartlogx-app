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
import { FileText, Plus, Search, Calendar, Edit, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'

interface WorkLog {
  id: string
  project_title: string
  log_heading: string
  log_details: string
  log_date: string
  session_type: string
  created_at: string
}

export default function WorkLogsPage() {
  const { data: session } = useSession()
  const [logs, setLogs] = useState<WorkLog[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingLog, setEditingLog] = useState<WorkLog | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    projectTitle: '',
    logHeading: '',
    logDetails: '',
    logDate: new Date().toISOString().split('T')[0],
    sessionType: 'FIRST_HALF'
  })

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      const response = await fetch('/api/user/logs')
      if (response.ok) {
        const data = await response.json()
        setLogs(data)
      }
    } catch (error) {
      console.error('Failed to fetch logs:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const url = editingLog ? `/api/user/logs/${editingLog.id}` : '/api/user/logs'
      const method = editingLog ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        fetchLogs()
        setIsDialogOpen(false)
        setEditingLog(null)
        setFormData({
          projectTitle: '',
          logHeading: '',
          logDetails: '',
          logDate: new Date().toISOString().split('T')[0],
          sessionType: 'FIRST_HALF'
        })
      }
    } catch (error) {
      console.error('Failed to save log:', error)
    }
  }

  const handleEdit = (log: WorkLog) => {
    setEditingLog(log)
    setFormData({
      projectTitle: log.project_title,
      logHeading: log.log_heading,
      logDetails: log.log_details,
      logDate: log.log_date.split('T')[0],
      sessionType: log.session_type
    })
    setIsDialogOpen(true)
  }

  const handleDelete = async (logId: string) => {
    if (!confirm('Are you sure you want to delete this log?')) return
    
    try {
      const response = await fetch(`/api/user/logs/${logId}`, {
        method: 'DELETE',
      })

      if (response.ok) {
        fetchLogs()
      }
    } catch (error) {
      console.error('Failed to delete log:', error)
    }
  }

  const filteredLogs = logs.filter(log =>
    log.project_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.log_heading.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.log_details.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getSessionTypeColor = (type: string) => {
    return type === 'FIRST_HALF' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
  }

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Work Logs</h1>
            <p className="text-gray-600 mt-2">Track your daily work activities and projects</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => {
                setEditingLog(null)
                setFormData({
                  projectTitle: '',
                  logHeading: '',
                  logDetails: '',
                  logDate: new Date().toISOString().split('T')[0],
                  sessionType: 'FIRST_HALF'
                })
              }}>
                <Plus className="h-4 w-4 mr-2" />
                Add Work Log
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>{editingLog ? 'Edit Work Log' : 'Add New Work Log'}</DialogTitle>
                <DialogDescription>
                  {editingLog ? 'Update your work log details' : 'Record your daily work activities'}
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="projectTitle">Project Title</Label>
                    <Input
                      id="projectTitle"
                      value={formData.projectTitle}
                      onChange={(e) => setFormData({ ...formData, projectTitle: e.target.value })}
                      placeholder="Enter project name"
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="sessionType">Session</Label>
                    <Select value={formData.sessionType} onValueChange={(value) => setFormData({ ...formData, sessionType: value })}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="FIRST_HALF">First Half</SelectItem>
                        <SelectItem value="SECOND_HALF">Second Half</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="logHeading">Log Heading</Label>
                    <Input
                      id="logHeading"
                      value={formData.logHeading}
                      onChange={(e) => setFormData({ ...formData, logHeading: e.target.value })}
                      placeholder="Brief description of work"
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="logDate">Date</Label>
                    <Input
                      id="logDate"
                      type="date"
                      value={formData.logDate}
                      onChange={(e) => setFormData({ ...formData, logDate: e.target.value })}
                      required
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="logDetails">Work Details</Label>
                  <Textarea
                    id="logDetails"
                    value={formData.logDetails}
                    onChange={(e) => setFormData({ ...formData, logDetails: e.target.value })}
                    placeholder="Detailed description of work completed"
                    rows={4}
                    required
                  />
                </div>

                <div className="flex justify-end space-x-2">
                  <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                    Cancel
                  </Button>
                  <Button type="submit">
                    {editingLog ? 'Update Log' : 'Save Log'}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Logs</p>
                  <p className="text-2xl font-bold">{logs.length}</p>
                </div>
                <FileText className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">This Month</p>
                  <p className="text-2xl font-bold">
                    {logs.filter(log => new Date(log.log_date).getMonth() === new Date().getMonth()).length}
                  </p>
                </div>
                <Calendar className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">This Week</p>
                  <p className="text-2xl font-bold">
                    {logs.filter(log => {
                      const logDate = new Date(log.log_date)
                      const today = new Date()
                      const weekStart = new Date(today.setDate(today.getDate() - today.getDay()))
                      return logDate >= weekStart
                    }).length}
                  </p>
                </div>
                <FileText className="h-8 w-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search work logs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Work Logs */}
        <Card>
          <CardHeader>
            <CardTitle>Your Work Logs</CardTitle>
            <CardDescription>All your recorded work activities</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">Loading work logs...</div>
            ) : filteredLogs.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                {searchTerm ? 'No logs found matching your search' : 'No work logs yet. Add your first log!'}
              </div>
            ) : (
              <div className="space-y-4">
                {filteredLogs.map((log) => (
                  <div key={log.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="font-medium text-gray-900">{log.log_heading}</h3>
                          <span className={`px-2 py-1 rounded-full text-xs ${getSessionTypeColor(log.session_type)}`}>
                            {log.session_type.replace('_', ' ')}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{log.project_title}</p>
                        <p className="text-sm text-gray-700">{log.log_details}</p>
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        <span className="text-sm text-gray-500">
                          {new Date(log.log_date).toLocaleDateString()}
                        </span>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleEdit(log)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleDelete(log.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
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