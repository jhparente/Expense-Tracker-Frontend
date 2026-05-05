import reflex as rx

# Import pages so that Reflex registers them during compilation
from .pages import login, signup, dashboard

@rx.page(route="/")
def index() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            top="-140px",
            left="-140px",
            width="360px",
            height="360px",
            background="radial-gradient(circle, rgba(94, 234, 212, 0.35), rgba(94, 234, 212, 0))",
            filter="blur(10px)",
        ),
        rx.box(
            position="absolute",
            bottom="-160px",
            right="-140px",
            width="420px",
            height="420px",
            background="radial-gradient(circle, rgba(56, 189, 248, 0.35), rgba(56, 189, 248, 0))",
            filter="blur(12px)",
        ),
        rx.center(
            rx.vstack(
                rx.heading(
                    "Expense Tracker",
                    size="9",
                    weight="bold",
                    color="white",
                ),
                rx.text(
                    "A clean, modern way to manage spending and stay on budget.",
                    color="#94a3b8",
                    size="4",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "Create account",
                            padding="0.9rem 1.4rem",
                            border_radius="14px",
                            background="linear-gradient(90deg, #5eead4, #38bdf8)",
                            color="white",
                        ),
                        href="/signup",
                    ),
                    rx.link(
                        rx.button(
                            "Login",
                            padding="0.9rem 1.4rem",
                            border_radius="14px",
                            background="rgba(148, 163, 184, 0.16)",
                            color="white",
                            border="1px solid rgba(148, 163, 184, 0.35)",
                        ),
                        href="/login",
                    ),
                    spacing="4",
                ),
                spacing="5",
                align_items="center",
                text_align="center",
            ),
            height="100vh",
            padding="2rem",
            position="relative",
            z_index="1",
        ),
        min_height="100vh",
        background="linear-gradient(135deg, #0a1017 0%, #0f1c2c 45%, #0a1017 100%)",
        position="relative",
        overflow="hidden",
        font_family='"Space Grotesk", "Segoe UI", sans-serif',
    )

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap"
    ]
)
