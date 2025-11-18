# Busy Budgeters — Budgeting Buddy

A clean, interactive budgeting projection tool that helps users estimate savings growth using compound interest.  
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

## 🔧 Backend Integration

The frontend is already structured to call a backend API:

```js
const BACKEND_URL = "";
const USE_BACKEND = false;
To connect a backend:

Set BACKEND_URL = "https://api-server.com".

Set USE_BACKEND = true.

Implement the /api/calculate endpoint to accept:

json
Copy code
{
  "balance": number,
  "deposit": number,
  "months": number,
  "bank": string,
  "accountType": string,
  "rate": number
}
If the backend is offline or returns incomplete data, the system automatically falls back to local projection mode.

📂 Project Structure
bash
Copy code
/
├── Busy Budgeters — Budgeting Buddy.html   # Main frontend app
└── README.md
(Optional: Add a /public or /assets folder later if you include images or icons.)

🚀 Running the Project
This project is fully client-side and requires no build step.

Option 1 — Double-click to open
Just open the HTML file in any browser:

nginx
Copy code
Busy Budgeters — Budgeting Buddy.html
Option 2 — Serve locally
If you want clean paths or plan to add backend:

bash
Copy code
npx serve .
or with Python:

bash
Copy code
python3 -m http.server
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