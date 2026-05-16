import reflex as rx

# Import pages so that Reflex registers them during compilation
from Expense_Tracker_Frontend import (
    login,
    signup,
    dashboard,
    expenses,
    expense_form,
    expense_detail,
    expense_delete,
    landing,
)

@rx.page(route="/")
def index() -> rx.Component:
    return landing.landing_page()

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap",
    ],
)
