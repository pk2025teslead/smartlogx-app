# Vercel Environment Variables Setup

## 🔧 Required Environment Variables for Vercel:

Go to your Vercel dashboard → Your Project → Settings → Environment Variables

Add these variables:

### Database
```
DATABASE_URL = postgresql://postgres:TgWowLFYKoEMqgMYeKRljOIkDKtCTyoj@switchyard.proxy.rlwy.net:26784/railway
```

### NextAuth
```
NEXTAUTH_URL = https://your-vercel-app.vercel.app
NEXTAUTH_SECRET = your-very-secure-secret-key-for-production
```

### Email (Optional)
```
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = pandikumar652001@gmail.com
SMTP_PASS = ljaq lzil dcxn dfmt
ADMIN_EMAIL = pandikumar652001@gmail.com
```

### Application
```
APP_NAME = SmartLogX
APP_URL = https://your-vercel-app.vercel.app
```

## 🔐 Generate Production Secret:
```bash
openssl rand -base64 32
```

## 📝 Important Notes:
1. Replace `your-vercel-app.vercel.app` with your actual Vercel domain
2. Use a different NEXTAUTH_SECRET for production
3. Make sure DATABASE_URL points to your Railway database
4. All variables should be set for "Production" environment