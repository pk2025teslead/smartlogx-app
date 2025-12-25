import crypto from 'crypto'

/**
 * Verify Django PBKDF2 password hash
 * Format: pbkdf2_sha256$iterations$salt$hash
 */
export function verifyDjangoPassword(password: string, hashedPassword: string): boolean {
  try {
    const parts = hashedPassword.split('$')
    if (parts.length !== 4 || parts[0] !== 'pbkdf2_sha256') {
      return false
    }

    const [, iterationsStr, salt, expectedHash] = parts
    const iterations = parseInt(iterationsStr, 10)

    // Generate hash using the same method as Django
    const hash = crypto.pbkdf2Sync(password, salt, iterations, 32, 'sha256')
    const base64Hash = hash.toString('base64')

    return base64Hash === expectedHash
  } catch (error) {
    console.error('Error verifying Django password:', error)
    return false
  }
}

/**
 * Test function to verify password verification works
 */
export function testDjangoPassword() {
  // Test with known Django hash (password: "Temp@123")
  const testHash = 'pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI='
  const testPassword = 'Temp@123'
  
  const isValid = verifyDjangoPassword(testPassword, testHash)
  console.log(`Django password test: ${isValid ? 'PASS' : 'FAIL'}`)
  
  return isValid
}