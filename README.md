# 🤖 TaskBot AI

<div align="center">
  <p><strong>Intelligent Full-Stack To-Do Application powered by Google Gemini 2.5 Flash</strong></p>
</div>

TaskBot AI is a modern, responsive, and intelligent task management assistant. It seamlessly integrates a natural language chatbot that understands casual conversation and strict commands (in English, French, Arabic, and Darija). Ask the AI to add, update, or delete tasks, and watch your dashboard update in real-time!

---

## ✨ Key Features

- **🧠 AI Intent Parsing:** Speak naturally. The Gemini-powered backend strictly categorizes your text into actionable database operations (Create, Delete, Update, Show).
- **🌍 Multi-Lingual Support:** Naturally handles inputs and responds in Darija, Arabic, French, and English.
- **⚡ Real-Time Sync:** Tasks are instantly reflected on the UI without manual page refreshes.
- **🛡️ Secure Architecture:** JWT-based authentication ensures that each user's tasks are strictly isolated and protected.
- **📱 Responsive UI:** A premium, "SaaS-style" dashboard built with React, Tailwind CSS, and Framer Motion animations.
- **🐳 Docker Ready:** Fully containerized for one-click deployment.

---

## 🛠️ Tech Stack

- **Frontend:** React, Vite, Tailwind CSS, Framer Motion, Lucide React
- **Backend:** Python, FastAPI, Pydantic, JWT (Passlib)
- **Database:** MongoDB (PyMongo)
- **AI Integration:** Google Gemini 2.5 Flash API (google-genai)
- **Deployment:** Docker & Docker Compose

---

## 📋 Prerequisites

Make sure you have the following installed on your system before proceeding:

- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://www.python.org/) (3.10+)
- [MongoDB](https://www.mongodb.com/) (Local instance or MongoDB Atlas)
- [Docker](https://www.docker.com/) & Docker Compose (For containerized deployment)

---

## 🔐 Environment Variables

You must create a `.env` file in the `backend/` directory. **Never commit your `.env` file to version control.**

| Variable | Description | Example |
|---|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API Key | `AIzaSyB...` |
| `MONGODB_URL` | Connection string to your MongoDB | `mongodb://localhost:27017/` |
| `JWT_SECRET_KEY` | A secure random string for JWT encoding | `your_super_secret_key` |
| `ALGORITHM` | JWT hashing algorithm (Default: `HS256`) | `HS256` |

---

## 💻 Local Setup & Installation

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` file inside the `backend/` directory.
5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The API will be available at `http://localhost:8000`.*

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The UI will be accessible at `http://localhost:5173`.*

---

## 🐳 Docker Setup (Production Ready)

To spin up the entire Full-Stack application (MongoDB, FastAPI Backend, and React Frontend) with a single command:

1. Ensure Docker Desktop is running.
2. Verify that your `backend/.env` file is properly configured.
3. From the root directory, run:
   ```bash
   docker-compose up --build
   ```

**Service Endpoints:**
- **Frontend UI:** `http://localhost:5173`
- **Backend API:** `http://localhost:8000`
- **MongoDB:** `localhost:27017`

To stop the containers, use:
```bash
docker-compose down
```

---

<div align="center">
  <i>Built with ❤️ for intelligent productivity.</i>
</div>
