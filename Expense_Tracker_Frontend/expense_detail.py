import reflex as rx
from Expense_Tracker_Frontend.state import AuthState
from Expense_Tracker_Frontend.dashboard import navbar


def detail_row(label: str, value) -> rx.Component:
    return rx.hstack(
        rx.text(label, size="2", color="#94a3b8"),
        rx.spacer(),
        rx.text(value, size="3", color="white"),
        width="100%",
    )


@rx.page(route="/expenses/view", on_load=AuthState.load_expense_detail)
def expense_detail_page() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            top="-160px",
            left="-160px",
            width="420px",
            height="420px",
            background="radial-gradient(circle, rgba(56, 189, 248, 0.25), rgba(56, 189, 248, 0))",
            filter="blur(12px)",
        ),
        rx.box(
            position="absolute",
            bottom="-180px",
            right="-160px",
            width="480px",
            height="480px",
            background="radial-gradient(circle, rgba(14, 116, 144, 0.2), rgba(14, 116, 144, 0))",
            filter="blur(12px)",
        ),
        navbar("Expenses"),
        rx.container(
            rx.center(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Expense details", size="6", weight="bold", color="white"),
                        rx.spacer(),
                        rx.link("Back to expenses", href="/expenses", color="#7dd3fc"),
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            detail_row("Category", AuthState.selected_expense["category"]),
                            detail_row("Amount", AuthState.selected_expense["amount"]),
                            detail_row("Date", AuthState.selected_expense["date"]),
                            detail_row(
                                "Description",
                                AuthState.selected_expense["description"],
                            ),
                            rx.hstack(
                                rx.button(
                                    "Edit",
                                    on_click=AuthState.go_to_edit(AuthState.selected_expense_id),
                                    padding="0.5rem 1rem",
                                    border_radius="999px",
                                    background="rgba(251, 191, 36, 0.15)",
                                    border="1px solid rgba(251, 191, 36, 0.35)",
                                    color="#facc15",
                                ),
                                rx.button(
                                    "Delete",
                                    on_click=AuthState.go_to_delete(AuthState.selected_expense_id),
                                    padding="0.5rem 1rem",
                                    border_radius="999px",
                                    background="rgba(248, 113, 113, 0.15)",
                                    border="1px solid rgba(248, 113, 113, 0.35)",
                                    color="#fca5a5",
                                ),
                                spacing="3",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="1.8rem",
                        border_radius="20px",
                        background="rgba(15, 18, 28, 0.75)",
                        border="1px solid rgba(148, 163, 184, 0.2)",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="1080px",
                ),
                width="100%",
            ),
            max_width="100%",
            padding="2.5rem 3.5rem 4rem",
        ),
        min_height="100vh",
        background="linear-gradient(135deg, #0a1017 0%, #0f1c2c 45%, #0a1017 100%)",
        position="relative",
        overflow="hidden",
        font_family='"Space Grotesk", "Segoe UI", sans-serif',
    )
