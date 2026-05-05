import reflex as rx
import requests

API_URL = "http://127.0.0.1:8000"

class AuthState(rx.State):
    token: str = rx.LocalStorage(name="auth_token")
    user_name: str = ""
    user_email: str = ""
    error_message: str = ""

    summary_total: str = "₱0.00"
    summary_count: str = "0"
    summary_categories_count: str = "0"
    summary_categories: list[dict] = []
    expenses: list[dict] = []

    login_email: str = ""
    login_password: str = ""

    reg_name: str = ""
    reg_email: str = ""
    reg_password: str = ""

    def set_login_email(self, val: str):
        self.login_email = val

    def set_login_password(self, val: str):
        self.login_password = val

    def set_reg_name(self, val: str):
        self.reg_name = val

    def set_reg_email(self, val: str):
        self.reg_email = val

    def set_reg_password(self, val: str):
        self.reg_password = val

    def _normalize_error(self, resp: requests.Response, fallback: str) -> str:
        try:
            data = resp.json()
        except Exception:
            return fallback

        detail = data.get("detail")
        if isinstance(detail, str):
            return detail
        if isinstance(detail, list):
            messages = []
            for item in detail:
                if isinstance(item, dict):
                    msg = item.get("msg") or item.get("message")
                    if msg:
                        messages.append(msg)
            if messages:
                return "; ".join(messages)
        if isinstance(detail, dict):
            msg = detail.get("msg") or detail.get("message")
            if msg:
                return msg
        if detail is not None:
            return str(detail)

        return fallback

    def _toast_error(self, message: str):
        self.error_message = message
        return rx.toast(
            message,
            level="error",
            position="top-left",
            duration=5000,
        )

    def _auth_headers(self) -> dict | None:
        if not self.token:
            return None
        return {"Authorization": f"Bearer {self.token}"}

    def check_auth(self):
        if not self.token:
            return rx.redirect("/login")
        headers = self._auth_headers()
        if headers is None:
            return rx.redirect("/login")
        try:
            resp = requests.get(f"{API_URL}/auth/me", headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                self.user_name = data.get("name", "")
                self.user_email = data.get("email", "")
            else:
                self.token = ""
                return rx.redirect("/login")
        except Exception:
            return self._toast_error("Could not connect to backend")

    def fetch_summary(self):
        headers = self._auth_headers()
        if headers is None:
            return
        try:
            resp = requests.get(f"{API_URL}/summary", headers=headers)
            if resp.status_code != 200:
                return self._toast_error(self._normalize_error(resp, "Failed to load summary"))
            data = resp.json()
            try:
                total = float(data.get("total_spent", 0))
            except Exception:
                total = 0.0
            self.summary_total = f"₱{total:,.2f}"
            self.summary_count = str(data.get("transaction_count", 0))
            categories = data.get("categories", []) or []
            self.summary_categories_count = str(len(categories))
            formatted = []
            for item in categories:
                try:
                    cat_total = float(item.get("total", 0))
                except Exception:
                    cat_total = 0.0
                formatted.append({
                    "category": item.get("category", "Uncategorized"),
                    "total": f"₱{cat_total:,.2f}",
                    "count": str(item.get("count", 0)),
                })
            self.summary_categories = formatted
        except Exception:
            return self._toast_error("Could not load summary")

    def fetch_expenses(self):
        headers = self._auth_headers()
        if headers is None:
            return
        try:
            resp = requests.get(f"{API_URL}/expenses", headers=headers)
            if resp.status_code != 200:
                return self._toast_error(self._normalize_error(resp, "Failed to load expenses"))
            data = resp.json() or []
            formatted = []
            for item in data:
                try:
                    amount_val = float(item.get("amount", 0))
                except Exception:
                    amount_val = 0.0
                formatted.append({
                    "id": item.get("id"),
                    "category": item.get("category", "Uncategorized"),
                    "amount": f"₱{amount_val:,.2f}",
                    "date": item.get("date", ""),
                    "description": item.get("description", ""),
                })
            formatted.sort(key=lambda row: row.get("date", ""), reverse=True)
            self.expenses = formatted[:10]
        except Exception:
            return self._toast_error("Could not load expenses")

    def load_dashboard(self):
        redirect = self.check_auth()
        if redirect is not None:
            return redirect
        self.fetch_summary()
        self.fetch_expenses()

    def login(self):
        if not self.login_email or not self.login_password:
            return self._toast_error("Email and password are required.")
        try:
            resp = requests.post(f"{API_URL}/auth/login", json={
                "email": self.login_email,
                "password": self.login_password
            })
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                self.error_message = ""
                return rx.redirect("/dashboard")
            else:
                return self._toast_error(self._normalize_error(resp, "Login failed"))
        except Exception:
            return self._toast_error("Could not connect to backend")

    def register(self):
        if not self.reg_name or not self.reg_email or not self.reg_password:
            return self._toast_error("Name, email, and password are required.")
        try:
            resp = requests.post(f"{API_URL}/auth/register", json={
                "name": self.reg_name,
                "email": self.reg_email,
                "password": self.reg_password
            })
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                self.error_message = ""
                return rx.redirect("/dashboard")
            else:
                return self._toast_error(self._normalize_error(resp, "Registration failed"))
        except Exception:
            return self._toast_error("Could not connect to backend")
            
    def logout(self):
        self.token = ""
        self.user_name = ""
        return rx.redirect("/login")
