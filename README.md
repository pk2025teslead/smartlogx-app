# SmartLogX - Next.js Employee Management System

A modern, full-stack employee management system built with Next.js, React, TypeScript, and PostgreSQL. This is a complete recreation of the original Django SmartLogX project with enhanced features and modern architecture.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure login with NextAuth.js and JWT
- **Role-based Access Control**: Admin and Employee dashboards
- **Work Logging**: Daily work log submission with time windows
- **Leave Management**: Leave requests with approval workflow
- **Comp-Off Management**: Sunday work compensation tracking
- **Work From Home**: WFH request management
- **Audit Trail**: Complete change history tracking

### Advanced Features
- **Time Window Validation**: Restricted log submission times (1-2:30 PM, 6-7:30 PM IST)
- **10-Minute Edit Window**: Edit requests within 10 minutes of creation
- **Approval Codes**: Out-of-window submission with approval codes
- **Email Notifications**: Automated email alerts for various actions
- **Real-time Dashboard**: Live statistics and activity monitoring
- **Export Functionality**: CSV and Excel export capabilities

## 🛠 Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS, shadcn/ui components
- **Backend**: Next.js API Routes
- **Database**: PostgreSQL with Prisma ORM
- **Authentication**: NextAuth.js
- **State Management**: TanStack Query (React Query)
- **Email**: SMTP integration
- **Deployment**: Vercel/Railway/Render ready

## 📋 Prerequisites

- Node.js 18+ 
- PostgreSQL 12+
- npm or yarn

## 🚀 Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd smartlogx-nextjs

# Install dependencies
npm install
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb smartlogx_db

# Or using psql
psql -U postgres
CREATE DATABASE smartlogx_db;
\\q
```

### 3. Environment Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configuration
DATABASE_URL="postgresql://username:password@localhost:5432/smartlogx_db"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-secret-key-here"
```

### 4. Database Migration and Seeding

```bash
# Generate Prisma client
npm run db:generate

# Push database schema
npm run db:push

# Seed with sample data
npm run db:seed
```

### 5. Start Development Server

```bash
npm run dev
```

Visit `http://localhost:3000` to access the application.

## 👥 Default Login Credentials

### Admin Account
- **Email**: admin@smartlogx.com
- **Password**: admin123

### Sample Employee Accounts
- **Email**: john.dev@smartlogx.com | **Password**: Temp@123
- **Email**: jane.test@smartlogx.com | **Password**: Temp@123
- **Email**: mike.design@smartlogx.com | **Password**: Temp@123
- **Email**: sarah.coord@smartlogx.com | **Password**: Temp@123

## 📁 Project Structure

```
smartlogx-nextjs/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── auth/              # Authentication pages
│   ├── dashboard/         # User dashboard
│   ├── admin/             # Admin dashboard
│   └── globals.css        # Global styles
├── components/            # Reusable components
│   ├── ui/               # shadcn/ui components
│   └── layout/           # Layout components
├── lib/                   # Utility libraries
│   ├── auth.ts           # NextAuth configuration
│   ├── db.ts             # Prisma client
│   └── utils.ts          # Helper functions
├── prisma/               # Database schema and migrations
│   ├── schema.prisma     # Database schema
│   └── seed.ts           # Database seeding
├── types/                # TypeScript type definitions
└── public/               # Static assets
```

## 🔧 Database Schema

### Core Tables
- **users_master**: Employee directory and authentication
- **user_logs**: Daily work logs with session tracking
- **attendance_leave_v2**: Leave requests with edit window
- **attendance_compoff**: Sunday work compensation
- **attendance_wfh**: Work from home requests
- **attendance_leave_audit**: Complete audit trail
- **approval_codes**: Temporary approval codes
- **projects**: Project master data

## 🕐 Time Windows & Business Rules

### Work Log Submission
- **First Half**: 1:00 PM - 2:30 PM IST
- **Second Half**: 6:00 PM - 7:30 PM IST
- **Out-of-window**: Requires approval code

### Edit Windows
- **Leave Requests**: 10 minutes after creation
- **Comp-Off Requests**: 10 minutes after creation
- **WFH Requests**: 10 minutes after creation

### Approval Workflow
- **Automatic**: Admin notifications on request creation
- **Manual**: Admin approval/rejection with notes
- **Audit**: Complete change history tracking

## 📧 Email Configuration

Configure SMTP settings in `.env`:

```env
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"
ADMIN_EMAIL="admin@smartlogx.com"
```

## 🚀 Deployment

### Vercel (Recommended)
1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables
4. Deploy automatically

### Railway
1. Connect GitHub repository
2. Add PostgreSQL service
3. Configure environment variables
4. Deploy

### Manual Deployment
```bash
# Build the application
npm run build

# Start production server
npm start
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/signin` - User login
- `POST /api/auth/signout` - User logout

### User Management
- `GET /api/users` - List users (admin)
- `POST /api/users` - Create user (admin)
- `PUT /api/users/[id]` - Update user (admin)
- `DELETE /api/users/[id]` - Delete user (admin)

### Work Logs
- `GET /api/logs` - Get user logs
- `POST /api/logs` - Create work log
- `PUT /api/logs/[id]` - Update work log
- `DELETE /api/logs/[id]` - Delete work log

### Leave Management
- `GET /api/attendance/leave` - Get leave requests
- `POST /api/attendance/leave` - Create leave request
- `PUT /api/attendance/leave/[id]` - Update leave request
- `POST /api/attendance/leave/[id]/approve` - Approve/reject leave

## 🔒 Security Features

- **Password Hashing**: bcryptjs with salt rounds
- **JWT Tokens**: Secure session management
- **CSRF Protection**: Built-in Next.js protection
- **Input Validation**: Zod schema validation
- **SQL Injection Prevention**: Prisma ORM protection
- **Audit Logging**: Complete action tracking

## 🧪 Testing

```bash
# Run tests (when implemented)
npm test

# Run type checking
npm run type-check

# Run linting
npm run lint
```

## 📈 Performance Optimizations

- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: React Query for client-side caching
- **Code Splitting**: Next.js automatic code splitting
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: Built-in bundle analyzer

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Email: support@smartlogx.com
- Documentation: [Project Wiki]

## 🔄 Migration from Django

This Next.js version maintains full compatibility with the original Django SmartLogX database schema while providing:
- Modern React-based UI
- Better performance
- Enhanced security
- Mobile responsiveness
- Real-time features
- Improved developer experience

---

**Built with ❤️ using Next.js, React, and TypeScript**