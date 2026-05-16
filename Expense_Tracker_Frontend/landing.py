import reflex as rx
import asyncio

# --- Design System Constants ---
ACCENT_BLUE = "#3B82F6"
ACCENT_EMERALD = "#10B981"
ACCENT_VIOLET = "#8B5CF6"
BG_DARK = "#030712"
GLASS_BG = "rgba(255, 255, 255, 0.03)"
GLASS_BORDER = "1px solid rgba(255, 255, 255, 0.08)"
BLUR_EFFECT = "blur(12px)"
# Fallback shim for Reflex versions without rx.motion.
_MOTION_PROPS = {
    "initial",
    "animate",
    "transition",
    "while_hover",
    "while_in_view",
    "exit",
    "variants",
}


def _fallback_motion(*children, **props):
    for key in _MOTION_PROPS:
        props.pop(key, None)
    return rx.box(*children, **props)


if not hasattr(rx, "motion"):
    rx.motion = _fallback_motion


def _fallback_span(*children, **props):
    try:
        return rx.text(*children, as_="span", **props)
    except TypeError:
        return rx.text(*children, **props)


if not hasattr(rx, "span"):
    rx.span = _fallback_span


try:
    _breakpoints = rx.breakpoints
except AttributeError:
    from reflex_base.breakpoints import breakpoints as _breakpoints

# --- Reusable Components ---

def glass_card(*children, **props):
    return rx.box(
        *children,
        background=GLASS_BG,
        backdrop_filter=BLUR_EFFECT,
        border=GLASS_BORDER,
        border_radius="24px",
        padding="1.5rem",
        **props
    )

def floating_person(image_src, top=None, left=None, right=None, bottom=None, delay=0):
    duration = 6 + (delay or 0)
    return rx.motion(
        rx.box(
            rx.image(
                src=image_src,
                width="100%",
                height="100%",
                object_fit="cover",
                border_radius="full",
            ),
            width="100px",
            height="100px",
            border=f"2px solid {ACCENT_BLUE}",
            border_radius="full",
            padding="4px",
            background=BG_DARK,
            box_shadow=f"0 0 30px {ACCENT_BLUE}33",
            _hover={"transform": "scale(1.1)", "transition": "transform 0.3s"},
        ),
        animation=f"float {duration}s ease-in-out infinite",
        animation_delay=f"{delay}s",
        position="absolute",
        top=top,
        left=left,
        right=right,
        bottom=bottom,
        z_index="5",
    )

def nav_link(text, href):
    return rx.link(
        rx.text(
            text,
            color="white",
            opacity="0.7",
            _hover={"opacity": "1", "transition": "opacity 0.2s"},
            font_size="0.9rem",
            font_weight="500",
        ),
        href=href,
    )

def navbar():
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.box(
                    width="32px",
                    height="32px",
                    background=f"linear-gradient(135deg, {ACCENT_BLUE}, {ACCENT_VIOLET})",
                    border_radius="8px",
                ),
                rx.heading("ExpenseTracker", size="6", weight="bold", color="white"),
                spacing="3",
                align_items="center",
            ),
            rx.spacer(),
            rx.hstack(
                nav_link("Features", "#features"),
                nav_link("Testimonials", "#testimonials"),
                nav_link("Pricing", "#"),
                spacing="8",
                display=_breakpoints(initial="none", sm="none", md="flex", lg="flex"),
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Log In",
                        variant="ghost",
                        color="white",
                        opacity="0.8",
                        _hover={"opacity": "1"},
                    ),
                    href="/login",
                ),
                rx.link(
                    rx.button(
                        "Get Started",
                        background=f"linear-gradient(135deg, {ACCENT_BLUE}, {ACCENT_VIOLET})",
                        color="white",
                        border_radius="12px",
                        padding="0.6rem 1.5rem",
                        _hover={"transform": "translateY(-2px)", "box_shadow": f"0 10px 20px {ACCENT_BLUE}33"},
                    ),
                    href="/signup",
                ),
                spacing="4",
            ),
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding="1rem 2rem",
        ),
        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="100",
        background="rgba(3, 7, 18, 0.5)",
        backdrop_filter="blur(10px)",
        border_bottom=GLASS_BORDER,
    )

def hero_section():
    return rx.box(
        # Glowing backgrounds
        rx.box(
            position="absolute",
            top="10%",
            left="20%",
            width="400px",
            height="400px",
            background=f"radial-gradient(circle, {ACCENT_BLUE}11, transparent 70%)",
            filter="blur(60px)",
            z_index="0",
        ),
        rx.box(
            position="absolute",
            bottom="10%",
            right="20%",
            width="500px",
            height="500px",
            background=f"radial-gradient(circle, {ACCENT_VIOLET}11, transparent 70%)",
            filter="blur(80px)",
            z_index="0",
        ),
        
        rx.center(
            rx.vstack(
                rx.text(
                    "✨ The Future of Personal Finance",
                    color=ACCENT_BLUE,
                    font_weight="600",
                    letter_spacing="2px",
                    font_size="0.8rem",
                    text_transform="uppercase",
                    padding="0.5rem 1.2rem",
                    background=f"{ACCENT_BLUE}11",
                    border_radius="100px",
                    border=f"1px solid {ACCENT_BLUE}33",
                    margin_bottom="2rem",
                ),
                rx.heading(
                    rx.span("Your Finances, ", color="white"),
                    rx.span("Finally Simplified.", color=ACCENT_BLUE),
                    size="9",
                    weight="bold",
                    line_height="1.1",
                    text_align="center",
                    max_width="800px",
                    margin_bottom="1.5rem",
                ),
                rx.text(
                    "Take control of your money with cinematic insights and effortless tracking. Built for the modern professional.",
                    color="white",
                    opacity="0.6",
                    font_size="1.2rem",
                    text_align="center",
                    max_width="600px",
                    margin_bottom="3rem",
                ),
                rx.motion(
                    rx.hstack(
                        rx.link(
                            rx.button(
                                "Start Free Today",
                                size="4",
                                background=f"linear-gradient(135deg, {ACCENT_BLUE}, {ACCENT_VIOLET})",
                                color="white",
                                border_radius="16px",
                                padding="1.8rem 2.5rem",
                                font_weight="600",
                                _hover={"transform": "scale(1.05)", "box_shadow": f"0 20px 40px {ACCENT_BLUE}44"},
                            ),
                            href="/signup",
                        ),
                        rx.button(
                            "Watch Demo",
                            size="4",
                            variant="ghost",
                            color="white",
                            border=GLASS_BORDER,
                            border_radius="16px",
                            padding="1.8rem 2.5rem",
                            _hover={"background": "rgba(255,255,255,0.05)"},
                        ),
                        spacing="6",
                    ),
                    initial={"opacity": 0, "y": 20},
                    animate={"opacity": 1, "y": 0},
                    transition={"duration": 0.8, "delay": 0.6},
                ),
                
                # Floating Elements
                rx.box(
                    floating_person("/woman.png", top="-300px", left="-150px", delay=0),
                    floating_person("/man.png", top="-100px", right="-150px", delay=1.5),
                    floating_person("/student.png", top="-400px", right="-50px", delay=0.8),
                    
                    # Decorative Cards
                    rx.motion(
                        glass_card(
                            rx.vstack(
                                rx.text("Monthly Savings", color="white", opacity="0.6", font_size="0.8rem"),
                                rx.heading("$4,250.00", color=ACCENT_EMERALD, size="5"),
                                rx.image(src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width="40px", opacity="0.5"),
                                spacing="2",
                            ),
                            width="200px",
                        ),
                        initial={"x": -100, "opacity": 0, "rotate": -10},
                        while_in_view={"x": 0, "opacity": 1, "rotate": -5},
                        transition={"duration": 1.2, "delay": 1},
                        position="absolute",
                        top="-150px",
                        left="-250px",
                    ),
                    rx.motion(
                        glass_card(
                            rx.vstack(
                                rx.text("Top Expense", color="white", opacity="0.6", font_size="0.8rem"),
                                rx.heading("Coffee ☕", color="white", size="4"),
                                rx.text("-$12.50", color="#EF4444", font_weight="bold"),
                                spacing="1",
                            ),
                            width="160px",
                        ),
                        initial={"x": 100, "opacity": 0, "rotate": 10},
                        while_in_view={"x": 0, "opacity": 1, "rotate": 5},
                        transition={"duration": 1.2, "delay": 1.2},
                        position="absolute",
                        top="-350px",
                        right="-220px",
                    ),
                    
                    position="relative",
                    width="100%",
                    max_width="1000px",
                    height="0px", # Change to 0 so it doesn't push content, but children are absolute
                    margin_top="2rem",
                ),
                
                width="100%",
                padding_top="25vh",
                padding_bottom="15vh",
            )
        ),
        padding="0 10rem",
        min_height="110vh",
        position="relative",
        overflow="hidden",
    )

def trust_section():
    return rx.box(
        rx.divider(border_color="rgba(255,255,255,0.05)"),
        rx.center(
            rx.vstack(
                rx.text("TRUSTED BY OVER 50,000+ USERS WORLDWIDE", color="white", opacity="0.4", font_size="0.7rem", letter_spacing="3px", margin_bottom="3rem"),
                rx.flex(
                    rx.vstack(rx.heading(f"{LandingState.transactions_count}M+", color="white", size="8"), rx.text("Transactions", color="white", opacity="0.5"), spacing="1", align_items="center"),
                    rx.vstack(rx.heading(f"{LandingState.accuracy_percent}%", color="white", size="8"), rx.text("Accuracy", color="white", opacity="0.5"), spacing="1", align_items="center"),
                    rx.vstack(rx.heading(f"{LandingState.rating_score}/5", color="white", size="8"), rx.text("App Rating", color="white", opacity="0.5"), spacing="1", align_items="center"),
                    rx.vstack(rx.heading(f"{LandingState.insights_hours}/7", color="white", size="8"), rx.text("Smart Insights", color="white", opacity="0.5"), spacing="1", align_items="center"),
                    width="100%",
                    justify_content="space-between",
                    flex_wrap="wrap",
                    gap="4rem",
                ),
                padding="6rem 2rem",
                max_width="1200px",
                on_mount=LandingState.start_counters,
            )
        ),
    )

def feature_card(title, description, icon, color):
    return rx.motion(
        glass_card(
            rx.vstack(
                rx.box(
                    rx.icon(tag=icon, color=color, size=30),
                    background=f"{color}11",
                    padding="1rem",
                    border_radius="16px",
                    margin_bottom="1rem",
                ),
                rx.heading(title, size="5", color="white", margin_bottom="0.5rem"),
                rx.text(description, color="white", opacity="0.6", line_height="1.6"),
                align_items="start",
            ),
            height="100%",
        ),
        while_hover={"y": -10, "box_shadow": f"0 20px 40px {color}22"},
        transition={"duration": 0.3},
    )

def features_section():
    return rx.box(
        rx.vstack(
            rx.heading(rx.span("Everything you need to ", color="white"), rx.span("thrive", color=ACCENT_BLUE), rx.span(".", color="white"), size="9", margin_bottom="4rem"),
            rx.grid(
                feature_card(
                    "Smart Categorization",
                    "Our AI automatically sorts your spending into meaningful categories so you don't have to.",
                    "layers",
                    ACCENT_BLUE
                ),
                feature_card(
                    "Real-time Alerts",
                    "Get notified instantly when you're approaching your budget limits. No surprises.",
                    "bell",
                    ACCENT_VIOLET
                ),
                feature_card(
                    "Visual Analytics",
                    "Beautifully crafted charts that reveal your financial habits in cinematic detail.",
                    "bar_chart",
                    ACCENT_EMERALD
                ),
                columns=_breakpoints(initial="1", md="1", lg="3"),
                spacing="6",
                width="100%",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="10rem 2rem",
        ),
        id="features",
    )

def mockup_section():
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading("Designed for the Modern Web", size="8", color="white", margin_bottom="1rem"),
                rx.text("A premium experience across all your devices.", color="white", opacity="0.6", margin_bottom="4rem"),
                rx.motion(
                    rx.box(
                        rx.image(
                            src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop",
                            width="100%",
                            border_radius="20px",
                            box_shadow="0 50px 100px rgba(0,0,0,0.5)",
                        ),
                        padding="10px",
                        background=GLASS_BG,
                        border=GLASS_BORDER,
                        border_radius="30px",
                        max_width="1000px",
                    ),
                    initial={"scale": 0.8, "opacity": 0},
                    while_in_view={"scale": 1, "opacity": 1},
                    transition={"duration": 1},
                ),
                padding="10rem 2rem",
            )
        ),
        background=f"radial-gradient(circle at 50% 50%, {ACCENT_BLUE}08, transparent 70%)",
    )

def testimonial_card(name, role, text, image):
    return rx.motion(
        glass_card(
            rx.vstack(
                rx.text(f'"{text}"', color="white", italic=True, opacity="0.8", margin_bottom="1.5rem"),
                rx.hstack(
                    rx.image(src=image, width="40px", height="40px", border_radius="full"),
                    rx.vstack(
                        rx.text(name, color="white", font_weight="bold", font_size="0.9rem"),
                        rx.text(role, color="white", opacity="0.5", font_size="0.7rem"),
                        spacing="0",
                        align_items="start",
                    ),
                    spacing="3",
                    align_items="center",
                ),
                align_items="start",
            ),
            width="350px",
        ),
        while_hover={"scale": 1.02},
    )

def testimonial_section():
    return rx.box(
        rx.vstack(
            rx.heading(rx.span("Loved by ", color="white"), rx.span("thousands", color=ACCENT_VIOLET), rx.span(".", color="white"), size="9", margin_bottom="4rem"),
            rx.flex(
                testimonial_card("Alea Grace Escala", "Freelance Designer", "ExpenseTracker completely changed how I track my project expenses. It's beautiful and intuitive.", "/woman.png"),
                testimonial_card("Jimuel Radomes", "Software Engineer", "The analytics are top-notch. I finally understand where my money is going every month.", "/man.png"),
                testimonial_card("Emma Tilos", "Student", "Simple, fast, and free for students. The best budget app I've ever used.", "/student.png"),
                gap="2rem",
                flex_wrap="wrap",
                justify_content="center",
            ),
            padding="10rem 2rem",
            max_width="1200px",
            margin="0 auto",
        ),
        id="testimonials",
    )

def cta_section():
    return rx.box(
        rx.center(
            rx.motion(
                rx.vstack(
                    rx.heading("Ready to master your finances?", size="9", color="white", text_align="center", margin_bottom="1.5rem"),
                    rx.text("Join 50,000+ users and start your journey to financial clarity today.", color="white", opacity="0.7", text_align="center", margin_bottom="3rem"),
                    rx.link(
                        rx.button(
                            "Get Started for Free",
                            size="4",
                            background="white",
                            color=BG_DARK,
                            border_radius="16px",
                            padding="1.8rem 3rem",
                            font_weight="bold",
                            _hover={"transform": "scale(1.05)", "box_shadow": "0 20px 40px rgba(255,255,255,0.2)"},
                        ),
                        href="/signup",
                    ),
                    background=f"linear-gradient(135deg, {ACCENT_BLUE}, {ACCENT_VIOLET})",
                    padding="6rem 4rem",
                    border_radius="40px",
                    width="100%",
                    max_width="1100px",
                    position="relative",
                    overflow="hidden",
                ),
                initial={"y": 50, "opacity": 0},
                while_in_view={"y": 0, "opacity": 1},
                transition={"duration": 0.8},
            ),
        ),
        padding="10rem 2rem",
    )

def footer():
    return rx.box(
        rx.divider(border_color="rgba(255,255,255,0.05)"),
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.box(width="24px", height="24px", background=ACCENT_BLUE, border_radius="6px"),
                    rx.heading("ExpenseTracker", size="4", color="white"),
                    spacing="2",
                ),
                rx.text("Empowering your financial future.", color="white", opacity="0.4", font_size="0.8rem"),
                align_items="start",
            ),
            rx.spacer(),
            rx.hstack(
                rx.text("© 2026 ExpenseTracker Inc.", color="white", opacity="0.4", font_size="0.8rem"),
                spacing="4",
            ),
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding="4rem 2rem",
        ),
    )

class LandingState(rx.State):
    mouse_x: int = 0
    mouse_y: int = 0
    
    # Stats Counters
    transactions_count: int = 0
    accuracy_percent: float = 0.0
    rating_score: float = 0.0
    insights_hours: int = 0
    
    is_counting: bool = False

    def handle_mouse_move(self, x: int | None = None, y: int | None = None, event: dict | None = None):
        if event is None and isinstance(x, dict) and y is None:
            event = x
            x = None
        if event:
            x = event.get("clientX") or event.get("x")
            y = event.get("clientY") or event.get("y")
        if x is None or y is None:
            return
        self.mouse_x = int(x)
        self.mouse_y = int(y)

    @rx.event(background=True)
    async def start_counters(self):
        if self.is_counting:
            return
        async with self:
            self.is_counting = True
        
        for i in range(21):
            async with self:
                self.transactions_count = i // 2
                self.accuracy_percent = round(min(99.9, i * 5), 1)
                self.rating_score = round(min(4.9, i * 0.25), 1)
                self.insights_hours = int(min(24, i * 1.2))
            await asyncio.sleep(0.05)

def landing_page():
    return rx.box(
        rx.el.style(
            """
            @keyframes float {
                0% { transform: translate3d(0, 0, 0) rotate(0deg); }
                50% { transform: translate3d(10px, -18px, 0) rotate(1.5deg); }
                100% { transform: translate3d(0, 0, 0) rotate(0deg); }
            }
            body {
                scrollbar-width: thin;
                scrollbar-color: #3B82F6 #030712;
            }
            """
        ),
        # Noise Texture Overlay
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            opacity="0.02",
            pointer_events="none",
            z_index="99",
            background_image="url('https://grainy-gradients.vercel.app/noise.svg')",
        ),
        
        # Interactive Glow
        rx.box(
            position="fixed",
            width="600px",
            height="600px",
            background=f"radial-gradient(circle, {ACCENT_BLUE}15, transparent 70%)",
            filter="blur(80px)",
            pointer_events="none",
            z_index="1",
            left=f"{LandingState.mouse_x - 300}px",
            top=f"{LandingState.mouse_y - 300}px",
            transition="left 0.1s ease-out, top 0.1s ease-out",
        ),

        navbar(),
        rx.box(
            hero_section(),
            trust_section(),
            features_section(),
            mockup_section(),
            testimonial_section(),
            cta_section(),
            footer(),
            z_index="2",
            position="relative",
        ),
        background=BG_DARK,
        min_height="100vh",
        font_family='"Inter", sans-serif',
        on_mouse_move=LandingState.handle_mouse_move,
    )
