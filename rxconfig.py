import reflex as rx

config = rx.Config(
    app_name="Expense_Tracker_Frontend",
    # Ports and API URL are dynamically configured for single-port deployment
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)