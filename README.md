# Expense Tracker Frontend (Reflex)

A modern Reflex frontend for the Expense Tracker backend. This UI handles login, signup, and a dashboard that loads real expenses and summary data from the API.

## Requirements

- Python 3.10+
- Backend running from the `Expense-Tracker` folder

## Setup (Windows)

1. Open a terminal in this folder:

   ```powershell
   cd "C:\Users\hp\Documents\PT 101-Platform Technologies\Expense-Tracker-Frontend"
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Run the Backend

From the backend folder, start FastAPI on port 8000:

```powershell
cd "C:\Users\hp\Documents\PT 101-Platform Technologies\Expense-Tracker"
uvicorn app:app --reload
```

## Run the Frontend

Start the Reflex app:

```powershell
cd "C:\Users\hp\Documents\PT 101-Platform Technologies\Expense-Tracker-Frontend"
venv\Scripts\activate
reflex run
```

The UI is available at:

- http://localhost:3000

Reflex uses its own backend for state updates and websockets, configured at:

- http://127.0.0.1:8001

## Configuration

The frontend talks to the API here:

- `Expense_Tracker_Frontend/state.py` -> `API_URL = "http://127.0.0.1:8000"`

If you change the backend port, update `API_URL` to match.

## Backend Endpoints Used

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `GET /summary`
- `GET /expenses`

## Troubleshooting

- If you see websocket errors for `/_event`, ensure FastAPI is on port 8000 and Reflex is on port 8001.
- If the UI cannot reach the backend, verify `API_URL` in `state.py` and make sure FastAPI is running.
