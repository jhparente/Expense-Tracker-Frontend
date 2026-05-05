import reflex as rx
from .state import AuthState


def stat_card(title: str, value: str, subtitle: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(title, size="2", color="#94a3b8"),
            rx.heading(value, size="6", weight="bold", color="white"),
            rx.text(subtitle, size="1", color="#64748b"),
            spacing="2",
            align_items="start",
        ),
        padding="1.4rem",
        border_radius="18px",
        background="rgba(15, 18, 28, 0.75)",
        border="1px solid rgba(148, 163, 184, 0.2)",
        box_shadow="0 20px 45px rgba(0, 0, 0, 0.35)",
    )


def expense_row(expense) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(expense["category"], weight="medium", color="white"),
            rx.cond(
                expense["description"] != "",
                rx.text(expense["description"], size="2", color="#94a3b8"),
                rx.text("No description", size="2", color="#64748b"),
            ),
            spacing="1",
            align_items="start",
        ),
        rx.spacer(),
        rx.vstack(
            rx.text(expense["amount"], weight="bold", color="white"),
            rx.text(expense["date"], size="2", color="#94a3b8"),
            spacing="1",
            align_items="end",
        ),
        padding="0.9rem 0",
        border_bottom="1px solid rgba(148, 163, 184, 0.12)",
        width="100%",
    )


def category_row(category) -> rx.Component:
    return rx.hstack(
        rx.text(category["category"], color="white", weight="medium"),
        rx.spacer(),
        rx.hstack(
            rx.text(category["count"], size="2", color="#94a3b8"),
            rx.text("items", size="2", color="#94a3b8"),
            spacing="1",
            align_items="center",
        ),
        rx.text(category["total"], weight="bold", color="white"),
        spacing="3",
        width="100%",
    )


def navbar() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.box(
                width="42px",
                height="42px",
                border_radius="14px",
                background="linear-gradient(135deg, #5eead4, #38bdf8)",
            ),
            rx.vstack(
                rx.text("Expense Tracker", size="2", color="#94a3b8"),
                rx.text("Dashboard", weight="bold", color="white"),
                spacing="1",
                align_items="start",
            ),
            spacing="3",
            align_items="center",
        ),
        rx.spacer(),
        rx.hstack(
            rx.text(AuthState.user_name, color="white", weight="medium"),
            rx.button(
                "Logout",
                on_click=AuthState.logout,
                padding="0.5rem 1rem",
                border_radius="999px",
                background="rgba(248, 113, 113, 0.15)",
                color="#fca5a5",
                border="1px solid rgba(248, 113, 113, 0.35)",
            ),
            spacing="3",
        ),
        padding="1.2rem 2.4rem",
        border_bottom="1px solid rgba(148, 163, 184, 0.2)",
        background="rgba(8, 11, 18, 0.9)",
        position="sticky",
        top="0",
        z_index="5",
        backdrop_filter="blur(12px)",
    )


@rx.page(route="/dashboard", on_load=AuthState.load_dashboard)
def dashboard() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            top="-160px",
            left="-160px",
            width="420px",
            height="420px",
            background="radial-gradient(circle, rgba(94, 234, 212, 0.3), rgba(94, 234, 212, 0))",
            filter="blur(12px)",
        ),
        rx.box(
            position="absolute",
            bottom="-180px",
            right="-160px",
            width="480px",
            height="480px",
            background="radial-gradient(circle, rgba(56, 189, 248, 0.25), rgba(56, 189, 248, 0))",
            filter="blur(12px)",
        ),
        navbar(),
        rx.container(
            rx.vstack(
                rx.grid(
                    stat_card("Total spent", AuthState.summary_total, "All time"),
                    stat_card("Transactions", AuthState.summary_count, "Recorded expenses"),
                    stat_card("Categories", AuthState.summary_categories_count, "Unique categories"),
                    columns="3",
                    spacing="4",
                    width="100%",
                ),
                rx.grid(
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.heading("Recent expenses", size="5", weight="bold", color="white"),
                                rx.spacer(),
                                rx.text("Last 10 entries", size="2", color="#94a3b8"),
                                width="100%",
                            ),
                            rx.cond(
                                AuthState.summary_count == "0",
                                rx.text("No expenses yet", color="#94a3b8", size="2"),
                                rx.vstack(
                                    rx.foreach(AuthState.expenses, expense_row),
                                    spacing="0",
                                    width="100%",
                                ),
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="1.5rem",
                        border_radius="20px",
                        background="rgba(15, 18, 28, 0.75)",
                        border="1px solid rgba(148, 163, 184, 0.2)",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading("Category breakdown", size="5", weight="bold", color="white"),
                            rx.cond(
                                AuthState.summary_categories_count == "0",
                                rx.text("No categories yet", color="#94a3b8", size="2"),
                                rx.vstack(
                                    rx.foreach(AuthState.summary_categories, category_row),
                                    spacing="3",
                                    width="100%",
                                ),
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="1.5rem",
                        border_radius="20px",
                        background="rgba(15, 18, 28, 0.75)",
                        border="1px solid rgba(148, 163, 184, 0.2)",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                spacing="5",
                width="100%",
            ),
            max_width="1100px",
            padding="2.5rem 1.5rem 4rem",
        ),
        min_height="100vh",
        background="linear-gradient(135deg, #0a1017 0%, #0f1c2c 45%, #0a1017 100%)",
        position="relative",
        overflow="hidden",
        font_family='"Space Grotesk", "Segoe UI", sans-serif',
    )
