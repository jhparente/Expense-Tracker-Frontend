import reflex as rx
from Expense_Tracker_Frontend.state import AuthState


def input_block(label: str, placeholder: str, on_change, input_type: str = "text") -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color="#cbd5e1"),
        rx.input(
            placeholder=placeholder,
            type=input_type,
            on_change=on_change,
            width="100%",
            height="48px",
            padding_left="1rem",
            padding_right="1rem",
            padding_top="0.65rem",
            padding_bottom="0.65rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.04)",
            border="1px solid rgba(148, 163, 184, 0.25)",
            color="white",
            font_size="1rem",
            line_height="1.2",
        ),
        spacing="1",
        width="100%",
    )


@rx.page(route="/login")
def login_page() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            top="-120px",
            left="-120px",
            width="360px",
            height="360px",
            background="radial-gradient(circle, rgba(34, 211, 238, 0.35), rgba(34, 211, 238, 0))",
            filter="blur(8px)",
        ),
        rx.box(
            position="absolute",
            bottom="-160px",
            right="-120px",
            width="420px",
            height="420px",
            background="radial-gradient(circle, rgba(59, 130, 246, 0.35), rgba(59, 130, 246, 0))",
            filter="blur(10px)",
        ),
        rx.center(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            width="44px",
                            height="44px",
                            border_radius="14px",
                            background="linear-gradient(135deg, #22d3ee, #3b82f6)",
                        ),
                        rx.vstack(
                            rx.text("Expense Tracker", size="2", color="#94a3b8"),
                            rx.heading("Welcome back", size="7", weight="bold", color="white"),
                            spacing="1",
                            align_items="start",
                        ),
                        spacing="3",
                        align_items="center",
                    ),
                    rx.text(
                        "Sign in to keep your expenses organized and in sync.",
                        color="#94a3b8",
                        size="3",
                    ),
                    rx.cond(
                        AuthState.cooldown_remaining > 0,
                        rx.box(
                            rx.text(
                                "Too many failed attempts. Try again in ",
                                AuthState.cooldown_remaining,
                                "s.",
                                color="#fca5a5",
                                size="2",
                                weight="medium",
                            ),
                            width="100%",
                            padding="0.6rem 0.9rem",
                            border_radius="12px",
                            background="rgba(248, 113, 113, 0.12)",
                            border="1px solid rgba(248, 113, 113, 0.3)",
                        ),
                        rx.box(),
                    ),
                    input_block("Email", "you@domain.com", AuthState.set_login_email),
                    input_block("Password", "Your password", AuthState.set_login_password, "password"),
                    rx.cond(
                        AuthState.cooldown_remaining > 0,
                        rx.button(
                            "Log in",
                            width="100%",
                            padding="0.9rem",
                            border_radius="14px",
                            background="rgba(148, 163, 184, 0.2)",
                            color="#94a3b8",
                            cursor="not-allowed",
                        ),
                        rx.button(
                            "Log in",
                            on_click=AuthState.login,
                            width="100%",
                            padding="0.9rem",
                            border_radius="14px",
                            background="linear-gradient(90deg, #22d3ee, #3b82f6)",
                            color="white",
                        ),
                    ),
                    rx.text(
                        "New here? ",
                        rx.link("Create an account", href="/signup", color="#38bdf8"),
                        color="#94a3b8",
                        size="2",
                    ),
                    spacing="4",
                    align_items="start",
                    width="100%",
                ),
                padding="2.8rem",
                width="100%",
                max_width="460px",
                background="rgba(15, 18, 28, 0.78)",
                border="1px solid rgba(148, 163, 184, 0.2)",
                border_radius="28px",
                box_shadow="0 30px 70px rgba(0, 0, 0, 0.55)",
                backdrop_filter="blur(18px)",
            ),
            height="100vh",
            padding="2rem",
            position="relative",
            z_index="1",
        ),
        min_height="100vh",
        background="linear-gradient(135deg, #0b0f1a 0%, #101827 45%, #0b0f1a 100%)",
        position="relative",
        overflow="hidden",
        font_family='"Space Grotesk", "Segoe UI", sans-serif',
    )
