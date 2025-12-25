import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 Starting database seed...')

  // Create admin user
  const adminPassword = await bcrypt.hash('admin123', 12)
  const admin = await prisma.user.upsert({
    where: { empId: 'ADMIN001' },
    update: {},
    create: {
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

  // Create sample users
  const sampleUsers = [
    {
      empId: 'EMP001',
      empName: 'John Developer',
      email: 'john.dev@smartlogx.com',
      mobileNumber: '9876543210',
      role: 'SOFTWARE DEVELOPER',
      department: 'Backend Team'
    },
    {
      empId: 'EMP002',
      empName: 'Jane Tester',
      email: 'jane.test@smartlogx.com',
      mobileNumber: '9876543211',
      role: 'SOFTWARE TESTER',
      department: 'QA Team'
    },
    {
      empId: 'EMP003',
      empName: 'Mike Designer',
      email: 'mike.design@smartlogx.com',
      mobileNumber: '9876543212',
      role: 'UI UX DESIGNER',
      department: 'Design Team'
    },
    {
      empId: 'EMP004',
      empName: 'Sarah Coordinator',
      email: 'sarah.coord@smartlogx.com',
      mobileNumber: '9876543213',
      role: 'IT COORDINATOR',
      department: 'IT Operations'
    }
  ]

  const defaultPassword = await bcrypt.hash('Temp@123', 12)

  for (const userData of sampleUsers) {
    const user = await prisma.user.upsert({
      where: { empId: userData.empId },
      update: {},
      create: {
        ...userData,
        password: defaultPassword,
        isFirstLogin: true,
        isActive: true
      }
    })
    console.log('✅ Created user:', user.empName)
  }

  // Create sample projects
  const sampleProjects = [
    {
      projectName: 'SmartLogX Development',
      projectCode: 'SLX001',
      description: 'Employee management system development'
    },
    {
      projectName: 'Client Portal',
      projectCode: 'CP001',
      description: 'Customer facing portal application'
    },
    {
      projectName: 'Mobile App',
      projectCode: 'MA001',
      description: 'Mobile application for employees'
    },
    {
      projectName: 'Data Analytics',
      projectCode: 'DA001',
      description: 'Business intelligence and analytics platform'
    }
  ]

  for (const projectData of sampleProjects) {
    const project = await prisma.project.upsert({
      where: { projectCode: projectData.projectCode },
      update: {},
      create: projectData
    })
    console.log('✅ Created project:', project.projectName)
  }

  console.log('🎉 Database seed completed successfully!')
  console.log('\n📋 Login Credentials:')
  console.log('Admin: admin@smartlogx.com / admin123')
  console.log('Users: [empId]@smartlogx.com / Temp@123')
  console.log('Example: john.dev@smartlogx.com / Temp@123')
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })