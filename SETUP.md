
# Setup Instructions

## Running on Replit with GitHub Integration

### 1. Connect to GitHub
- Go to your Replit account settings
- Connect your GitHub account under "Connected Services"
- Import this repository or push your Replit project to GitHub

### 2. Database Setup
The app uses PostgreSQL for persistent storage. On Replit:
- PostgreSQL is already configured in the `.replit` file
- Set the `DATABASE_URL` environment variable in Replit Secrets:
  ```
  DATABASE_URL=postgresql://username:password@hostname:port/database
  ```
- Or use Replit's built-in PostgreSQL database

### 3. Environment Variables
Set these in Replit Secrets:
- `SESSION_SECRET`: A secure random string for session encryption
- `DATABASE_URL`: Your PostgreSQL connection string

### 4. File Storage
- Images are stored in `static/uploads/` directory
- This directory is persistent on Replit

### 5. Running the Application
- Use the Run button in Replit
- Or run: `gunicorn --bind 0.0.0.0:5000 main:app`

### 6. Features
- **Authentication**: Two users (love1 and love2) with secure login
- **Chat**: Real-time messaging with file sharing and reactions
- **Period Tracking**: Wellness tracking with database persistence
- **Food Memories**: Restaurant and dish tracking
- **Photo Memories**: Image gallery with upload/delete
- **Responsive Design**: Mobile-friendly interface

### 7. Data Persistence
All data is now stored in PostgreSQL:
- User accounts and profiles
- Chat messages and reactions
- Period tracking data
- Food memories
- Photo metadata

### 8. GitHub Sync
- Use Replit's built-in Git integration
- Push changes to GitHub using the Git tab
- Pull updates from GitHub repository

The application is designed to work seamlessly on Replit with full GitHub integration and persistent PostgreSQL storage.
