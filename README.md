# AI Shopping Chatbot

## Overview
A simple AI-powered shopping chatbot that allows users to browse products, ask questions, add items to a cart, and place an order via chat.

## Features
- List available products
- Ask product-related questions (price, budget)
- Add products to cart
- Checkout and confirm orders
- Orders stored in database
- Gemini API for conversational fallback

## Tech Stack
- Backend: Django, Django REST Framework
- Frontend: React (Vite)
- AI: Google Gemini API
- Database: SQLite
- Deployment:
  - Backend: Render
  - Frontend: Vercel

## Live Links
- Frontend: https://ai-shopping-chatbot-six.vercel.app/
- Backend API: https://ai-shopping-chatbot-1.onrender.com

## Sample Chat Flow
User: Show products  
Bot: Lists products  

User: Add backpack  
Bot: Added to cart  

User: Checkout  
Bot: Order confirmed with total price  

## Notes
- Cart is stored in memory for simplicity as allowed by the task.
- In a production system, cart would be persisted per user using sessions or database.

## Setup (Local)
```bash
git clone <repo>
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
