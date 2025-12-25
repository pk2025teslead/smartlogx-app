'use client'

import { useSession } from 'next-auth/react'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Calendar, Clock, FileText, Home, Plus } from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  const { data: session } = useSession()

  const quickActions = [
    {
      title: 'Add Work Log',
      description: 'Log your daily work activities',
      href: '/logs/add',
      icon: FileText,
      color: 'bg-blue-500'
    },
    {
      title: 'Request Leave',
      description: 'Submit a new leave request',
      href: '/attendance/leave/add',
      icon: Calendar,
      color: 'bg-green-500'
    },
    {
      title: 'Comp-Off Request',
      description: 'Request comp-off for Sunday work',
      href: '/attendance/compoff/add',
      icon: Clock,
      color: 'bg-orange-500'
    },
    {
      title: 'WFH Request',
      description: 'Request work from home',
      href: '/attendance/wfh/add',
      icon: Home,
      color: 'bg-purple-500'
    }
  ]

  const stats = [
    {
      title: 'Total Logs',
      value: '0',
      description: 'This month',
      icon: FileText
    },
    {
      title: 'Pending Leaves',
      value: '0',
      description: 'Awaiting approval',
      icon: Calendar
    },
    {
      title: 'Comp-Off Balance',
      value: '0',
      description: 'Available days',
      icon: Clock
    },
    {
      title: 'WFH Requests',
      value: '0',
      description: 'This month',
      icon: Home
    }
  ]

  return (
    <DashboardLayout>
      <div className="p-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {session?.user?.name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Here's what's happening with your work today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat) => {
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
              <CardTitle>Recent Work Logs</CardTitle>
              <CardDescription>Your latest work activities</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-gray-500">
                <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No work logs yet</p>
                <Link href="/logs/add">
                  <Button className="mt-4">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Your First Log
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Upcoming Leaves</CardTitle>
              <CardDescription>Your scheduled time off</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-gray-500">
                <Calendar className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No upcoming leaves</p>
                <Link href="/attendance/leave/add">
                  <Button className="mt-4">
                    <Plus className="h-4 w-4 mr-2" />
                    Request Leave
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