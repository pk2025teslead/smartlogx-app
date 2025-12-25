import NextAuth from 'next-auth'

declare module 'next-auth' {
  interface Session {
    user: {
      id: string
      empId: string
      name: string
      email: string
      role: string
      department: string
      isFirstLogin: boolean
    }
  }

  interface User {
    empId: string
    role: string
    department: string
    isFirstLogin: boolean
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    empId: string
    role: string
    department: string
    isFirstLogin: boolean
  }
}