'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Calendar, 
  FileText, 
  Clock, 
  Home, 
  TrendingUp, 
  CheckCircle, 
  AlertCircle,
  Plus
} from 'lucide-react'
import { useEffect, useState } from 'react'
import Link from 'next/link'

interface DashboardStats {
  totalLogs: number
  pendingLeaves: number
  approvedLeaves: number
  pendingCompOffs: number
  pendingWFH: number
  thisMonthLogs: number
}

export default function UserDashboardPage() {
  const { data: session } = useSession()
  const [stats, setStats] = useState<DashboardStats>({
    totalLogs: 0,
    pendingLeaves: 0,
    approvedLeaves: 0,
    pendingCompOffs: 0,
    pendingWFH: 0,
    thisMonthLogs: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('/api/user/dashboard/stats')
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const quickActions = [
    {
      title: 'Add Work Log',
      description: 'Log your daily work activities',
      icon: FileText,
      href: '/logs',
      color: 'bg-blue-500'
    },
    {
      title: 'Request Leave',
      description: 'Submit a new leave request',
      icon: Calendar,
      href: '/attendance/leave',
      color: 'bg-green-500'
    },
    {
      title: 'Comp-Off Request',
      description: 'Request comp-off for weekend work',
      icon: Clock,
      href: '/attendance/compoff',
      color: 'bg-purple-500'
    },
    {
      title: 'Work From Home',
      description: 'Request to work from home',
      icon: Home,
      href: '/attendance/wfh',
      color: 'bg-orange-500'
    }
  ]

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {session?.user?.name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Here's what's happening with your work activities
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Work Logs</p>
                  <p className="text-2xl font-bold">{stats.totalLogs}</p>
                </div>
                <FileText className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">This Month Logs</p>
                  <p className="text-2xl font-bold">{stats.thisMonthLogs}</p>
                </div>
                <TrendingUp className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Approved Leaves</p>
                  <p className="text-2xl font-bold text-green-600">{stats.approvedLeaves}</p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Pending Requests</p>
                  <p className="text-2xl font-bold text-yellow-600">
                    {stats.pendingLeaves + stats.pendingCompOffs + stats.pendingWFH}
                  </p>
                </div>
                <AlertCircle className="h-8 w-8 text-yellow-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action) => {
              const Icon = action.icon
              return (
                <Link key={action.href} href={action.href}>
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-3">
                        <div className={`w-10 h-10 rounded-lg ${action.color} flex items-center justify-center`}>
                          <Icon className="h-5 w-5 text-white" />
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900">{action.title}</h3>
                          <p className="text-sm text-gray-500">{action.description}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              )
            })}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pending Requests */}
          <Card>
            <CardHeader>
              <CardTitle>Pending Requests</CardTitle>
              <CardDescription>Your requests awaiting approval</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {stats.pendingLeaves > 0 && (
                  <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <Calendar className="h-5 w-5 text-yellow-600" />
                      <span className="text-sm font-medium">Leave Requests</span>
                    </div>
                    <span className="text-sm text-yellow-600">{stats.pendingLeaves} pending</span>
                  </div>
                )}
                
                {stats.pendingCompOffs > 0 && (
                  <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <Clock className="h-5 w-5 text-purple-600" />
                      <span className="text-sm font-medium">Comp-Off Requests</span>
                    </div>
                    <span className="text-sm text-purple-600">{stats.pendingCompOffs} pending</span>
                  </div>
                )}
                
                {stats.pendingWFH > 0 && (
                  <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <Home className="h-5 w-5 text-orange-600" />
                      <span className="text-sm font-medium">WFH Requests</span>
                    </div>
                    <span className="text-sm text-orange-600">{stats.pendingWFH} pending</span>
                  </div>
                )}
                
                {(stats.pendingLeaves + stats.pendingCompOffs + stats.pendingWFH) === 0 && (
                  <div className="text-center py-4 text-gray-500">
                    No pending requests
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle>This Month Summary</CardTitle>
              <CardDescription>Your activity summary for this month</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Work Logs Submitted</span>
                  <span className="font-medium">{stats.thisMonthLogs}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Leaves Approved</span>
                  <span className="font-medium text-green-600">{stats.approvedLeaves}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Attendance Rate</span>
                  <span className="font-medium text-blue-600">
                    {stats.thisMonthLogs > 0 ? '95%' : '0%'}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}