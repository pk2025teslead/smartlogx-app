import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import bcrypt from 'bcryptjs'
import { prisma } from './db'
import { verifyDjangoPassword } from './django-auth'

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

        // Try to find user by empId or email using raw SQL for MySQL
        const users = await prisma.$queryRaw`
          SELECT ID, EMP_ID, EMP_NAME, EMAIL, ROLE, ROLL, PASSWORD, IS_FIRST_LOGIN
          FROM users_master 
          WHERE (EMP_ID = ${credentials.username} OR EMAIL = ${credentials.username})
          AND ID IS NOT NULL
        `

        if (!Array.isArray(users) || users.length === 0) {
          return null
        }

        const user = users[0] as any

        // Verify password using Django PBKDF2 format
        const isPasswordValid = verifyDjangoPassword(credentials.password, user.PASSWORD)

        if (!isPasswordValid) {
          return null
        }

        return {
          id: user.ID.toString(),
          empId: user.EMP_ID,
          name: user.EMP_NAME,
          email: user.EMAIL,
          role: user.ROLE,
          department: user.ROLL || '',
          isFirstLogin: Boolean(user.IS_FIRST_LOGIN)
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