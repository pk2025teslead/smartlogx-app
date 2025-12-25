# SmartLogX Setup Guide

This guide will walk you through setting up the SmartLogX Next.js application from scratch.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 18 or higher)
- **npm** or **yarn** package manager
- **PostgreSQL** (version 12 or higher)
- **Git** for version control

## 🗄️ PostgreSQL Database Setup

### Option 1: Local PostgreSQL Installation

#### Windows
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Add PostgreSQL to your PATH environment variable

#### macOS
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql

# Create a database user (optional)
createuser --interactive
```

#### Linux (Ubuntu/Debian)
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user and create database
sudo -u postgres psql
```

### Option 2: Docker PostgreSQL
```bash
# Run PostgreSQL in Docker
docker run --name smartlogx-postgres \\
  -e POSTGRES_PASSWORD=yourpassword \\
  -e POSTGRES_DB=smartlogx_db \\
  -p 5432:5432 \\
  -d postgres:15

# Verify it's running
docker ps
```

### Option 3: Cloud PostgreSQL (Recommended for Production)

#### Supabase (Free Tier Available)
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your database URL from Settings > Database
4. Use the connection string in your `.env` file

#### Railway
1. Go to [railway.app](https://railway.app)
2. Create a new project
3. Add PostgreSQL service
4. Copy the database URL

#### Render
1. Go to [render.com](https://render.com)
2. Create a new PostgreSQL database
3. Copy the connection details

## 🚀 Application Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd smartlogx-nextjs
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Using yarn
yarn install
```

### 3. Environment Configuration

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/smartlogx_db"

# NextAuth Configuration
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-very-secure-secret-key-here"

# Email Configuration (Optional but recommended)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"
ADMIN_EMAIL="admin@smartlogx.com"

# Application Configuration
APP_NAME="SmartLogX"
APP_URL="http://localhost:3000"
```

#### Database URL Examples:
```env
# Local PostgreSQL
DATABASE_URL="postgresql://postgres:password@localhost:5432/smartlogx_db"

# Docker PostgreSQL
DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/smartlogx_db"

# Supabase
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres"

# Railway
DATABASE_URL="postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/railway"

# Render
DATABASE_URL="postgresql://[USER]:[PASSWORD]@[HOST]/[DATABASE]"
```

### 4. Generate NextAuth Secret
```bash
# Generate a secure secret
openssl rand -base64 32

# Or use Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### 5. Database Setup

#### Create Database (if using local PostgreSQL)
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE smartlogx_db;

# Create user (optional)
CREATE USER smartlogx_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE smartlogx_db TO smartlogx_user;

# Exit
\\q
```

#### Generate Prisma Client
```bash
npm run db:generate
```

#### Push Database Schema
```bash
npm run db:push
```

#### Seed Database with Sample Data
```bash
npm run db:seed
```

### 6. Start Development Server
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 🔐 Default Login Credentials

After seeding, you can log in with these accounts:

### Administrator
- **Email**: `admin@smartlogx.com`
- **Password**: `admin123`

### Sample Employees
- **Email**: `john.dev@smartlogx.com` | **Password**: `Temp@123`
- **Email**: `jane.test@smartlogx.com` | **Password**: `Temp@123`
- **Email**: `mike.design@smartlogx.com` | **Password**: `Temp@123`
- **Email**: `sarah.coord@smartlogx.com` | **Password**: `Temp@123`

## 📧 Email Setup (Optional)

### Gmail Configuration
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Generate password for "Mail"
3. Use the app password in your `.env` file

### Other Email Providers
```env
# Outlook/Hotmail
SMTP_HOST="smtp-mail.outlook.com"
SMTP_PORT="587"

# Yahoo
SMTP_HOST="smtp.mail.yahoo.com"
SMTP_PORT="587"

# Custom SMTP
SMTP_HOST="your-smtp-server.com"
SMTP_PORT="587"
```

## 🛠️ Development Tools

### Database Management
```bash
# Open Prisma Studio (Database GUI)
npm run db:studio

# Reset database (careful!)
npx prisma db push --force-reset

# Generate new migration
npx prisma migrate dev --name your_migration_name
```

### Code Quality
```bash
# Run TypeScript type checking
npx tsc --noEmit

# Run ESLint
npm run lint

# Format code with Prettier (if configured)
npm run format
```

## 🚀 Production Deployment

### Build for Production
```bash
npm run build
npm start
```

### Environment Variables for Production
```env
# Production Database
DATABASE_URL="your-production-database-url"

# Production URL
NEXTAUTH_URL="https://your-domain.com"

# Secure secret (different from development)
NEXTAUTH_SECRET="your-production-secret"

# Production email settings
SMTP_HOST="your-production-smtp"
ADMIN_EMAIL="admin@your-domain.com"
```

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgres  # macOS

# Test connection
psql -U postgres -h localhost -p 5432 -d smartlogx_db
```

#### Prisma Client Error
```bash
# Regenerate Prisma client
npm run db:generate

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :3000  # Windows
```

#### Environment Variables Not Loading
- Ensure `.env` file is in the root directory
- Restart the development server after changing `.env`
- Check for typos in variable names

### Database Reset (if needed)
```bash
# Complete reset
npx prisma db push --force-reset
npm run db:seed
```

## 📊 Monitoring and Logs

### Development Logs
```bash
# View application logs
npm run dev

# View database queries (add to schema.prisma)
# generator client {
#   provider = "prisma-client-js"
#   log      = ["query", "info", "warn", "error"]
# }
```

### Production Monitoring
- Use services like Vercel Analytics, Railway Metrics, or custom monitoring
- Set up error tracking with Sentry or similar
- Monitor database performance with connection pooling

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** in your terminal
2. **Verify environment variables** are correctly set
3. **Ensure database is running** and accessible
4. **Check PostgreSQL logs** for database issues
5. **Review the README.md** for additional information

### Support Channels
- Create an issue on GitHub
- Check existing issues for solutions
- Review the documentation

---

**You're all set! 🎉 Your SmartLogX application should now be running successfully.**