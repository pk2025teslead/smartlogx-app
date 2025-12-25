const { PrismaClient } = require('@prisma/client')

const prisma = new PrismaClient()

async function testConnection() {
  try {
    console.log('🔍 Testing MySQL database connection...')
    
    // Test basic connection
    await prisma.$connect()
    console.log('✅ Database connected successfully!')
    
    // Test if we can query the database
    const result = await prisma.$queryRaw`SELECT 1 as test`
    console.log('✅ Query test successful:', result)
    
    // Check if users_master table exists and has data
    try {
      const userCount = await prisma.$queryRaw`SELECT COUNT(*) as count FROM users_master`
      console.log('✅ users_master table found with', userCount[0].count, 'users')
    } catch (error) {
      console.log('❌ users_master table not found or empty:', error.message)
    }
    
    // Check if user_logs table exists and has data
    try {
      const logCount = await prisma.$queryRaw`SELECT COUNT(*) as count FROM user_logs`
      console.log('✅ user_logs table found with', logCount[0].count, 'logs')
    } catch (error) {
      console.log('❌ user_logs table not found or empty:', error.message)
    }
    
    // Check if attendance_leave_v2 table exists and has data
    try {
      const leaveCount = await prisma.$queryRaw`SELECT COUNT(*) as count FROM attendance_leave_v2`
      console.log('✅ attendance_leave_v2 table found with', leaveCount[0].count, 'leave requests')
    } catch (error) {
      console.log('❌ attendance_leave_v2 table not found or empty:', error.message)
    }
    
  } catch (error) {
    console.error('❌ Database connection failed:', error.message)
    console.log('\n🔧 Troubleshooting:')
    console.log('1. Check if MySQL is running')
    console.log('2. Verify DATABASE_URL in .env file')
    console.log('3. Check username/password')
    console.log('4. Ensure smartlogx_db database exists')
  } finally {
    await prisma.$disconnect()
  }
}

testConnection()