# AI Customer Support Bot 🤖💬

Hi! This is my AI Customer Support Bot project. The goal of this project is to simulate a real customer support assistant using AI. It can answer FAQs, keep track of conversations, and escalate issues to a human agent if the question is too complicated.

---

## 🌟 What It Can Do

* **Answer Questions Automatically** – The AI can respond to customer queries using a knowledge base and context from previous messages.
* **Remember Conversations** – Keeps track of the last few messages so it can give coherent answers.
* **Smart Escalation** – If it doesn’t know the answer, it can politely say so and connect the user to a human agent.
* **Short or Detailed Replies** – Can give quick answers or detailed explanations depending on the request.
* **FAQs Integration** – Uses a preloaded FAQ file to answer common questions.
* **Optional Chat Interface** – A simple web UI for chatting in real-time.

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **AI Model:** Google Gemini API (`gemini-2.5-flash`)
* **Database:** SQLite using SQLAlchemy
* **Frontend:** HTML, CSS, JavaScript
* **Environment:** python-dotenv for storing API keys

---

## 📋 What You Need

* Python 3.8 or above
* A Google Gemini API key
* (Optional) Git to clone the project

---

## ⚡ How to Set It Up

1. **Clone the repo**

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set your environment variables**

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_GOOGLE_GEMINI_KEY
GEMINI_MODEL=gemini-2.5-flash
```

---

## 📁 Project Structure

```
├── main.py                 # FastAPI backend
├── gemini_service.py       # AI integration logic
├── database.py             # Database setup and models
├── faqs.json               # FAQ knowledge base
├── templates/
│   └── chat.html           # Web chat interface
├── static/
│   ├── style.css           # Styles for chat UI
│   └── script.js           # Frontend logic
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md
```

---

## 📡 How to Use It

### 1. Ask a Question

```
POST /ask
```

Request example:

```json
{
  "session_id": "your-session-id",
  "query": "track my order",
  "concise": true
}
```

* `concise=true` → short answer
* `concise=false` → detailed answer

Response example:

```json
{
  "response": "You can track your order in 'My Orders' or via your tracking email.",
  "escalated": false
}
```

---

### 2. Start a New Session

```
POST /new_session
```

Response example:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 3. Get Conversation History

```
GET /get_history/{session_id}
```

Response example:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "track my order",
      "timestamp": "2025-10-16T16:00:00"
    },
    {
      "id": 2,
      "role": "bot",
      "content": "You can track your order in 'My Orders'...",
      "timestamp": "2025-10-16T16:00:05"
    }
  ]
}
```

---

### 4. Get FAQs

```
GET /faqs
```

Response example:

```json
[
  {
    "id": 1,
    "question": "How do I reset my password?",
    "answer": "Go to login page and click 'Forgot Password'.",
    "category": "Account"
  }
]
```

---

### 5. Chat UI

```
GET /
```

* Simple web chat interface to interact with the bot in real-time.
* Shows whether responses are AI-generated or escalated to a human.

---

## 🧠 How the AI Works

* **Human-like Answers:** Responds in a warm, professional tone.
* **Keeps Context:** Looks at the last 5 messages to give meaningful answers.
* **FAQ Reference:** Answers common questions using `faqs.json`.
* **Escalation:** Offers to connect the user to a human agent if the issue is complex.
* **Short or Detailed Responses:** Use `concise` flag to control reply length.

---

## ⚙️ Running the Project Locally

```bash
uvicorn main:app --reload
```

* Chat UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


