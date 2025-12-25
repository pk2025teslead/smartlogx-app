'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { FileText, Search, Filter, Download, Eye } from 'lucide-react'
import { useEffect, useState } from 'react'

interface UserLog {
  ID: number
  USER_ID: number
  PROJECT_TITLE: string
  LOG_HEADING: string
  LOG_DETAILS: string
  LOG_DATE: string
  SESSION_TYPE: string
  APPROVAL_REQUIRED: boolean
  APPROVAL_CODE: string | null
  CREATED_AT: string
  EMP_NAME: string
  EMP_ID: string
}

export default function AdminLogsPage() {
  const { data: session } = useSession()
  const [logs, setLogs] = useState<UserLog[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      const response = await fetch('/api/admin/logs')
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

  const filteredLogs = logs.filter(log =>
    log.PROJECT_TITLE.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.LOG_HEADING.toLowerCase().includes(searchTerm.toLowerCase()) ||
    log.EMP_NAME.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Log Monitoring</h1>
            <p className="text-gray-600 mt-2">Monitor and review all user work logs</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </Button>
          </div>
        </div>

        {/* Search and Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
          <div className="lg:col-span-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search logs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          
          <Card className="lg:col-span-1">
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

          <Card className="lg:col-span-1">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">This Month</p>
                  <p className="text-2xl font-bold">{logs.filter(log => {
                    const logDate = new Date(log.LOG_DATE)
                    const now = new Date()
                    return logDate.getMonth() === now.getMonth() && logDate.getFullYear() === now.getFullYear()
                  }).length}</p>
                </div>
                <FileText className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="lg:col-span-1">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">With Approval</p>
                  <p className="text-2xl font-bold">{logs.filter(log => log.APPROVAL_REQUIRED).length}</p>
                </div>
                <FileText className="h-8 w-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Logs Table */}
        <Card>
          <CardHeader>
            <CardTitle>All Work Logs</CardTitle>
            <CardDescription>Complete list of user work logs</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">Loading logs...</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-3">Date</th>
                      <th className="text-left p-3">Employee</th>
                      <th className="text-left p-3">Project</th>
                      <th className="text-left p-3">Heading</th>
                      <th className="text-left p-3">Session</th>
                      <th className="text-left p-3">Status</th>
                      <th className="text-left p-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredLogs.map((log) => (
                      <tr key={log.ID} className="border-b hover:bg-gray-50">
                        <td className="p-3">
                          {new Date(log.LOG_DATE).toLocaleDateString()}
                        </td>
                        <td className="p-3">
                          <div>
                            <div className="font-medium">{log.EMP_NAME}</div>
                            <div className="text-sm text-gray-500">{log.EMP_ID}</div>
                          </div>
                        </td>
                        <td className="p-3">
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                            {log.PROJECT_TITLE}
                          </span>
                        </td>
                        <td className="p-3 max-w-xs truncate">{log.LOG_HEADING}</td>
                        <td className="p-3">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            log.SESSION_TYPE === 'First Half' 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-purple-100 text-purple-800'
                          }`}>
                            {log.SESSION_TYPE}
                          </span>
                        </td>
                        <td className="p-3">
                          {log.APPROVAL_REQUIRED ? (
                            <span className="px-2 py-1 bg-orange-100 text-orange-800 rounded-full text-xs">
                              Approved ({log.APPROVAL_CODE})
                            </span>
                          ) : (
                            <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                              Normal
                            </span>
                          )}
                        </td>
                        <td className="p-3">
                          <Button variant="outline" size="sm">
                            <Eye className="h-4 w-4 mr-1" />
                            View
                          </Button>
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