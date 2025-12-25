import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function checkAdmin() {
  console.log('🔍 Checking admin users...')

  try {
    // Find all admin users
    const adminUsers = await prisma.user.findMany({
      where: {
        OR: [
          { role: 'ADMIN' },
          { role: 'IT COORDINATOR' },
          { email: { contains: 'admin' } }
        ]
      }
    })

    console.log('👥 Found admin users:')
    for (const user of adminUsers) {
      console.log(`- ${user.empName} (${user.empId})`)
      console.log(`  Email: ${user.email}`)
      console.log(`  Role: ${user.role}`)
      console.log(`  Active: ${user.isActive}`)
      console.log(`  First Login: ${user.isFirstLogin}`)
      console.log('---')
    }

    // Check if we can find the specific admin
    const specificAdmin = await prisma.user.findUnique({
      where: { email: 'admin@smartlogx.com' }
    })

    if (specificAdmin) {
      console.log('✅ Found admin@smartlogx.com:')
      console.log(`Name: ${specificAdmin.empName}`)
      console.log(`EmpId: ${specificAdmin.empId}`)
      console.log(`Active: ${specificAdmin.isActive}`)
      
      // Test password
      const isPasswordValid = await bcrypt.compare('admin123', specificAdmin.password)
      console.log(`Password 'admin123' valid: ${isPasswordValid}`)
    } else {
      console.log('❌ admin@smartlogx.com not found')
      
      // Create the admin user
      console.log('🔧 Creating admin@smartlogx.com...')
      const adminPassword = await bcrypt.hash('admin123', 12)
      const newAdmin = await prisma.user.create({
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
      console.log('✅ Created admin user:', newAdmin.empName)
    }

  } catch (error) {
    console.error('❌ Error:', error)
    throw error
  }
}

checkAdmin()
  .catch((e) => {
    console.error('❌ Script failed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })