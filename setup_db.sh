#!/bin/bash

# Database Setup Script for macOS
# This script helps you set up PostgreSQL for the chatbot

echo "🗄️  PostgreSQL Setup for Amzur Chatbot"
echo "======================================="
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed."
    echo "Installing PostgreSQL using Homebrew..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew is not installed. Please install it first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    brew install postgresql@14
    brew services start postgresql@14
    echo "✅ PostgreSQL installed and started"
else
    echo "✅ PostgreSQL is already installed"
fi

echo ""
echo "Creating database and user..."
echo "------------------------------"

# Create database
psql postgres -c "CREATE DATABASE chatbot_db;" 2>/dev/null && echo "✅ Database 'chatbot_db' created" || echo "ℹ️  Database 'chatbot_db' may already exist"

echo ""
echo "✅ Database setup complete!"
echo ""
echo "Your database URL is:"
echo "postgresql://postgres:postgres@localhost:5432/chatbot_db"
echo ""
echo "Make sure this matches the DATABASE_URL in your .env file"
