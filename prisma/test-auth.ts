import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function testAuth() {
  console.log('🔐 Testing authentication...')

  try {
    // Test admin login
    console.log('\n1. Testing admin@smartlogx.com login...')
    
    const user = await prisma.user.findFirst({
      where: {
        OR: [
          { empId: 'admin@smartlogx.com' },
          { email: 'admin@smartlogx.com' }
        ],
        isActive: true
      }
    })

    if (!user) {
      console.log('❌ User not found')
      return
    }

    console.log(`✅ User found: ${user.empName}`)
    console.log(`   Email: ${user.email}`)
    console.log(`   EmpId: ${user.empId}`)
    console.log(`   Role: ${user.role}`)
    console.log(`   Active: ${user.isActive}`)

    const isPasswordValid = await bcrypt.compare('admin123', user.password)
    console.log(`   Password valid: ${isPasswordValid}`)

    if (isPasswordValid) {
      console.log('✅ Authentication should work!')
      console.log('\n📋 Login Details:')
      console.log('URL: https://smartlogx-app.vercel.app/auth/login')
      console.log('Email: admin@smartlogx.com')
      console.log('Password: admin123')
    } else {
      console.log('❌ Password validation failed')
    }

    // Test other users
    console.log('\n2. Testing other users...')
    const otherUsers = await prisma.user.findMany({
      where: {
        email: { not: 'admin@smartlogx.com' }
      },
      take: 3
    })

    for (const testUser of otherUsers) {
      const testPassword = await bcrypt.compare('Temp@123', testUser.password)
      console.log(`${testUser.email} - Password 'Temp@123' valid: ${testPassword}`)
    }

  } catch (error) {
    console.error('❌ Error:', error)
    throw error
  }
}

testAuth()
  .catch((e) => {
    console.error('❌ Script failed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })