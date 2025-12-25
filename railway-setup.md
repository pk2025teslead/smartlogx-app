# Railway PostgreSQL Setup

## Quick Setup:

1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Provision PostgreSQL"
5. Once created, click on the PostgreSQL service
6. Go to "Variables" tab
7. Copy the `DATABASE_URL`
8. Update your `.env` file

## Example Railway DATABASE_URL:
```
DATABASE_URL="postgresql://postgres:password@roundhouse.proxy.rlwy.net:12345/railway"
```

## Benefits:
- Free tier available
- Always-on database
- Easy setup
- Good performance