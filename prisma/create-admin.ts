import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function createAdmin() {
  console.log('🔧 Creating admin user...')

  try {
    // Check if admin already exists
    const existingAdmin = await prisma.user.findFirst({
      where: {
        OR: [
          { email: 'admin@smartlogx.com' },
          { empId: 'ADMIN001' }
        ]
      }
    })

    if (existingAdmin) {
      console.log('✅ Admin user already exists:', existingAdmin.empName)
      return
    }

    // Create admin user
    const adminPassword = await bcrypt.hash('admin123', 12)
    const admin = await prisma.user.create({
      data: {
        empId: 'ADMIN001',
        empName: 'System Administrator',
        email: 'admin@smartlogx.com',
        mobileNumber: '9999999999',
        role: 'ADMIN',
        department: 'IT Operations',
        password: adminPassword,
        isFirstLogin: false,
        isActive: true
      }
    })

    console.log('✅ Created admin user:', admin.empName)
    console.log('📋 Login Credentials:')
    console.log('Email: admin@smartlogx.com')
    console.log('Password: admin123')

  } catch (error) {
    console.error('❌ Failed to create admin user:', error)
    throw error
  }
}

createAdmin()
  .catch((e) => {
    console.error('❌ Script failed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })