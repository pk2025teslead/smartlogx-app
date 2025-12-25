const { verifyDjangoPassword } = require('./lib/django-auth.ts')

// Test Django password verification with actual data from your database
const testCases = [
  {
    password: 'Temp@123',
    hash: 'pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI=',
    user: 'Jane Tester'
  },
  {
    password: 'admin123',
    hash: 'pbkdf2_sha256$720000$XWBOr4Fbw29qaBjm6ROtmo$qHVNscTMe+J0bLyAWj4Afz8DJ7x2u8vErqRZx/7uY9c=',
    user: 'John Developer'
  }
]

console.log('🔐 Testing Django password verification...')

testCases.forEach(test => {
  const isValid = verifyDjangoPassword(test.password, test.hash)
  console.log(`${test.user}: Password "${test.password}" - ${isValid ? '✅ VALID' : '❌ INVALID'}`)
})

// Test with wrong password
const wrongPassword = verifyDjangoPassword('wrongpassword', testCases[0].hash)
console.log(`Wrong password test: ${wrongPassword ? '❌ FAILED' : '✅ PASSED'}`)