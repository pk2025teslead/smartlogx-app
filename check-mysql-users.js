const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function checkUsers() {
  try {
    console.log('🔍 Checking users in MySQL database...')
    
    // Get all users from users_master table
    const users = await prisma.$queryRaw`
      SELECT ID, EMP_ID, EMP_NAME, EMAIL, ROLE, PASSWORD, IS_FIRST_LOGIN 
      FROM users_master 
      LIMIT 10
    `
    
    console.log('\n👥 Users found in database:')
    users.forEach(user => {
      console.log(`- ${user.EMP_NAME} (${user.EMP_ID})`)
      console.log(`  Email: ${user.EMAIL}`)
      console.log(`  Role: ${user.ROLE}`)
      console.log(`  Password Hash: ${user.PASSWORD.substring(0, 50)}...`)
      console.log(`  First Login: ${user.IS_FIRST_LOGIN}`)
      console.log('---')
    })
    
    // Check if admin user exists
    const adminUser = await prisma.$queryRaw`
      SELECT * FROM users_master 
      WHERE EMAIL = 'admin@smartlogx.com' OR EMP_ID = 'admin' OR ROLE = 'ADMIN'
    `
    
    if (adminUser.length > 0) {
      console.log('\n🔑 Admin users found:')
      adminUser.forEach(admin => {
        console.log(`- ${admin.EMP_NAME}: ${admin.EMAIL}`)
      })
    } else {
      console.log('\n❌ No admin user found')
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message)
  } finally {
    await prisma.$disconnect()
  }
}

checkUsers()