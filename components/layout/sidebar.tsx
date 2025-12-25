'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { signOut, useSession } from 'next-auth/react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  LayoutDashboard,
  FileText,
  Calendar,
  Users,
  Settings,
  LogOut,
  Menu,
  X,
  Clock,
  Home,
  UserCheck
} from 'lucide-react'

interface SidebarProps {
  className?: string
}

export function Sidebar({ className }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const pathname = usePathname()
  const { data: session } = useSession()

  const isAdmin = session?.user?.role === 'ADMIN' || session?.user?.role === 'IT COORDINATOR'

  const userNavItems = [
    {
      title: 'Dashboard',
      href: '/dashboard',
      icon: LayoutDashboard
    },
    {
      title: 'Work Logs',
      href: '/logs',
      icon: FileText
    },
    {
      title: 'Leave Requests',
      href: '/attendance/leave',
      icon: Calendar
    },
    {
      title: 'Comp-Off',
      href: '/attendance/compoff',
      icon: Clock
    },
    {
      title: 'Work From Home',
      href: '/attendance/wfh',
      icon: Home
    }
  ]

  const adminNavItems = [
    {
      title: 'Admin Dashboard',
      href: '/admin/dashboard',
      icon: LayoutDashboard
    },
    {
      title: 'User Management',
      href: '/admin/users',
      icon: Users
    },
    {
      title: 'Leave Management',
      href: '/admin/attendance/leave',
      icon: Calendar
    },
    {
      title: 'Comp-Off Management',
      href: '/admin/attendance/compoff',
      icon: Clock
    },
    {
      title: 'WFH Management',
      href: '/admin/attendance/wfh',
      icon: Home
    },
    {
      title: 'Log Monitoring',
      href: '/admin/logs',
      icon: FileText
    }
  ]

  const navItems = isAdmin ? adminNavItems : userNavItems

  const handleSignOut = () => {
    signOut({ callbackUrl: '/auth/login' })
  }

  return (
    <div className={cn(
      "flex flex-col h-full bg-white border-r border-gray-200",
      isCollapsed ? "w-16" : "w-64",
      className
    )}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        {!isCollapsed && (
          <h1 className="text-xl font-bold text-gray-900">SmartLogX</h1>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="h-8 w-8"
        >
          {isCollapsed ? <Menu className="h-4 w-4" /> : <X className="h-4 w-4" />}
        </Button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          
          return (
            <Link key={item.href} href={item.href}>
              <div className={cn(
                "flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                isActive 
                  ? "bg-primary text-primary-foreground" 
                  : "text-gray-700 hover:bg-gray-100",
                isCollapsed && "justify-center"
              )}>
                <Icon className={cn("h-4 w-4", !isCollapsed && "mr-3")} />
                {!isCollapsed && item.title}
              </div>
            </Link>
          )
        })}
      </nav>

      {/* User Info & Logout */}
      <div className="p-4 border-t border-gray-200">
        {!isCollapsed && session?.user && (
          <div className="mb-3 p-3 bg-gray-50 rounded-lg">
            <p className="text-sm font-medium text-gray-900">{session.user.name}</p>
            <p className="text-xs text-gray-500">{session.user.empId}</p>
            <p className="text-xs text-gray-500">{session.user.role}</p>
          </div>
        )}
        <Button
          variant="ghost"
          onClick={handleSignOut}
          className={cn(
            "w-full justify-start text-gray-700 hover:bg-gray-100",
            isCollapsed && "justify-center"
          )}
        >
          <LogOut className={cn("h-4 w-4", !isCollapsed && "mr-3")} />
          {!isCollapsed && "Sign Out"}
        </Button>
      </div>
    </div>
  )
}