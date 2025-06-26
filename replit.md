# Overview

This is a romantic multi-page web application built as a personal love website with mobile-first responsive design. The application is designed to be a heartfelt digital gift, featuring multiple sections dedicated to expressing love, tracking personal wellness, sharing memories, and maintaining a romantic journal. The website combines emotional content with practical features like photo uploads, period tracking, private chat functionality, and dynamic content management. Features adorable dog-themed UI elements and seamless mobile experience with hamburger navigation.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap 5 with custom romantic styling
- **Animation Library**: AOS (Animate On Scroll) for smooth animations
- **Responsive Design**: Mobile-first approach using Bootstrap grid system
- **Typography**: Google Fonts (Dancing Script for headings, Poppins for body text)

## Backend Architecture
- **Framework**: Flask (Python web framework)
- **File Handling**: Werkzeug for secure file uploads
- **Session Management**: Flask sessions with secret key
- **WSGI Server**: Gunicorn for production deployment
- **Proxy Handling**: ProxyFix middleware for deployment environments

## Data Storage
- **File-based Storage**: JSON files for period tracking data
- **Image Storage**: Local filesystem in `static/uploads/` directory
- **Configuration**: Environment variables for sensitive data

# Key Components

## Core Application (app.py)
- Flask application setup with secret key management
- File upload handling with security validation
- Period tracking functionality with JSON persistence
- Template rendering with dynamic data

## Template System
- **Base Template**: Common layout with responsive navigation and mobile hamburger menu
- **Home Page**: Animated landing page with typing effects and floating dog-themed elements
- **Why I Love You**: Reasons for love with card-based layout
- **Favorites**: Movies and songs in organized sections
- **Food Memories**: Restaurant and dish tracking with priority system and dynamic add/delete
- **Photo Memories**: Image gallery with upload and delete functionality
- **Period Tracker**: Wellness tracking with cycle predictions
- **Journal**: Daily affirmations and messages
- **Contact Page**: Contact form with dog-themed animations
- **Chat Page**: Private WhatsApp-style chat with image sharing
- **Apology Page**: Dedicated apologetic content

## Styling System
- Custom CSS variables for consistent romantic theme
- Pink and purple color scheme with gradients
- Hover effects and animations for interactive elements
- Responsive design for all screen sizes

## File Upload System
- Secure filename handling with Werkzeug
- Image validation for supported formats (PNG, JPG, JPEG, GIF, WEBP)
- Organized storage in static/uploads directory

# Data Flow

## Image Upload Flow
1. User selects image file through web form
2. Flask validates file type and secures filename
3. File is saved to static/uploads directory
4. Gallery page displays uploaded images

## Period Tracking Flow
1. User inputs last period date and cycle length
2. Flask calculates next period predictions
3. Data is saved to JSON file in data directory
4. Predictions are displayed on tracker page

## Navigation Flow
- Fixed navigation bar with smooth scrolling
- Home page as entry point with animated elements
- Interconnected pages through navigation menu
- Responsive mobile navigation with Bootstrap

# External Dependencies

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome 6**: Icon library for visual elements
- **AOS**: Animation library for scroll-triggered effects
- **Google Fonts**: Typography (Dancing Script, Poppins)

## Python Dependencies
- **Flask**: Web framework
- **Werkzeug**: WSGI utilities and security
- **Gunicorn**: WSGI HTTP server
- **email-validator**: Email validation utilities
- **psycopg2-binary**: PostgreSQL adapter (prepared for future database integration)

## System Dependencies
- **OpenSSL**: Cryptographic library
- **PostgreSQL**: Database system (configured but not actively used)

# Deployment Strategy

## Development Environment
- **Runtime**: Python 3.11 with Nix package management
- **Development Server**: Flask built-in server with debug mode
- **Hot Reload**: Automatic reloading on code changes

## Production Environment
- **WSGI Server**: Gunicorn with autoscale deployment target
- **Port Configuration**: Bound to 0.0.0.0:5000
- **Process Management**: Reuse-port option for zero-downtime deployments

## File Organization
- Static files served directly by web server
- Upload directory with proper permissions
- Data directory for JSON storage
- Environment-based configuration

# User Preferences

Preferred communication style: Simple, everyday language.

# Changelog

Changelog:
- June 26, 2025. Initial setup
- June 26, 2025. Enhanced with mobile responsiveness, contact page, private chat functionality, dynamic food management with priority system, image deletion in memories, and adorable dog-themed UI elements
- June 26, 2025. Implemented complete authentication system for Navu and Darling with PostgreSQL database
- June 26, 2025. Added WhatsApp-style chat with emoji reactions, video/image support, message deletion options
- June 26, 2025. Created "About Her" page with personal details, dress sizes, favorites, and birthday countdown
- June 26, 2025. Enhanced period tracker with comprehensive history, predictions, and desktop/mobile optimization
- June 26, 2025. Improved hamburger menu design and reduced chat animations per user feedback