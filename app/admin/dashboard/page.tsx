'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Users, FileText, Calendar, Clock, Home, Plus, TrendingUp } from 'lucide-react'
import Link from 'next/link'
import { useEffect, useState } from 'react'

export default function AdminDashboardPage() {
  const { data: session } = useSession()
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalLogs: 0,
    pendingLeaves: 0,
    pendingCompOffs: 0,
    pendingWFH: 0
  })

  useEffect(() => {
    // Fetch admin statistics
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/admin/stats')
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }

  const quickActions = [
    {
      title: 'Manage Users',
      description: 'Add, edit, or manage user accounts',
      href: '/admin/users',
      icon: Users,
      color: 'bg-blue-500'
    },
    {
      title: 'Review Logs',
      description: 'Monitor user work logs and activities',
      href: '/admin/logs',
      icon: FileText,
      color: 'bg-green-500'
    },
    {
      title: 'Leave Requests',
      description: 'Approve or reject leave requests',
      href: '/admin/attendance/leave',
      icon: Calendar,
      color: 'bg-orange-500'
    },
    {
      title: 'Comp-Off Requests',
      description: 'Manage Sunday work comp-off requests',
      href: '/admin/attendance/compoff',
      icon: Clock,
      color: 'bg-purple-500'
    }
  ]

  const dashboardStats = [
    {
      title: 'Total Users',
      value: stats.totalUsers.toString(),
      description: 'Active employees',
      icon: Users,
      trend: '+2 this month'
    },
    {
      title: 'Work Logs',
      value: stats.totalLogs.toString(),
      description: 'This month',
      icon: FileText,
      trend: '+12% from last month'
    },
    {
      title: 'Pending Leaves',
      value: stats.pendingLeaves.toString(),
      description: 'Awaiting approval',
      icon: Calendar,
      trend: '3 urgent'
    },
    {
      title: 'Pending Requests',
      value: (stats.pendingCompOffs + stats.pendingWFH).toString(),
      description: 'Comp-off & WFH',
      icon: Clock,
      trend: '2 new today'
    }
  ]

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Admin Dashboard
          </h1>
          <p className="text-gray-600 mt-2">
            Welcome back, {session?.user?.name}! Here's your system overview.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {dashboardStats.map((stat) => {
            const Icon = stat.icon
            return (
              <Card key={stat.title}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {stat.title}
                  </CardTitle>
                  <Icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className="text-xs text-muted-foreground">
                    {stat.description}
                  </p>
                  <div className="flex items-center mt-2">
                    <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                    <span className="text-xs text-green-500">{stat.trend}</span>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action) => {
              const Icon = action.icon
              return (
                <Link key={action.title} href={action.href}>
                  <Card className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardHeader>
                      <div className={`w-12 h-12 rounded-lg ${action.color} flex items-center justify-center mb-3`}>
                        <Icon className="h-6 w-6 text-white" />
                      </div>
                      <CardTitle className="text-lg">{action.title}</CardTitle>
                      <CardDescription>{action.description}</CardDescription>
                    </CardHeader>
                  </Card>
                </Link>
              )
            })}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Leave Requests</CardTitle>
              <CardDescription>Latest leave requests requiring attention</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-gray-500">
                <Calendar className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No pending leave requests</p>
                <Link href="/admin/attendance/leave">
                  <Button className="mt-4" variant="outline">
                    View All Requests
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>System Activity</CardTitle>
              <CardDescription>Recent user activities and logs</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-gray-500">
                <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Loading recent activities...</p>
                <Link href="/admin/logs">
                  <Button className="mt-4" variant="outline">
                    View All Logs
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}