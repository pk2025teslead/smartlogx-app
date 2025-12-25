import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import bcrypt from 'bcryptjs'
import { prisma } from './db'

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        username: { label: 'Username', type: 'text' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) {
          return null
        }

        // Try to find user by empId or email
        const user = await prisma.user.findFirst({
          where: {
            OR: [
              { empId: credentials.username },
              { email: credentials.username }
            ],
            isActive: true
          }
        })

        if (!user) {
          return null
        }

        const isPasswordValid = await bcrypt.compare(credentials.password, user.password)

        if (!isPasswordValid) {
          return null
        }

        return {
          id: user.id,
          empId: user.empId,
          name: user.empName,
          email: user.email,
          role: user.role,
          department: user.department || '',
          isFirstLogin: user.isFirstLogin
        }
      }
    })
  ],
  session: {
    strategy: 'jwt'
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.empId = user.empId
        token.role = user.role
        token.department = user.department
        token.isFirstLogin = user.isFirstLogin
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.sub!
        session.user.empId = token.empId as string
        session.user.role = token.role as string
        session.user.department = token.department as string
        session.user.isFirstLogin = token.isFirstLogin as boolean
      }
      return session
    }
  },
  pages: {
    signIn: '/auth/login'
  }
}