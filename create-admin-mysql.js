const { PrismaClient } = require('@prisma/client')
const crypto = require('crypto')

const prisma = new PrismaClient()

function createDjangoPasswordHash(password) {
  const iterations = 720000
  const salt = crypto.randomBytes(12).toString('base64').replace(/[+/=]/g, '').substring(0, 22)
  const hash = crypto.pbkdf2Sync(password, salt, iterations, 32, 'sha256')
  const base64Hash = hash.toString('base64')
  
  return `pbkdf2_sha256$${iterations}$${salt}$${base64Hash}`
}

async function createAdmin() {
  try {
    console.log('🔧 Creating admin user in MySQL...')
    
    // Check if admin already exists
    const existingAdmin = await prisma.$queryRaw`
      SELECT * FROM users_master WHERE EMAIL = 'admin@smartlogx.com'
    `
    
    if (existingAdmin.length > 0) {
      console.log('✅ Admin user already exists')
      return
    }
    
    // Create Django-compatible password hash
    const passwordHash = createDjangoPasswordHash('admin123')
    
    // Insert admin user
    await prisma.$executeRaw`
      INSERT INTO users_master (EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT)
      VALUES ('ADMIN001', 'System Administrator', '9999999999', 'admin@smartlogx.com', 'ADMIN', 'IT Operations', ${passwordHash}, 0, NOW(), NOW())
    `
    
    console.log('✅ Admin user created successfully!')
    console.log('📋 Login Credentials:')
    console.log('Email: admin@smartlogx.com')
    console.log('Password: admin123')
    
  } catch (error) {
    console.error('❌ Error creating admin:', error.message)
  } finally {
    await prisma.$disconnect()
  }
}

createAdmin()