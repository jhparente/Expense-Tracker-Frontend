import reflex as rx
from Expense_Tracker_Frontend.state import AuthState
from Expense_Tracker_Frontend.dashboard import navbar


def form_input(
    label: str,
    placeholder: str,
    on_change,
    value,
    input_type: str = "text",
    **input_props,
) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color="#cbd5e1"),
        rx.input(
            placeholder=placeholder,
            type=input_type,
            on_change=on_change,
            value=value,
            **input_props,
            width="100%",
            height="46px",
            padding_left="1rem",
            padding_right="1rem",
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


def form_text_area(label: str, placeholder: str, on_change, value, **props) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", weight="medium", color="#cbd5e1"),
        rx.text_area(
            placeholder=placeholder,
            on_change=on_change,
            value=value,
            **props,
            width="100%",
            min_height="120px",
            padding="0.85rem 1rem",
            border_radius="12px",
            background="rgba(255, 255, 255, 0.04)",
            border="1px solid rgba(148, 163, 184, 0.25)",
            color="white",
            font_size="0.95rem",
            line_height="1.4",
        ),
        spacing="1",
        width="100%",
    )


def category_picker() -> rx.Component:
    return rx.vstack(
        rx.text("Category", size="2", weight="medium", color="#cbd5e1"),
        rx.hstack(
            rx.select(
                AuthState.category_options,
                placeholder="Choose category",
                on_change=AuthState.set_expense_category,
                width="40%",
                height="46px",
                padding_left="0.8rem",
                padding_right="0.8rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.04)",
                border="1px solid rgba(148, 163, 184, 0.25)",
                color="white",
                font_size="0.95rem",
            ),
            rx.input(
                placeholder="Or type a category",
                on_change=AuthState.set_expense_category,
                value=AuthState.expense_category,
                max_length=20,
                width="60%",
                height="46px",
                padding_left="1rem",
                padding_right="1rem",
                border_radius="12px",
                background="rgba(255, 255, 255, 0.04)",
                border="1px solid rgba(148, 163, 184, 0.25)",
                color="white",
                font_size="1rem",
                line_height="1.2",
            ),
            spacing="2",
            width="100%",
        ),
        spacing="1",
        width="100%",
    )


def add_summary_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Totals preview", size="2", color="#94a3b8"),
            rx.heading(AuthState.expense_prev_total, size="6", weight="bold", color="white"),
            rx.text("Total spent so far", size="2", color="#64748b"),
            rx.box(height="1px", width="100%", background="rgba(148, 163, 184, 0.2)"),
            rx.heading(AuthState.expense_next_total, size="6", weight="bold", color="white"),
            rx.text("After adding this expense", size="2", color="#64748b"),
            rx.text(
                "Update the amount to see how totals change.",
                size="2",
                color="#94a3b8",
            ),
            spacing="3",
            align_items="start",
        ),
        padding="1.6rem",
        border_radius="20px",
        background="rgba(15, 18, 28, 0.75)",
        border="1px solid rgba(148, 163, 184, 0.2)",
        width="100%",
    )


def edit_summary_card() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Current expense", size="2", color="#94a3b8"),
            rx.heading(AuthState.selected_expense["category"], size="6", weight="bold", color="white"),
            rx.text(AuthState.selected_expense["amount"], size="3", color="#e2e8f0"),
            rx.text("Date", size="2", color="#94a3b8"),
            rx.text(AuthState.selected_expense["date"], size="3", color="#e2e8f0"),
            rx.text("Description", size="2", color="#94a3b8"),
            rx.text(
                AuthState.selected_expense["description"],
                size="2",
                color="#e2e8f0",
            ),
            spacing="3",
            align_items="start",
        ),
        padding="1.6rem",
        border_radius="20px",
        background="rgba(15, 18, 28, 0.75)",
        border="1px solid rgba(148, 163, 184, 0.2)",
        width="100%",
    )


def expense_form_card(title: str, button_label: str, on_submit, is_edit: bool) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(title, size="5", weight="bold", color="white"),
                rx.spacer(),
                rx.link(
                    "Back to expenses",
                    href="/expenses",
                    color="#7dd3fc",
                ),
                width="100%",
            ),
            form_input(
                "Amount",
                "0.00",
                AuthState.set_expense_amount,
                AuthState.expense_amount,
                "number",
                step="0.01",
                max="9999999999",
                id="amount_input",
            ),
            category_picker(),
            form_input(
                "Date",
                "YYYY-MM-DD",
                AuthState.set_expense_date,
                AuthState.expense_date,
                "date",
            ),
            form_text_area(
                "Description",
                "Optional notes about this expense",
                AuthState.set_expense_description,
                AuthState.expense_description,
                max_length=50,
            ),
            rx.button(
                button_label,
                on_click=on_submit,
                width="100%",
                padding="0.9rem",
                border_radius="14px",
                background="linear-gradient(90deg, #22d3ee, #3b82f6)" if not is_edit else "linear-gradient(90deg, #38bdf8, #22c55e)",
                color="white",
            ),
            spacing="4",
            width="100%",
        ),
        padding="1.8rem",
        border_radius="20px",
        background="rgba(15, 18, 28, 0.75)",
        border="1px solid rgba(148, 163, 184, 0.2)",
        width="100%",
    )


def expense_form_layout(title: str, button_label: str, on_submit, is_edit: bool) -> rx.Component:
    return rx.box(
        # Custom JS to enforce 10-digit limit and block scientific notation (+, -, e)
        # This prevents 'spamming' and invalid characters instantly in the browser
        rx.script("""
            document.addEventListener('input', (e) => {
                if (e.target.id === 'amount_input') {
                    if (e.target.value.length > 10) {
                        e.target.value = e.target.value.slice(0, 10);
                    }
                }
            });
            document.addEventListener('keydown', (e) => {
                if (e.target.id === 'amount_input') {
                    if (['e', 'E', '+', '-'].includes(e.key)) {
                        e.preventDefault();
                    }
                }
            });
        """),
        rx.box(
            position="absolute",
            top="-160px",
            left="-160px",
            width="420px",
            height="420px",
            background="radial-gradient(circle, rgba(34, 211, 238, 0.25), rgba(34, 211, 238, 0))",
            filter="blur(12px)",
        ),
        rx.box(
            position="absolute",
            bottom="-180px",
            right="-160px",
            width="480px",
            height="480px",
            background="radial-gradient(circle, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0))",
            filter="blur(12px)",
        ),
        navbar("Edit" if is_edit else "Add Expense"),
        rx.container(
            rx.center(
                rx.vstack(
                    edit_summary_card() if is_edit else add_summary_card(),
                    expense_form_card(title, button_label, on_submit, is_edit),
                    spacing="4",
                    width="100%",
                    max_width="760px",
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


@rx.page(route="/expenses/new", on_load=AuthState.load_add_expense)
def expense_create_page() -> rx.Component:
    return expense_form_layout("Add expense", "Create expense", AuthState.create_expense, False)


@rx.page(route="/expenses/edit", on_load=AuthState.load_edit_expense)
def expense_edit_page() -> rx.Component:
    return expense_form_layout("Edit expense", "Update expense", AuthState.update_expense, True)