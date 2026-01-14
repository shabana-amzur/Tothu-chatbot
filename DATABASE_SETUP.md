# Database Setup Guide for Amzur Chatbot

## Prerequisites

You need PostgreSQL installed on your system.

### macOS Installation

```bash
# Install PostgreSQL using Homebrew
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Verify installation
psql --version
```

### Alternative: Use the setup script

```bash
chmod +x setup_db.sh
./setup_db.sh
```

## Manual Database Setup

1. **Start PostgreSQL** (if not already running):
   ```bash
   brew services start postgresql@14
   ```

2. **Create the database**:
   ```bash
   psql postgres
   CREATE DATABASE chatbot_db;
   \q
   ```

3. **Update .env file** with your database credentials:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/chatbot_db
   ```

## Using Docker (Alternative)

If you prefer Docker:

```bash
docker run --name chatbot-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=chatbot_db \
  -p 5432:5432 \
  -d postgres:14
```

## Verify Connection

Test your database connection:

```bash
psql postgresql://postgres:postgres@localhost:5432/chatbot_db
```

## Troubleshooting

### Port Already in Use
If port 5432 is already in use:
```bash
lsof -i :5432
# Kill the process or change the port in DATABASE_URL
```

### Permission Issues
```bash
# Fix PostgreSQL permissions
sudo chown -R $(whoami) /usr/local/var/postgresql@14
```

### Connection Refused
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Restart if needed
brew services restart postgresql@14
```

## Database Schema

The application will automatically create these tables:
- **users**: Store Amzur employee accounts
- **chat_messages**: Store all chat conversations

Tables are created automatically when you first run the app.
