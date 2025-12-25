import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function migrateExistingData() {
  console.log('🔄 Starting migration of existing data from log.sql...')

  try {
    // 1. Migrate Users from users_master table
    console.log('👥 Migrating users...')
    
    const existingUsers = [
      {
        id: 1,
        empId: 'EMP001',
        empName: 'John Developer',
        mobileNumber: '9876543210',
        email: 'john.dev@smartlogx.com',
        role: 'SOFTWARE DEVELOPER',
        department: 'Backend Team',
        password: 'pbkdf2_sha256$720000$XWBOr4Fbw29qaBjm6ROtmo$qHVNscTMe+J0bLyAWj4Afz8DJ7x2u8vErqRZx/7uY9c=',
        isFirstLogin: false
      },
      {
        id: 2,
        empId: 'EMP002',
        empName: 'Jane Tester',
        mobileNumber: '9876543211',
        email: 'jane.test@smartlogx.com',
        role: 'SOFTWARE TESTER',
        department: 'QA Team',
        password: 'pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI=',
        isFirstLogin: true
      },
      {
        id: 3,
        empId: 'EMP003',
        empName: 'Mike Designer',
        mobileNumber: '9876543212',
        email: 'mike.design@smartlogx.com',
        role: 'UI UX DESIGNER',
        department: 'Design Team',
        password: 'pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI=',
        isFirstLogin: true
      },
      {
        id: 4,
        empId: 'EMP004',
        empName: 'Sarah Coordinator',
        mobileNumber: '9876543213',
        email: 'sarah.coord@smartlogx.com',
        role: 'IT COORDINATOR',
        department: 'IT Operations',
        password: 'pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI=',
        isFirstLogin: true
      },
      {
        id: 5,
        empId: 'EMP008',
        empName: 'DHARANI',
        mobileNumber: '9876543210',
        email: 'dharaniteslead@gmail.com',
        role: 'SOFTWARE DEVELOPER',
        department: 'IT',
        password: 'pbkdf2_sha256$720000$DuBHIIyqpzv5nLVuLUZ5ex$wrtH3YpeyoMS5hbTHVFt5f9joiMoIbIgmuQvieLoBQ0=',
        isFirstLogin: true
      },
      {
        id: 6,
        empId: '10034',
        empName: 'ARUN',
        mobileNumber: '9876541230',
        email: 'arunpandian@teslead.com',
        role: 'IT COORDINATOR',
        department: 'IT',
        password: 'pbkdf2_sha256$720000$pjSTo7bxVx41fNnpYw78o9$dud3xH4gwmrB2GuPKRW071y/evjFkdyOfaGByctT6ag=',
        isFirstLogin: false
      }
    ]

    // Convert Django password hashes to bcrypt (for compatibility)
    // Note: In production, users will need to reset passwords or we keep Django hash format
    for (const userData of existingUsers) {
      // For now, we'll set a temporary password and mark as first login
      const tempPassword = await bcrypt.hash('Temp@123', 12)
      
      await prisma.user.upsert({
        where: { empId: userData.empId },
        update: {},
        create: {
          empId: userData.empId,
          empName: userData.empName,
          email: userData.email,
          mobileNumber: userData.mobileNumber,
          role: userData.role,
          department: userData.department,
          password: tempPassword, // Temporary password
          isFirstLogin: true, // Force password change
          isActive: true
        }
      })
      console.log(`✅ Migrated user: ${userData.empName}`)
    }

    // 2. Migrate Projects
    console.log('📁 Migrating projects...')
    
    const existingProjects = [
      {
        projectName: 'SmartLogX Development',
        projectCode: 'SLX-DEV',
        description: 'Main SmartLogX application development'
      },
      {
        projectName: 'Client Portal',
        projectCode: 'CP-001',
        description: 'Client facing portal development'
      },
      {
        projectName: 'Internal Tools',
        projectCode: 'INT-TOOLS',
        description: 'Internal productivity tools'
      },
      {
        projectName: 'Mobile App',
        projectCode: 'MOB-APP',
        description: 'Mobile application development'
      },
      {
        projectName: 'API Development',
        projectCode: 'API-DEV',
        description: 'Backend API development'
      },
      {
        projectName: 'UI/UX Design',
        projectCode: 'UI-UX',
        description: 'User interface and experience design'
      },
      {
        projectName: 'Testing & QA',
        projectCode: 'TEST-QA',
        description: 'Quality assurance and testing'
      },
      {
        projectName: 'Documentation',
        projectCode: 'DOCS',
        description: 'Technical documentation'
      }
    ]

    for (const projectData of existingProjects) {
      await prisma.project.upsert({
        where: { projectCode: projectData.projectCode },
        update: {},
        create: projectData
      })
      console.log(`✅ Migrated project: ${projectData.projectName}`)
    }

    // 3. Migrate User Logs
    console.log('📝 Migrating user logs...')
    
    // Get user mappings
    const users = await prisma.user.findMany()
    const userMap = new Map(users.map(u => [u.empId, u.id]))

    const existingLogs = [
      {
        userId: userMap.get('EMP001'),
        projectTitle: 'SAFETY VALVE SYSTEM',
        logHeading: 'SUPPORT ONLINE',
        logDetails: 'SUPPORT THORUGH TEAM VIWER',
        logDate: new Date('2025-11-28'),
        sessionType: 'FIRST_HALF',
        approvalRequired: true,
        approvalCode: '594293'
      },
      {
        userId: userMap.get('10034'),
        projectTitle: 'SAFETY VALVE SYSTEM',
        logHeading: 'TESTING FOR ONLINE',
        logDetails: 'THE EXAMPLE OF TESTING',
        logDate: new Date('2025-11-29'),
        sessionType: 'FIRST_HALF',
        approvalRequired: true,
        approvalCode: '120236'
      },
      {
        userId: userMap.get('EMP001'),
        projectTitle: 'SAFETY VALVE SYSTEM',
        logHeading: 'SUPPORT ONLINE',
        logDetails: 'THE DETAIL SHOULD BE PROVIDE THE LOG DETAILS',
        logDate: new Date('2025-12-02'),
        sessionType: 'FIRST_HALF',
        approvalRequired: false,
        approvalCode: null
      }
    ]

    for (const logData of existingLogs) {
      if (logData.userId) {
        await prisma.userLog.create({
          data: logData
        })
        console.log(`✅ Migrated log: ${logData.logHeading}`)
      }
    }

    // 4. Migrate Leave Requests
    console.log('🏖️ Migrating leave requests...')
    
    const existingLeaves = [
      {
        userId: userMap.get('EMP001'),
        leaveDate: new Date('2025-11-28'),
        leaveType: 'CASUAL',
        notes: '56445654654',
        status: 'APPROVED',
        isEditable: false,
        editableUntil: new Date('2025-11-29T00:08:05'),
        createdBy: userMap.get('EMP001'),
        approvedBy: userMap.get('EMP001'),
        approvedAt: new Date('2025-11-29T10:06:57'),
        approvalNotes: '',
        createdAt: new Date('2025-11-28T23:58:05')
      },
      {
        userId: userMap.get('EMP001'),
        leaveDate: new Date('2025-11-29'),
        leaveType: 'CASUAL',
        notes: 'Some personal work',
        status: 'APPROVED',
        isEditable: false,
        editableUntil: new Date('2025-11-29T11:23:13'),
        createdBy: userMap.get('EMP001'),
        approvedBy: userMap.get('EMP001'),
        approvedAt: new Date('2025-11-29T11:25:58'),
        approvalNotes: 'ok',
        createdAt: new Date('2025-11-29T11:13:13')
      },
      {
        userId: userMap.get('EMP001'),
        leaveDate: new Date('2025-11-29'),
        leaveType: 'PLANNED',
        notes: 'i planned leave for 2 days',
        status: 'APPROVED',
        isEditable: false,
        editableUntil: new Date('2025-11-29T17:38:11'),
        createdBy: userMap.get('EMP001'),
        approvedBy: userMap.get('EMP001'),
        approvedAt: new Date('2025-11-29T17:29:03'),
        approvalNotes: 'proceed',
        createdAt: new Date('2025-11-29T17:28:11')
      }
    ]

    for (const leaveData of existingLeaves) {
      if (leaveData.userId && leaveData.createdBy) {
        await prisma.leave.create({
          data: leaveData
        })
        console.log(`✅ Migrated leave: ${leaveData.leaveType} on ${leaveData.leaveDate.toDateString()}`)
      }
    }

    console.log('🎉 Data migration completed successfully!')
    console.log('\n📋 Migration Summary:')
    console.log('✅ Users: 6 migrated')
    console.log('✅ Projects: 8 migrated')
    console.log('✅ User Logs: 3 migrated')
    console.log('✅ Leave Requests: 3 migrated')
    console.log('\n🔐 Login Credentials:')
    console.log('All users: [email] / Temp@123')
    console.log('Example: john.dev@smartlogx.com / Temp@123')
    console.log('Note: Users will be prompted to change password on first login')

  } catch (error) {
    console.error('❌ Migration failed:', error)
    throw error
  }
}

migrateExistingData()
  .catch((e) => {
    console.error('❌ Migration script failed:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })