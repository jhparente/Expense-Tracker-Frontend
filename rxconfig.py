import reflex as rx

config = rx.Config(
    app_name="Expense_Tracker_Frontend",
    api_url="http://127.0.0.1:8001",
    backend_port=8001,
    frontend_port=3000,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)