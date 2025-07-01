#!/bin/bash

# Django Production Boilerplate Setup Script
# This script helps you customize the boilerplate for your new project

echo "🚀 Django Production Boilerplate Setup"
echo "======================================"

# Get project information from user
read -p "Enter your project name (e.g., my-awesome-project): " PROJECT_NAME
read -p "Enter your project description: " PROJECT_DESCRIPTION
read -p "Enter your name: " AUTHOR_NAME
read -p "Enter your email: " AUTHOR_EMAIL
read -p "Enter your GitHub username: " GITHUB_USERNAME

# Validate inputs
if [ -z "$PROJECT_NAME" ] || [ -z "$AUTHOR_NAME" ] || [ -z "$AUTHOR_EMAIL" ]; then
    echo "❌ Error: Project name, author name, and email are required."
    exit 1
fi

echo ""
echo "📝 Installing dependencies..."

# Install dependencies first to ensure Django is available for secret key generation
if command -v uv >/dev/null 2>&1; then
    echo "🔄 Running uv sync to install dependencies..."
    uv sync
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies with uv sync"
        exit 1
    fi
else
    echo "❌ Error: UV is not installed. Please install UV first: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo ""
echo "📝 Updating project files..."

# Update pyproject.toml (simplified for the new structure)
if [ -f "pyproject.toml" ]; then
    sed -i.bak "s/name = \"django-production-boilerplate\"/name = \"$PROJECT_NAME\"/" pyproject.toml
    sed -i.bak "s/description = \"Production-Ready Django Boilerplate with modern tooling, best practices, and easy project customization\"/description = \"$PROJECT_DESCRIPTION\"/" pyproject.toml
    
    echo "✅ Updated pyproject.toml"
fi

# Update django.env.example
if [ -f "django.env.example" ]; then
    PROJECT_DB_NAME=$(echo "$PROJECT_NAME" | tr '-' '_')_db
    sed -i.bak "s/POSTGRES_DB=your_project_db/POSTGRES_DB=$PROJECT_DB_NAME/" django.env.example
    echo "✅ Updated django.env.example"
fi

# Copy django.env.example to django.env if it doesn't exist
if [ ! -f "django.env" ] && [ -f "django.env.example" ]; then
    cp django.env.example django.env
    echo "✅ Created django.env from template"
fi

# Generate Django secret key using uv run
SECRET_KEY=$(uv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
if [ $? -eq 0 ] && [ ! -z "$SECRET_KEY" ]; then
    if [ -f "django.env" ]; then
        sed -i.bak "s/DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY='$SECRET_KEY'/" django.env
        echo "✅ Generated new Django secret key"
    fi
else
    echo "❌ Failed to generate Django secret key. Make sure Django is properly installed."
    exit 1
fi

# Clean up backup files
rm -f pyproject.toml.bak django.env.example.bak django.env.bak

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Review and update django.env with your database and email settings"
echo "2. Create your database: createdb ${PROJECT_DB_NAME:-your_project_db}"
echo "3. Run migrations: uv run python manage.py migrate"
echo "4. Create admin user: uv run python manage.py createAdmin"
echo "5. Start development server: uv run python manage.py runserver"
echo ""
echo "💡 Useful commands:"
echo "   - Activate virtual environment: source .venv/bin/activate"
echo "   - Run Django commands: uv run python manage.py <command>"
echo "   - Install new packages: uv add <package-name>"
echo ""
echo "🔗 Remember to update the repository URLs if you're using version control!"
echo ""
echo "Happy coding! 🚀"
