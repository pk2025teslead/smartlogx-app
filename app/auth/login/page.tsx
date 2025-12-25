'use client'

import { useState, useEffect } from 'react'
import { signIn, getSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, Building2, Users, BarChart3, Shield, Zap, Globe } from 'lucide-react'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentFeature, setCurrentFeature] = useState(0)
  const router = useRouter()

  const features = [
    {
      icon: Users,
      title: "Team Management",
      description: "Manage your team efficiently with role-based access control"
    },
    {
      icon: BarChart3,
      title: "Analytics & Reports",
      description: "Get insights with comprehensive reporting and analytics"
    },
    {
      icon: Shield,
      title: "Secure & Reliable",
      description: "Enterprise-grade security with data protection"
    },
    {
      icon: Zap,
      title: "Fast & Efficient",
      description: "Lightning-fast performance for better productivity"
    }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % features.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const result = await signIn('credentials', {
        username,
        password,
        redirect: false
      })

      if (result?.error) {
        setError('Invalid credentials. Please check your Employee ID/Email and password.')
      } else {
        const session = await getSession()
        if (session?.user) {
          if (session.user.role === 'ADMIN' || session.user.role === 'IT COORDINATOR') {
            router.push('/admin/dashboard')
          } else {
            router.push('/dashboard')
          }
        }
      }
    } catch (error) {
      setError('An error occurred. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex">
      {/* Left Side - Features Showcase */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 p-12 flex-col justify-center relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-32 h-32 bg-white rounded-full animate-pulse"></div>
          <div className="absolute bottom-32 right-16 w-24 h-24 bg-white rounded-full animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/3 w-16 h-16 bg-white rounded-full animate-pulse delay-2000"></div>
        </div>

        <div className="relative z-10">
          {/* Logo and Title */}
          <div className="mb-12">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center mr-4">
                <Building2 className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">SmartLogX</h1>
                <p className="text-blue-100">Employee Management System</p>
              </div>
            </div>
          </div>

          {/* Animated Features */}
          <div className="space-y-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div
                  key={index}
                  className={`transform transition-all duration-500 ${
                    index === currentFeature
                      ? 'translate-x-0 opacity-100 scale-105'
                      : 'translate-x-4 opacity-60 scale-95'
                  }`}
                >
                  <div className="flex items-start space-x-4">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center transition-colors duration-300 ${
                      index === currentFeature ? 'bg-white text-blue-600' : 'bg-blue-500 text-white'
                    }`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                      <p className="text-blue-100 leading-relaxed">{feature.description}</p>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Stats */}
          <div className="mt-12 grid grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-white">500+</div>
              <div className="text-blue-100 text-sm">Companies</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white">10K+</div>
              <div className="text-blue-100 text-sm">Users</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white">99.9%</div>
              <div className="text-blue-100 text-sm">Uptime</div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          {/* Mobile Logo */}
          <div className="lg:hidden text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl mb-4">
              <Building2 className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">SmartLogX</h1>
            <p className="text-gray-600">Employee Management System</p>
          </div>

          <Card className="shadow-2xl border-0 bg-white/80 backdrop-blur-sm">
            <CardContent className="p-8">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome Back!</h2>
                <p className="text-gray-600">Sign in to your account to continue</p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="username" className="text-sm font-medium text-gray-700">
                    Employee ID or Email
                  </Label>
                  <Input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter your Employee ID or Email"
                    required
                    disabled={isLoading}
                    className="h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password" className="text-sm font-medium text-gray-700">
                    Password
                  </Label>
                  <Input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    required
                    disabled={isLoading}
                    className="h-12 border-gray-200 focus:border-blue-500 focus:ring-blue-500 transition-colors"
                  />
                </div>

                {error && (
                  <Alert variant="destructive" className="animate-shake">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <Button 
                  type="submit" 
                  className="w-full h-12 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium rounded-lg transition-all duration-200 transform hover:scale-105" 
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Signing In...
                    </>
                  ) : (
                    <>
                      <Globe className="mr-2 h-4 w-4" />
                      Sign In
                    </>
                  )}
                </Button>
              </form>

              <div className="mt-8 text-center">
                <p className="text-sm text-gray-600">
                  Need help? Contact your system administrator
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Demo Credentials */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h4 className="font-medium text-blue-900 mb-2">Demo Credentials:</h4>
            <div className="text-sm text-blue-700 space-y-1">
              <div><strong>Admin:</strong> admin@smartlogx.com / admin123</div>
              <div><strong>User:</strong> john.dev@smartlogx.com / Temp@123</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}