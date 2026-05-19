import asyncio
import re
from datetime import date
import reflex as rx
import requests

API_URL = "http://127.0.0.1:8000/api/v1"
MAX_LOGIN_ATTEMPTS = 5
LOGIN_COOLDOWN_SECONDS = 30
DEFAULT_CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Shopping",
    "Health",
    "Education",
    "Travel",
    "Other",
]
MAX_CATEGORY_LENGTH = 20
MAX_AMOUNT_DIGITS = 10
MAX_AMOUNT_DECIMALS = 2

class AuthState(rx.State):
    token: str = rx.LocalStorage(name="auth_token")
    user_name: str = ""
    user_email: str = ""
    error_message: str = ""

    summary_total: str = "₱0.00"
    summary_total_value: float = 0.0
    summary_count: str = "0"
    summary_categories_count: str = "0"
    summary_categories: list[dict] = []
    category_options: list[str] = DEFAULT_CATEGORIES
    period_day_total: str = "₱0.00"
    period_week_total: str = "₱0.00"
    period_month_total: str = "₱0.00"
    expenses: list[dict] = []

    expenses_full: list[dict] = []
    expenses_filtered: list[dict] = []
    filtered_count: str = "0"
    has_filtered_expenses: bool = False
    filter_query: str = ""
    filter_category: str = ""
    filter_start_date: str = ""
    filter_end_date: str = ""

    selected_expense_id: int = 0
    selected_expense: dict = {
        "id": 0,
        "category": "",
        "amount": "",
        "amount_raw": 0.0,
        "date": "",
        "description": "",
    }
    expense_amount: str = ""
    expense_category: str = ""
    expense_date: str = ""
    expense_description: str = ""
    expense_form_error: str = ""
    expense_prev_total: str = "₱0.00"
    expense_next_total: str = "₱0.00"

    login_email: str = ""
    login_password: str = ""
    login_attempts: int = 0
    cooldown_remaining: int = 0

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

    def set_expense_amount(self, val: str):
        # 1. Prevent scientific notation (e/E) immediately
        if "e" in val.lower():
            return rx.set_value("amount_input", self.expense_amount)

        # 2. Basic cleaning - only digits and one dot
        cleaned = re.sub(r"[^0-9.]", "", val)
        if cleaned.count(".") > 1:
            return rx.set_value("amount_input", self.expense_amount)

        int_part, dot, dec_part = cleaned.partition(".")
        
        # 3. Strictly limit integer part to 10 digits
        truncated = False
        if len(int_part) > MAX_AMOUNT_DIGITS:
            int_part = int_part[:MAX_AMOUNT_DIGITS]
            truncated = True

        # 4. Limit decimal part to 2 digits
        if len(dec_part) > MAX_AMOUNT_DECIMALS:
            dec_part = dec_part[:MAX_AMOUNT_DECIMALS]
            truncated = True

        # 5. Reconstruct the value
        if dot:
            if not int_part:
                int_part = "0"
            new_val = f"{int_part}.{dec_part}"
        else:
            new_val = int_part
            
        # 6. Update state and totals
        self.expense_amount = new_val
        self._update_expense_totals()

        # 7. CRITICAL: If truncated or invalid, force the browser to match our state
        # This fixes the issue where the browser's internal buffer for type="number" 
        # gets out of sync with the React/Reflex state.
        if truncated or val != new_val:
            return rx.set_value("amount_input", new_val)

    def set_expense_category(self, val: str):
        self.expense_category = (val or "")[:MAX_CATEGORY_LENGTH]

    def set_expense_date(self, val: str):
        self.expense_date = val

    def set_expense_description(self, val: str):
        self.expense_description = (val or "")[:50]

    def set_filter_query(self, val: str):
        self.filter_query = val
        self.apply_expense_filters()

    def set_filter_category(self, val: str):
        self.filter_category = val
        self.apply_expense_filters()

    def set_filter_start_date(self, val: str):
        self.filter_start_date = val
        self.apply_expense_filters()

    def set_filter_end_date(self, val: str):
        self.filter_end_date = val
        self.apply_expense_filters()

    def clear_filters(self):
        self.filter_query = ""
        self.filter_category = ""
        self.filter_start_date = ""
        self.filter_end_date = ""
        self.apply_expense_filters()

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

    def _format_currency(self, value: float) -> str:
        return f"₱{value:,.2f}"

    def _merge_categories(self, defaults: list[str], custom: list[str]) -> list[str]:
        merged = []
        seen = set()
        for option in defaults + sorted(custom, key=lambda val: val.lower()):
            if not option:
                continue
            key = option.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            merged.append(option)
        return merged

    def _parse_amount(self, raw_value: str) -> float | None:
        try:
            value = float(raw_value)
        except Exception:
            return None
        if value <= 0:
            return None
        int_part, _, dec_part = raw_value.partition(".")
        if len(int_part) > MAX_AMOUNT_DIGITS:
            return None
        if len(dec_part) > MAX_AMOUNT_DECIMALS:
            return None
        return value

    def _update_expense_totals(self):
        amount = self._parse_amount(self.expense_amount)
        if amount is None:
            self.expense_next_total = self.expense_prev_total
            return
        new_total = self.summary_total_value + amount
        self.expense_next_total = self._format_currency(new_total)

    def reset_expense_form(self):
        self.expense_amount = ""
        self.expense_category = ""
        self.expense_description = ""
        self.expense_date = date.today().isoformat()
        self.expense_form_error = ""
        self.expense_prev_total = self.summary_total
        self.expense_next_total = self.summary_total

    @rx.event(background=True)
    async def run_cooldown(self):
        while True:
            await asyncio.sleep(1)
            async with self:
                if self.cooldown_remaining <= 0:
                    self.cooldown_remaining = 0
                    return
                self.cooldown_remaining -= 1

    def _start_login_cooldown(self, seconds: int | None = None):
        if seconds is not None and seconds > 0:
            self.cooldown_remaining = seconds
        else:
            self.cooldown_remaining = LOGIN_COOLDOWN_SECONDS
        self.login_attempts = 0
        return AuthState.run_cooldown

    def _record_login_failure(self):
        self.login_attempts += 1
        if self.login_attempts >= MAX_LOGIN_ATTEMPTS:
            return self._start_login_cooldown()
        return None

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
            self.summary_total_value = total
            self.summary_total = self._format_currency(total)
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
                    "total": self._format_currency(cat_total),
                    "count": str(item.get("count", 0)),
                })
            self.summary_categories = formatted
            self.expense_prev_total = self.summary_total
            self._update_expense_totals()
        except Exception:
            return self._toast_error("Could not load summary")

    def fetch_categories(self):
        headers = self._auth_headers()
        if headers is None:
            return
        try:
            resp = requests.get(f"{API_URL}/categories", headers=headers)
            if resp.status_code != 200:
                return self._toast_error(self._normalize_error(resp, "Failed to load categories"))
            data = resp.json() or []
            names = [item.get("name", "") for item in data if item.get("name")]
            self.category_options = self._merge_categories(DEFAULT_CATEGORIES, names)
        except Exception:
            return self._toast_error("Could not load categories")

    def fetch_period_summary(self):
        headers = self._auth_headers()
        if headers is None:
            return
        try:
            resp = requests.get(f"{API_URL}/summary/periods", headers=headers)
            if resp.status_code != 200:
                return self._toast_error(self._normalize_error(resp, "Failed to load period totals"))
            data = resp.json() or {}
            try:
                day_total = float(data.get("day_total", 0))
            except Exception:
                day_total = 0.0
            try:
                week_total = float(data.get("week_total", 0))
            except Exception:
                week_total = 0.0
            try:
                month_total = float(data.get("month_total", 0))
            except Exception:
                month_total = 0.0
            self.period_day_total = self._format_currency(day_total)
            self.period_week_total = self._format_currency(week_total)
            self.period_month_total = self._format_currency(month_total)
        except Exception:
            return self._toast_error("Could not load period totals")

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
                    "amount": self._format_currency(amount_val),
                    "date": item.get("date", ""),
                    "description": item.get("description", ""),
                })
            formatted.sort(key=lambda row: row.get("date", ""), reverse=True)
            self.expenses = formatted[:10]
        except Exception:
            return self._toast_error("Could not load expenses")

    def apply_expense_filters(self):
        query = self.filter_query.strip().lower()
        category = self.filter_category.strip().lower()
        start_date = self.filter_start_date.strip()
        end_date = self.filter_end_date.strip()

        filtered = []
        for item in self.expenses_full:
            item_category = (item.get("category") or "").lower()
            item_description = (item.get("description") or "").lower()
            item_date = item.get("date") or ""

            if category and category not in item_category:
                continue
            if query and query not in item_category and query not in item_description:
                continue
            if start_date and item_date and item_date < start_date:
                continue
            if end_date and item_date and item_date > end_date:
                continue

            filtered.append(item)

        self.expenses_filtered = filtered
        self.filtered_count = str(len(filtered))
        self.has_filtered_expenses = len(filtered) > 0

    def fetch_expense_list(self):
        headers = self._auth_headers()
        if headers is None:
            return None
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
                    "amount": self._format_currency(amount_val),
                    "amount_raw": amount_val,
                    "date": item.get("date", ""),
                    "description": item.get("description", ""),
                })
            formatted.sort(key=lambda row: row.get("date", ""), reverse=True)
            self.expenses_full = formatted
            self.apply_expense_filters()
        except Exception:
            return self._toast_error("Could not load expenses")
        return None

    def fetch_expense_detail(self, expense_id: int):
        headers = self._auth_headers()
        if headers is None:
            return None
        try:
            resp = requests.get(f"{API_URL}/expenses/{expense_id}", headers=headers)
            if resp.status_code != 200:
                return self._toast_error(self._normalize_error(resp, "Expense not found"))
            data = resp.json() or {}
            try:
                amount_val = float(data.get("amount", 0))
            except Exception:
                amount_val = 0.0
            self.selected_expense = {
                "id": data.get("id"),
                "category": data.get("category", "Uncategorized"),
                "amount": self._format_currency(amount_val),
                "amount_raw": amount_val,
                "date": data.get("date", ""),
                "description": data.get("description", ""),
            }
        except Exception:
            return self._toast_error("Could not load expense")
        return None

    def load_expense_list(self):
        redirect = self.check_auth()
        if redirect is not None:
            return redirect
        return self.fetch_expense_list()

    def load_add_expense(self):
        redirect = self.check_auth()
        if redirect is not None:
            return redirect
        self.selected_expense_id = 0
        self.fetch_summary()
        self.fetch_categories()
        self.reset_expense_form()

    def load_expense_detail(self):
        redirect = self.check_auth()
        if redirect is not None:
            return redirect
        if not self.selected_expense_id:
            return rx.redirect("/expenses")
        return self.fetch_expense_detail(self.selected_expense_id)

    def load_edit_expense(self):
        redirect = self.check_auth()
        if redirect is not None:
            return redirect
        if not self.selected_expense_id:
            return rx.redirect("/expenses")
        self.fetch_categories()
        result = self.fetch_expense_detail(self.selected_expense_id)
        if result is not None:
            return result
        self.expense_amount = str(self.selected_expense.get("amount_raw", ""))
        self.expense_category = self.selected_expense.get("category", "")
        self.expense_date = self.selected_expense.get("date", "")
        self.expense_description = self.selected_expense.get("description", "")
        self.expense_form_error = ""

    def load_delete_expense(self):
        redirect = self.check_auth()
        if redirect is not None:
            return redirect
        if not self.selected_expense_id:
            return rx.redirect("/expenses")
        return self.fetch_expense_detail(self.selected_expense_id)

    def create_expense(self):
        amount_val = self._parse_amount(self.expense_amount)
        if amount_val is None:
            return self._toast_error("Enter a valid amount between 0 and 1,000,000,000.")
        category_name = self.expense_category.strip()
        if not category_name:
            return self._toast_error("Category is required.")
        if len(category_name) > MAX_CATEGORY_LENGTH:
            return self._toast_error("Category must be 20 characters or fewer.")
        if not self.expense_date:
            return self._toast_error("Date is required.")

        headers = self._auth_headers()
        if headers is None:
            return rx.redirect("/login")
        try:
            resp = requests.post(
                f"{API_URL}/expenses",
                headers=headers,
                json={
                    "amount": amount_val,
                    "category": category_name,
                    "description": self.expense_description or "",
                    "date": self.expense_date,
                },
            )
            if resp.status_code in (200, 201):
                self.error_message = ""
                return rx.redirect("/dashboard")
            return self._toast_error(self._normalize_error(resp, "Failed to create expense"))
        except Exception:
            return self._toast_error("Could not connect to backend")

    def update_expense(self):
        if not self.selected_expense_id:
            return self._toast_error("Select an expense to update.")
        amount_val = self._parse_amount(self.expense_amount)
        if amount_val is None:
            return self._toast_error("Enter a valid amount between 0 and 1,000,000,000.")
        category_name = self.expense_category.strip()
        if not category_name:
            return self._toast_error("Category is required.")
        if len(category_name) > MAX_CATEGORY_LENGTH:
            return self._toast_error("Category must be 20 characters or fewer.")
        if not self.expense_date:
            return self._toast_error("Date is required.")

        headers = self._auth_headers()
        if headers is None:
            return rx.redirect("/login")
        try:
            resp = requests.put(
                f"{API_URL}/expenses/{self.selected_expense_id}",
                headers=headers,
                json={
                    "amount": amount_val,
                    "category": category_name,
                    "description": self.expense_description or "",
                    "date": self.expense_date,
                },
            )
            if resp.status_code == 200:
                self.error_message = ""
                return rx.redirect("/dashboard")
            return self._toast_error(self._normalize_error(resp, "Failed to update expense"))
        except Exception:
            return self._toast_error("Could not connect to backend")

    def delete_expense(self):
        if not self.selected_expense_id:
            return self._toast_error("Select an expense to delete.")
        headers = self._auth_headers()
        if headers is None:
            return rx.redirect("/login")
        try:
            resp = requests.delete(
                f"{API_URL}/expenses/{self.selected_expense_id}",
                headers=headers,
            )
            if resp.status_code in (200, 204):
                self.error_message = ""
                self.selected_expense_id = 0
                return rx.redirect("/dashboard")
            return self._toast_error(self._normalize_error(resp, "Failed to delete expense"))
        except Exception:
            return self._toast_error("Could not connect to backend")

    def go_to_add(self):
        self.selected_expense_id = 0
        return rx.redirect("/expenses/new")

    def go_to_view(self, expense_id: int):
        self.selected_expense_id = expense_id
        return rx.redirect("/expenses/view")

    def go_to_edit(self, expense_id: int):
        self.selected_expense_id = expense_id
        return rx.redirect("/expenses/edit")

    def go_to_delete(self, expense_id: int):
        self.selected_expense_id = expense_id
        return rx.redirect("/expenses/delete")

    def load_dashboard(self):
        redirect = self.check_auth()
        if redirect is not None:
            return redirect
        self.fetch_summary()
        self.fetch_period_summary()
        self.fetch_expenses()

    def login(self):
        if not self.login_email or not self.login_password:
            return self._toast_error("Email and password are required.")
        if self.cooldown_remaining > 0:
            return self._toast_error(
                f"Too many failed attempts. Try again in {self.cooldown_remaining}s."
            )
        try:
            resp = requests.post(f"{API_URL}/auth/login", json={
                "email": self.login_email,
                "password": self.login_password
            })
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                self.error_message = ""
                self.login_attempts = 0
                self.cooldown_remaining = 0
                return rx.redirect("/dashboard")
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                try:
                    retry_seconds = int(retry_after) if retry_after else LOGIN_COOLDOWN_SECONDS
                except Exception:
                    retry_seconds = LOGIN_COOLDOWN_SECONDS
                cooldown_event = self._start_login_cooldown(retry_seconds)
                return [
                    self._toast_error(self._normalize_error(resp, "Too many requests")),
                    cooldown_event,
                ]
            if resp.status_code == 401:
                cooldown_event = self._record_login_failure()
                if cooldown_event is not None:
                    return [
                        self._toast_error(
                            f"Too many failed attempts. Try again in {self.cooldown_remaining}s."
                        ),
                        cooldown_event,
                    ]
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
        return rx.redirect("/")
