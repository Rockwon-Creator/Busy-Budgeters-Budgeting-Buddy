# Busy Budgeters — Budgeting Buddy

A clean, interactive budgeting projection tool that helps users estimate savings growth using compound interest.  
This version includes full backend support using FastAPI for accurate compound‑interest projections.  
This project includes a fully functional **frontend** interface and is ready for **backend integration** via a simple configuration toggle.

---

## ✨ Features

### 🎛️ Budget Modes
The tool supports three calculation modes:

1. **Final Balance**  
   → Predict your savings after a fixed period.

2. **Time to Goal**  
   → Calculate how many months you need to reach a target balance.

3. **Required Deposit**  
   → Compute the monthly deposit needed to hit a goal within a set time.

### 📊 Data Visualization
- Live line chart (Chart.js)
- Monthly balance projection
- KPI summary for:
  - Total balance
  - Total contributions
  - Interest earned

### 🏦 Bank + APR Auto-Fill
- Preloaded banks and savings accounts with typical APR values.
- APR auto-syncs based on bank and account type.
- User can override APR manually.

### 🧱 Fully Client-Side (Frontend)
- Pure HTML + CSS + JavaScript
- Uses Chart.js for rendering
- Responsive, mobile-friendly UI
- Gradient and blurred-glass effects for modern look

---

## 🔧 Backend Integration (FastAPI)

The project now supports **full backend computation** using a FastAPI server.

### How to enable backend mode
In the frontend (`index.html`), update the configuration block:

```js
const BACKEND_URL = "https://your-render-backend-url.onrender.com";
const USE_BACKEND = true;
```

### Expected API Endpoint
The backend must expose the following endpoint:

```
POST /api/calculate
```

### Request Body
```json
{
  "mode": "final" | "time" | "deposit",
  "balance": number,
  "deposit": number,
  "months": number,
  "rate": number,
  "goal": number | null
}
```

### Response Format
```json
{
  "series": [number],
  "total": number,
  "contrib": number,
  "interestEarned": number,
  "monthsNeeded": number | null,
  "requiredDeposit": number | null
}
```

The backend handles all compound‑interest calculations, and the frontend displays the projected monthly balances, KPIs, and charts.

📂 Project Structure
```
/
├── Backend/
│   ├── app.py                  # FastAPI server (live endpoint: /api/calculate)
│   ├── BudgetingBuddy.py       # Core compound‑interest logic
│   ├── requirements.txt        # Render deployment
│
├── Frontend/
│   ├── index.html              # Main UI (Chart.js + client logic)
│
└── README.md
```

🚀 Running the Project

## Frontend (Vercel-ready)
No build step required. You can run it by opening:

```
index.html
```

or serving it locally:

```bash
npx serve .
# or
python3 -m http.server
```

## Backend (FastAPI)
From the `/Backend` directory:

```bash
uvicorn app:app --reload
```

Production deployment is configured for **Render** with:

```
uvicorn app:app --host 0.0.0.0 --port 8000
```
🧩 Tech Stack
Component	Technology
UI	HTML / CSS / JS
Styling	Custom theme tokens (dark mode)
Charts	Chart.js 4.4
Backend-ready	Fetch API (optional toggle)

📈 Future Enhancements (Planned)
Supabase authentication

Save user profiles

Store projections in database

CSV import/export

Real bank/APR API integration

Mobile-first redesign

Vercel deployment

📜 License
MIT License — feel free to use, modify, and extend.

👤 Author
Rockwon Seo
Frontend & System Integration Lead
University at Albany, SUNY