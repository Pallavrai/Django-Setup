# Django Production Boilerplate

A comprehensive Django 4.2+ boilerplate application with modern tooling and best practices. This project includes Django REST Framework, Celery for background tasks, PostGIS for geospatial support, Redis for caching, and a beautiful admin interface with Django Unfold.

> **🎯 Perfect Starter Template**: This boilerplate is designed to be easily customizable for any Django project. Simply clone, rename, and start building your application with production-ready foundations.

## ✨ Features

### Core Technologies
- **Django 4.2+** with modern Python 3.11+ support
- **Django REST Framework** for API development with OpenAPI/Swagger documentation
- **PostGIS** support for geospatial applications
- **Celery** with Redis for background task processing
- **Django Unfold** - Beautiful modern admin interface
- **UV Package Manager** for fast dependency management
- **WhiteNoise** for static file serving
- **Django Silk** for performance profiling

### Built-in Apps & Features
- 🔐 **Authentication** with Token-based API authentication
- 📧 **Email System** with Celery-based email testing commands
- 🗄️ **Database** PostgreSQL with PostGIS extension support
- 📊 **Admin Interface** with Django Unfold (beautiful, modern UI)
- 🔍 **API Documentation** with drf-spectacular (Swagger/OpenAPI)
- 🚀 **Performance Monitoring** with Django Silk
- 📁 **File Upload** handling with proper media management
- 🌍 **CORS** support for frontend integration
- 📦 **Import/Export** functionality for admin
- 🔧 **Management Commands** for common tasks

### Development Tools
- **Docker & Docker Compose** for containerized development
- **uv** for ultra-fast Python package management
- **Pre-configured environments** for development and production
- **Email testing** with comprehensive management commands
- **Admin user creation** command

## 🌟 Branch Selection

This repository offers different branches to suit your project needs:

### 📦 Main Branch
- **Best for**: Basic Django projects, APIs, simple web applications
- **Includes**: Django, DRF, PostgreSQL, Admin interface, basic features
- **Use when**: You don't need background task processing

### 🔄 Celery+Redis Branch  
- **Best for**: Applications requiring background tasks, email processing, scheduled jobs
- **Includes**: Everything from main branch + Celery + Redis + advanced task management
- **Use when**: You need asynchronous task processing, email queues, periodic tasks

## 🚀 Quick Start

### 🎯 Customizing for Your Project

This boilerplate is designed to be easily adapted for any Django project. Follow these steps to set it up for your specific project:

#### 1. Clone and Setup New Project

**Choose the right branch for your needs:**

```bash
# For basic Django setup (main branch)
git clone https://github.com/Pallavrai/Django-Setup.git your-project-name

# For advanced setup with Celery + Redis (celery+redis branch)
git clone -b celery%2Bredis https://github.com/Pallavrai/Django-Setup.git your-project-name

cd your-project-name

# Remove the original git history
rm -rf .git

# Initialize new git repository
git init
git add .
git commit -m "Initial commit from Django Production Boilerplate"
```

**Branch Information:**
- `main` - Basic Django setup with core features
- `celery+redis` - Advanced setup including Celery for background tasks and Redis for caching

#### 2. Customize Project Settings
Update the following files with your project-specific information:

**pyproject.toml** - Update project metadata:
```toml
[project]
name = "your-project-name"
description = "Your project description"
authors = [
    {name = "Your Name", email = "your-email@example.com"}
]
# Update other fields as needed
```

**django.env** - Configure your environment:
```bash
cp django.env.example django.env
# Edit django.env with your project-specific settings
```

**config/settings.py** - Update project-specific settings:
- Database name
- Email settings
- CORS origins
- Any app-specific configurations

#### 3. Rename Django Project (Optional)
If you want to rename the Django project from 'config' to your project name:
```bash
# Rename the config directory
mv config your_project_name

# Update manage.py
# Update docker-compose.yml
# Update any import statements
```

### Prerequisites
- Python 3.11+ 
- PostgreSQL with PostGIS extension
- Redis (for Celery)
- uv package manager (recommended) or pip

### 1. Environment Setup

Copy the environment file and configure your settings:
```bash
cp django.env.example django.env
```

Generate a Django secret key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Update `django.env` with your configuration:
```env
DJANGO_SECRET_KEY='your_generated_secret_key_here'
DEBUG=True
POSTGRES_DB=your_project_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
# ... other settings
```

### 2. Local Development (Without Docker)

#### Install Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt  # if you have requirements.txt
```

#### Database Setup
```bash
# Make sure PostgreSQL is running with PostGIS extension
# Create your database
createdb your_project_db

# Run migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Create admin user
uv run python manage.py createAdmin
```

#### Start Development Services
```bash
# Terminal 1: Start Redis (required for Celery)
redis-server

# Terminal 2: Start Celery worker
uv run celery -A config worker --loglevel=info

# Terminal 3: Start Django development server
uv run python manage.py runserver
```

### 3. Docker Development

## 🌐 Infrastructure Setup Scripts

### AWS/Cloud Deployment
Script for AWS EC2 instances (Amazon Linux):
```bash
#!/bin/bash
sudo yum -y update
sudo yum install -y docker
sudo usermod -a -G docker $(whoami)
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/download/2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Ubuntu/Debian:
```bash
#!/bin/bash
sudo apt update
sudo apt install -y docker.io
sudo usermod -a -G docker $(whoami)
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/download/2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Reset Project for New Repository
```bash
# Remove git history
rm -rf .git

# Initialize new repository
git init
git add .
git commit -m "Initial commit"

# Add remote and push
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main
```

Build and run with Docker Compose:
```bash
# Build the containers
docker-compose build

# Start all services
docker-compose up

# Run in background
docker-compose up -d
```

The Docker setup includes:
- **Django App** (main application)
- **PostgreSQL** with PostGIS extension
- **Redis** for Celery tasks
- **Nginx** as reverse proxy
- **Celery Worker** for background tasks
- **Adminer** for database management (available at http://localhost:8080)

## 🛠️ Available Management Commands

### Core Commands

#### Create Admin User
```bash
# Create admin user from environment variables
uv run python manage.py createAdmin

# With Docker
docker-compose exec app uv run python manage.py createAdmin
```

#### Email Testing
Comprehensive email testing with Celery integration:
```bash
# Send single test email
uv run python manage.py test_email recipient@example.com

# Send with custom subject and message
uv run python manage.py test_email recipient@example.com --subject "Test" --message "Hello"

# Send to multiple recipients
uv run python manage.py test_email --bulk email1@example.com email2@example.com

# Send synchronously (without Celery)
uv run python manage.py test_email recipient@example.com --sync

# Wait for task completion
uv run python manage.py test_email recipient@example.com --wait
```

### Database Commands
```bash
# Create and apply migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Collect static files
uv run python manage.py collectstatic
```

### Development Commands
```bash
# Start development server
uv run python manage.py runserver

# Start Django shell
uv run python manage.py shell

# Run tests
uv run python manage.py test

# Show available commands
uv run python manage.py help
```

### Celery Commands
```bash
# Start Celery worker
uv run celery -A config worker --loglevel=info

# Start Celery beat (for scheduled tasks)
uv run celery -A config beat --loglevel=info

# Monitor Celery tasks
uv run celery -A config flower  # if flower is installed
```

## 🎯 Key Features Explained

### 1. Modern Admin Interface (Django Unfold)
- Beautiful, responsive design
- Custom color scheme and branding
- Enhanced user experience
- Built-in import/export functionality

Access at: `http://localhost:8000/admin/`

### 2. API Documentation
- Auto-generated Swagger/OpenAPI documentation
- Interactive API explorer
- Authentication support

Access at: `http://localhost:8000/api/schema/swagger-ui/`

### 3. Performance Monitoring (Django Silk)
- SQL query analysis
- Request/response profiling
- Performance insights

Access at: `http://localhost:8000/silk/`

### 4. Email System
- Gmail SMTP configuration
- Celery-based async email sending
- Comprehensive testing commands
- Retry logic and error handling

### 5. Geospatial Support
- PostGIS integration
- GeoDjango support
- Spatial queries and operations

## 🏗️ Project Structure

```
django-production-boilerplate/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py           # URL configuration
│   ├── celery.py         # Celery configuration
│   └── wsgi.py           # WSGI application
├── core_commands/         # Core management commands
│   ├── management/
│   │   └── commands/
│   │       ├── createAdmin.py    # Admin user creation
│   │       └── test_email.py     # Email testing
│   ├── tasks.py          # Celery tasks
│   └── models.py         # Core models
├── media/                # User uploaded files
├── nginx/                # Nginx configuration
├── static/               # Static files
├── templates/            # Django templates
├── django.env           # Environment variables
├── docker-compose.yml   # Docker services
├── Dockerfile          # Docker image definition
├── manage.py           # Django management script
└── pyproject.toml      # Python dependencies (UV)
```

## 🔧 Configuration

### Environment Variables
Key configuration options in `django.env`:

```env
# Django Core
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
POSTGRES_DB=your_project_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis/Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
CORS_ALLOW_CREDENTIALS=True

# Admin User
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=secure_password
```

### Database Configuration
The project supports both development and production database configurations:

**Development**: Individual PostgreSQL connection parameters
**Production**: DATABASE_URL for services like Heroku, Railway, etc.

## 🚀 Deployment

### Production Deployment
```bash
# Set production environment variables
export DEBUG=False
export DATABASE_URL=postgresql://user:pass@host:port/dbname

# Collect static files
uv run python manage.py collectstatic --noinput

# Run migrations
uv run python manage.py migrate

# Create admin user
uv run python manage.py createAdmin

# Start with Gunicorn
uv run gunicorn -c gunicorn.conf.py config.wsgi:application
```

### Docker Production
```bash
# Build production image
docker-compose -f docker-compose.yml build

# Deploy
docker-compose up -d
```

## 📊 Monitoring & Debugging

### Django Silk Profiling
- Enable in development: `DEBUG=True`
- Access at `/silk/`
- Monitor SQL queries, request times, and performance

### Celery Monitoring
```bash
# Monitor worker status
uv run celery -A config inspect active

# Monitor task statistics
uv run celery -A config inspect stats
```

### Logs
```bash
# View Docker logs
docker-compose logs -f app
docker-compose logs -f celery

# View specific service logs
docker-compose logs -f redis
docker-compose logs -f db
```

## 🔍 API Usage

### Authentication
```python
# Token-based authentication
headers = {
    'Authorization': 'Token your_token_here',
    'Content-Type': 'application/json'
}
```

### API Endpoints
- `/api/schema/` - OpenAPI schema
- `/api/schema/swagger-ui/` - Swagger UI
- `/api/schema/redoc/` - ReDoc interface
- `/admin/` - Django admin interface
- `/silk/` - Performance profiling

## 🧪 Testing

### Email Testing
See detailed email testing documentation in `EMAIL_TESTING.md`

### Unit Tests
```bash
# Run all tests
uv run python manage.py test

# Run specific app tests
uv run python manage.py test core_commands

# Run with coverage
uv run coverage run --source='.' manage.py test
uv run coverage report
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `uv run python manage.py test`
6. Commit changes: `git commit -am 'Add new feature'`
7. Push to branch: `git push origin feature-name`
8. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Author**: Pallav Rai  
**Copyright**: © 2025 Pallav Rai  
**Project**: Django Production Boilerplate - Modern Django Starter Template

### Attribution
While not required by the MIT License, attribution is appreciated when using this boilerplate:
- Keep the LICENSE and NOTICE files in your project
- Consider mentioning the original author (Pallav Rai) in your project documentation
- Reference this boilerplate in your README or credits
- Include a link back to the original repository when possible

### Commercial Use
This software may be used for commercial purposes under the terms of the MIT License.
No additional permissions are required, but attribution is appreciated.

For more details, see the [NOTICE](NOTICE) file.

## 🆘 Support

For support and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Include error logs and configuration details

## 🔄 Version History

- **v2.0.0** - Major update with Django Unfold, enhanced email system, and improved Docker setup
- **v1.0.0** - Initial release with basic Django, PostgreSQL, and Docker setup