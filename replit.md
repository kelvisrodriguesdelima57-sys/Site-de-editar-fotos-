# EquaSmart - Math Calculator with AI

## Overview
EquaSmart is a Portuguese language web application that provides an AI-powered mathematics calculator. Users can input math questions in natural language and receive calculated answers using OpenAI's GPT-4o-mini model.

## Project Architecture
- **Frontend**: Single-page HTML application with embedded CSS and JavaScript
- **Backend**: Simple Python HTTP server serving static files
- **API Integration**: OpenAI GPT-4o-mini for mathematical computations
- **Language**: Portuguese (Brazil)

## Current State
- ✅ Web server configured and running on port 5000
- ✅ HTML application accessible via web browser
- ✅ Responsive design for mobile and desktop
- ⚠️ Requires OpenAI API key configuration for full functionality

## Project Structure
```
/
├── index.html          # Main application file with UI and logic
├── server.py          # Python HTTP server for serving static files
└── replit.md          # This documentation file
```

## Recent Changes
- **2025-09-22**: Initial project setup in Replit environment
  - Created Python HTTP server with cache control headers
  - Configured workflow to serve application on port 5000 with 0.0.0.0 binding
  - Set up proper host configuration for Replit proxy environment

## Technical Details
- **Server**: Python 3.11 with built-in HTTP server
- **Port**: 5000 (configured for Replit environment)
- **Host Binding**: 0.0.0.0 (required for Replit proxy)
- **Cache Control**: Disabled for development environment
- **API**: OpenAI Chat Completions API

## User Preferences
- Original Portuguese language interface maintained
- Dark theme UI preserved
- Responsive design kept intact
- API functionality maintained but requires key configuration

## Setup Notes
- The application requires an OpenAI API key to function fully
- Current placeholder: "SUA_CHAVE_API_AQUI" needs to be replaced
- Server automatically serves index.html for root path requests
- Cache headers are disabled for Replit development environment