# SmartLogX Setup Script
# Run this script to set up the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SmartLogX - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Database setup
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Database Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Running interactive database setup..." -ForegroundColor Yellow
python db_setup.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Database setup failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

# Create superuser
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Create Admin Account" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
$createAdmin = Read-Host "Do you want to create an admin account now? (y/n)"

if ($createAdmin -eq "y" -or $createAdmin -eq "Y") {
    python manage.py createsuperuser
}

# Collect static files
Write-Host ""
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Setup complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Then open your browser to:" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:8000/" -ForegroundColor White
Write-Host ""
Write-Host "Happy logging! 🚀" -ForegroundColor Green
