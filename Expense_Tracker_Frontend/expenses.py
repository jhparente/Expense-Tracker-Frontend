import reflex as rx
from Expense_Tracker_Frontend.state import AuthState
from Expense_Tracker_Frontend.dashboard import navbar


def filter_input(label: str, placeholder: str, on_change, input_type: str = "text") -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color="#cbd5e1"),
        rx.input(
            placeholder=placeholder,
            type=input_type,
            on_change=on_change,
            width="100%",
            height="42px",
            padding_left="0.9rem",
            padding_right="0.9rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.04)",
            border="1px solid rgba(148, 163, 184, 0.25)",
            color="white",
            font_size="0.95rem",
            line_height="1.2",
        ),
        spacing="1",
        width="100%",
    )


def expense_action_button(label: str, on_click, tone: str) -> rx.Component:
    tone_styles = {
        "view": {
            "background": "rgba(56, 189, 248, 0.15)",
            "border": "1px solid rgba(56, 189, 248, 0.35)",
            "color": "#7dd3fc",
        },
        "edit": {
            "background": "rgba(251, 191, 36, 0.15)",
            "border": "1px solid rgba(251, 191, 36, 0.35)",
            "color": "#facc15",
        },
        "delete": {
            "background": "rgba(248, 113, 113, 0.15)",
            "border": "1px solid rgba(248, 113, 113, 0.35)",
            "color": "#fca5a5",
        },
    }
    style = tone_styles.get(tone, tone_styles["view"])
    return rx.button(
        label,
        on_click=on_click,
        padding="0.35rem 0.85rem",
        border_radius="999px",
        background=style["background"],
        border=style["border"],
        color=style["color"],
    )


def expense_row(expense: dict) -> rx.Component:
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
        rx.hstack(
            expense_action_button("View", AuthState.go_to_view(expense["id"]), "view"),
            expense_action_button("Edit", AuthState.go_to_edit(expense["id"]), "edit"),
            expense_action_button("Delete", AuthState.go_to_delete(expense["id"]), "delete"),
            spacing="2",
        ),
        padding="0.9rem 0",
        border_bottom="1px solid rgba(148, 163, 184, 0.12)",
        width="100%",
        align_items="center",
    )


@rx.page(route="/expenses", on_load=AuthState.load_expense_list)
def expenses_page() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            top="-160px",
            left="-160px",
            width="420px",
            height="420px",
            background="radial-gradient(circle, rgba(59, 130, 246, 0.25), rgba(59, 130, 246, 0))",
            filter="blur(12px)",
        ),
        rx.box(
            position="absolute",
            bottom="-180px",
            right="-160px",
            width="480px",
            height="480px",
            background="radial-gradient(circle, rgba(14, 165, 233, 0.2), rgba(14, 165, 233, 0))",
            filter="blur(12px)",
        ),
        navbar("Expenses"),
        rx.container(
            rx.center(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Expenses", size="7", weight="bold", color="white"),
                            rx.text(
                                "Review, search, and manage all expenses in one place.",
                                size="3",
                                color="#94a3b8",
                            ),
                            spacing="1",
                            align_items="start",
                        ),
                        rx.spacer(),
                        rx.button(
                            "Add expense",
                            on_click=AuthState.go_to_add,
                            padding="0.85rem 1.2rem",
                            border_radius="14px",
                            background="linear-gradient(90deg, #22d3ee, #3b82f6)",
                            color="white",
                        ),
                        align_items="center",
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.heading("Filters", size="4", color="white"),
                                rx.spacer(),
                                rx.text(AuthState.filtered_count, " results", size="2", color="#94a3b8"),
                                width="100%",
                            ),
                            rx.grid(
                                filter_input("Search", "Category or description", AuthState.set_filter_query),
                                filter_input("Category", "e.g. Food", AuthState.set_filter_category),
                                filter_input("Start date", "YYYY-MM-DD", AuthState.set_filter_start_date, "date"),
                                filter_input("End date", "YYYY-MM-DD", AuthState.set_filter_end_date, "date"),
                                columns="4",
                                spacing="3",
                                width="100%",
                            ),
                            rx.button(
                                "Clear filters",
                                on_click=AuthState.clear_filters,
                                padding="0.4rem 0.9rem",
                                border_radius="999px",
                                background="rgba(148, 163, 184, 0.2)",
                                color="#e2e8f0",
                                border="1px solid rgba(148, 163, 184, 0.35)",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="1.5rem",
                        border_radius="20px",
                        background="rgba(15, 18, 28, 0.75)",
                        border="1px solid rgba(148, 163, 184, 0.2)",
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.heading("Expense list", size="5", weight="bold", color="white"),
                                rx.spacer(),
                                rx.text("Sorted by date", size="2", color="#94a3b8"),
                                width="100%",
                            ),
                            rx.cond(
                                AuthState.has_filtered_expenses,
                                rx.vstack(
                                    rx.foreach(AuthState.expenses_filtered, expense_row),
                                    spacing="0",
                                    width="100%",
                                ),
                                rx.text("No expenses match those filters.", color="#94a3b8", size="2"),
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="1.5rem",
                        border_radius="20px",
                        background="rgba(15, 18, 28, 0.75)",
                        border="1px solid rgba(148, 163, 184, 0.2)",
                        width="100%",
                    ),
                    spacing="5",
                    width="100%",
                    max_width="1320px",
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
