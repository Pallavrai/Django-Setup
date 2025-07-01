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
echo "📝 Updating project files..."

# Update pyproject.toml
if [ -f "pyproject.toml" ]; then
    sed -i.bak "s/name = \"django-production-boilerplate\"/name = \"$PROJECT_NAME\"/" pyproject.toml
    sed -i.bak "s/description = \"Production-Ready Django Boilerplate with modern tooling, best practices, and easy project customization\"/description = \"$PROJECT_DESCRIPTION\"/" pyproject.toml
    sed -i.bak "s/Pallav Rai/$AUTHOR_NAME/g" pyproject.toml
    sed -i.bak "s/pallavrai@example.com/$AUTHOR_EMAIL/g" pyproject.toml
    
    if [ ! -z "$GITHUB_USERNAME" ]; then
        sed -i.bak "s|https://github.com/Pallavrai/Django-Setup|https://github.com/$GITHUB_USERNAME/$PROJECT_NAME|g" pyproject.toml
        sed -i.bak "s/Pallavrai/$GITHUB_USERNAME/g" pyproject.toml
    fi
    
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

# Generate Django secret key
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
if [ -f "django.env" ]; then
    sed -i.bak "s/DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY='$SECRET_KEY'/" django.env
    echo "✅ Generated new Django secret key"
fi

# Clean up backup files
rm -f pyproject.toml.bak django.env.example.bak django.env.bak

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Review and update django.env with your database and email settings"
echo "2. Install dependencies: uv sync"
echo "3. Create your database: createdb $PROJECT_DB_NAME"
echo "4. Run migrations: uv run python manage.py migrate"
echo "5. Create admin user: uv run python manage.py createAdmin"
echo "6. Start development server: uv run python manage.py runserver"
echo ""
echo "🔗 Remember to update the repository URLs if you're using version control!"
echo ""
echo "Happy coding! 🚀"
