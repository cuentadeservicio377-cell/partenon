"""
Partenon Hackathon Explainer — Manim Community Edition script.
One class per scene, each independently renderable.
No MathTex / LaTeX. Text only. Partenon palette. Monospace font.
"""

from manim import *

# ═══════════════════════════════════════════════════════════════════════════════
# SHARED CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

BG = "#050505"
SURFACE = "#08080C"
TEXT = "#F7F5F0"
MUTED = "#6B6B78"
DIM = "#45454F"
CYAN = "#00D4FF"
AMBER = "#FFB800"
PARCHMENT = "#EDE8DF"

MONO = "Menlo"

# Hero colors
SCRIBE_COLOR = "#4A90A4"
HERALD_COLOR = "#9B59B6"
COLLECTOR_COLOR = "#635BFF"
GUARDIAN_COLOR = "#76B900"
STRATEGIST_COLOR = AMBER
DIPLOMAT_COLOR = "#E74C3C"
BRAIN_COLOR = "#D4A853"

HEROES = [
    ("Scribe", "finance", SCRIBE_COLOR),
    ("Herald", "communications", HERALD_COLOR),
    ("Collector", "payments", COLLECTOR_COLOR),
    ("Guardian", "security", GUARDIAN_COLOR),
    ("Strategist", "operations", STRATEGIST_COLOR),
    ("Diplomat", "relations", DIPLOMAT_COLOR),
    ("Brain", "memory", BRAIN_COLOR),
]


def make_text(text, font_size=24, color=TEXT, weight=NORMAL, opacity=1.0):
    """Helper for consistent Text mobjects."""
    t = Text(text, font_size=font_size, font=MONO, weight=weight, color=color)
    if opacity != 1.0:
        t.set_opacity(opacity)
    return t


def make_dot(color, radius=0.12):
    return Dot(color=color, radius=radius)


def rounded_rect(width, height, color, stroke_width=1, fill_color=None, fill_opacity=0.0, corner_radius=0.2):
    r = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        stroke_width=stroke_width,
        stroke_color=color,
        fill_color=fill_color or BG,
        fill_opacity=fill_opacity,
    )
    return r


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 1: THE ORACLE PROBLEM
# ═══════════════════════════════════════════════════════════════════════════════

class Scene1_TheOracleProblem(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = make_text("Most AI tools are oracles.", font_size=40, color=CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.6)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # Chat bubble on the left
        bubble = rounded_rect(4.2, 2.2, MUTED, fill_color=SURFACE, fill_opacity=0.6, corner_radius=0.25)
        bubble.to_edge(LEFT, buff=1.0)
        bubble.shift(UP * 0.2)

        q = make_text("Q: What should I do?", font_size=22, color=MUTED)
        a = make_text('A: "Organize your receipts."', font_size=22, color=TEXT)
        q.move_to(bubble.get_center() + UP * 0.4)
        a.move_to(bubble.get_center() + DOWN * 0.3)

        self.play(Create(bubble), run_time=1.0)
        self.play(Write(q), run_time=1.0)
        self.play(Write(a), run_time=1.0)
        self.wait(0.5)

        # Founder figure on the right
        founder = make_text("FOUNDER", font_size=20, color=TEXT, weight=BOLD)
        founder.to_edge(RIGHT, buff=2.2)
        founder.shift(DOWN * 0.3)
        founder_dot = make_dot(CYAN, radius=0.16)
        founder_dot.next_to(founder, UP, buff=0.25)

        self.play(FadeIn(founder_dot), Write(founder), run_time=1.0)

        # Orbiting documents
        doc_labels = ["RECEIPTS", "INVOICES", "FOLLOWUPS", "CALENDAR"]
        docs = VGroup()
        angles = [30, 110, 190, 270]
        radius = 1.6
        for label, angle_deg in zip(doc_labels, angles):
            angle = np.deg2rad(angle_deg)
            rect = rounded_rect(1.6, 0.55, DIM, fill_color=SURFACE, fill_opacity=0.5, corner_radius=0.1)
            pos = founder_dot.get_center() + np.array([np.cos(angle) * radius, np.sin(angle) * radius, 0])
            rect.move_to(pos)
            txt = make_text(label, font_size=14, color=MUTED)
            txt.move_to(rect.get_center())
            docs.add(VGroup(rect, txt))

        self.play(LaggedStart(*[FadeIn(d) for d in docs], lag_ratio=0.2), run_time=2.0)
        self.wait(0.5)

        # Arrow from chat bubble toward founder, then dim
        arrow_start = bubble.get_right() + RIGHT * 0.2
        arrow_end = founder_dot.get_left() + LEFT * 0.4
        arrow = Arrow(arrow_start, arrow_end, color=CYAN, stroke_width=2, buff=0.1)
        arrow.set_opacity(0.8)

        self.play(GrowArrow(arrow), run_time=1.0)
        self.wait(0.5)
        self.play(arrow.animate.set_opacity(0.15), run_time=1.0)
        self.wait(1.5)
        self.wait(7.0)  # hold for voiceover pacing

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 2: HERMES NEEDS A HOME
# ═══════════════════════════════════════════════════════════════════════════════

class Scene2_HermesNeedsAHome(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Hermes ring
        ring = Circle(radius=1.2, stroke_color=CYAN, stroke_width=3, fill_opacity=0)
        ring.move_to(ORIGIN)

        hermes_label = make_text("HERMES", font_size=32, color=CYAN, weight=BOLD)
        hermes_label.move_to(ring.get_center())

        self.play(Create(ring), run_time=1.5)
        self.play(FadeIn(hermes_label), run_time=1.0)
        self.wait(0.5)

        # Pulse
        pulse = Circle(radius=1.2, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
        pulse.move_to(ring.get_center())
        self.add(pulse)
        self.play(pulse.animate.scale(1.4).set_opacity(0), run_time=1.5, rate_func=smooth)
        self.remove(pulse)

        subtitle = make_text("agent, not assistant", font_size=24, color=MUTED)
        subtitle.next_to(ring, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(0.5)

        # Column outline rises behind
        column = RoundedRectangle(
            width=4.0,
            height=5.5,
            corner_radius=0.1,
            stroke_color=DIM,
            stroke_width=1,
            fill_opacity=0,
        )
        column.move_to(ORIGIN)
        column.set_opacity(0.3)
        self.play(FadeIn(column), run_time=1.5)
        self.wait(0.5)

        # Transform into Partenon title
        partenon_title = make_text("THE PARTENON", font_size=48, color=TEXT, weight=BOLD)
        partenon_title.move_to(ORIGIN)

        self.play(
            Transform(ring, Circle(radius=0.01, stroke_opacity=0, fill_opacity=0).move_to(ORIGIN)),
            FadeOut(hermes_label),
            FadeOut(subtitle),
            Write(partenon_title),
            run_time=1.5,
        )
        self.wait(0.5)

        tagline = make_text("a working headquarters for Hermes, inside a small business.", font_size=22, color=MUTED)
        tagline.next_to(partenon_title, DOWN, buff=0.5)
        self.play(Write(tagline), run_time=1.5)
        self.wait(1.5)
        self.wait(7.0)  # hold for voiceover pacing

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 3: THE SEVEN HEROES
# ═══════════════════════════════════════════════════════════════════════════════

class Scene3_TheSevenHeroes(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = make_text("Seven profiles. One shared context.", font_size=36, color=CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        # Hermes center
        center = ORIGIN + DOWN * 0.2
        hermes_dot = make_dot(CYAN, radius=0.18)
        hermes_dot.move_to(center)
        hermes_label = make_text("HERMES", font_size=20, color=CYAN, weight=BOLD)
        hermes_label.next_to(hermes_dot, DOWN, buff=0.15)

        self.play(FadeIn(hermes_dot), Write(hermes_label), run_time=1.0)

        # Orbit ring
        orbit = Circle(radius=2.4, stroke_color=DIM, stroke_width=1, fill_opacity=0)
        orbit.move_to(center)
        self.play(Create(orbit), run_time=1.5)
        self.wait(0.3)

        # Place heroes around the orbit
        hero_mobjects = []
        hero_groups = []
        start_angle = 90  # top
        for i, (name, territory, color) in enumerate(HEROES):
            angle_deg = start_angle - i * (360 / 7)
            angle = np.deg2rad(angle_deg)
            pos = center + np.array([np.cos(angle) * 2.4, np.sin(angle) * 2.4, 0])

            dot = make_dot(color, radius=0.14)
            dot.move_to(pos)
            name_txt = make_text(name, font_size=18, color=color, weight=BOLD)
            terr_txt = make_text(territory, font_size=14, color=MUTED)
            name_txt.next_to(dot, direction=pos - center, buff=0.2)
            terr_txt.next_to(name_txt, DOWN, buff=0.08)

            group = VGroup(dot, name_txt, terr_txt)
            hero_groups.append(group)
            hero_mobjects.extend([dot, name_txt, terr_txt])

            self.play(FadeIn(group), run_time=0.7)

        self.wait(0.5)

        # Lines from Hermes to each hero
        lines = VGroup()
        for group in hero_groups:
            dot = group[0]
            line = DashedLine(center, dot.get_center(), color=DIM, stroke_width=1, dashed_ratio=0.5)
            lines.add(line)

        self.play(LaggedStart(*[Create(line) for line in lines], lag_ratio=0.1), run_time=2.0)
        self.wait(0.5)

        # Highlight Brain and connect to all others
        brain_group = hero_groups[-1]
        brain_dot = brain_group[0]
        brain_lines = VGroup()
        for group in hero_groups[:-1]:
            line = Line(brain_dot.get_center(), group[0].get_center(), color=BRAIN_COLOR, stroke_width=1.5)
            line.set_opacity(0.5)
            brain_lines.add(line)

        self.play(
            brain_dot.animate.scale(1.6).set_color(AMBER),
            run_time=0.8,
        )
        self.play(LaggedStart(*[Create(line) for line in brain_lines], lag_ratio=0.1), run_time=2.0)

        memory_text = make_text("shared memory", font_size=18, color=BRAIN_COLOR)
        memory_text.next_to(brain_group, direction=brain_group.get_center() - center, buff=0.15)
        self.play(Write(memory_text), run_time=1.0)

        self.wait(2.0)
        self.wait(10.0)  # hold for voiceover pacing
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 4: HONEST STATUS TAGS
# ═══════════════════════════════════════════════════════════════════════════════

class Scene4_HonestStatusTags(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = make_text("Honest status tags", font_size=40, color=CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        statuses = [
            ("LIVE", "runs the moment you install", AMBER),
            ("CONNECT", "works after you add credentials", CYAN),
            ("ROADMAP", "not built yet; labeled clearly", PARCHMENT),
        ]

        cards = VGroup()
        for i, (tag, desc, color) in enumerate(statuses):
            card = rounded_rect(7.0, 1.1, DIM, fill_color=SURFACE, fill_opacity=0.5, corner_radius=0.15)
            tag_text = make_text(tag, font_size=22, color=color, weight=BOLD)
            desc_text = make_text(desc, font_size=22, color=TEXT)
            tag_text.move_to(card.get_left() + RIGHT * 1.1)
            desc_text.move_to(card.get_center() + RIGHT * 0.8)
            card_group = VGroup(card, tag_text, desc_text)
            card_group.move_to(ORIGIN + UP * (1.2 - i * 1.4))
            cards.add(card_group)

        for card_group in cards:
            self.play(card_group.animate.shift(RIGHT * 8).shift(LEFT * 8), run_time=0.01)
            self.play(card_group.animate.shift(RIGHT * 0.05), run_time=1.2)
            self.wait(0.3)

        note = make_text("No credentials required to explore.", font_size=20, color=MUTED)
        note.next_to(cards, DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=1.0)

        self.wait(2.0)
        self.wait(8.0)  # hold for voiceover pacing
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 5: ARCHITECTURE FLOW
# ═══════════════════════════════════════════════════════════════════════════════

class Scene5_ArchitectureFlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = make_text("How a mission flows", font_size=36, color=CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        nodes = [
            ("FOUNDER", TEXT),
            ("HERMES", CYAN),
            ("CORE", CYAN),
            ("HEROES", TEXT),
            ("TOOLS", MUTED),
        ]

        node_objs = []
        x_positions = np.linspace(-5.5, 5.5, len(nodes))
        y = -0.2

        for (label, color), x in zip(nodes, x_positions):
            dot = make_dot(color, radius=0.18)
            dot.move_to(np.array([x, y, 0]))
            txt = make_text(label, font_size=20, color=color, weight=BOLD)
            txt.next_to(dot, DOWN, buff=0.25)
            group = VGroup(dot, txt)
            node_objs.append(group)

        # Draw nodes one by one
        for group in node_objs:
            self.play(FadeIn(group), run_time=0.8)

        # Arrows between nodes
        arrows = VGroup()
        for i in range(len(node_objs) - 1):
            start = node_objs[i][0].get_center()
            end = node_objs[i + 1][0].get_center()
            arrow = Arrow(start, end, color=DIM, stroke_width=2, buff=0.3)
            arrows.add(arrow)

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=2.0)
        self.wait(0.5)

        # Tool integrations under TOOLS
        tools_y = -2.2
        tool_labels = ["Google Workspace", "Stripe", "G-Brain"]
        tool_objs = VGroup()
        for j, tl in enumerate(tool_labels):
            t = make_text(tl, font_size=18, color=MUTED)
            x = x_positions[-1] + (j - 1) * 1.6
            t.move_to(np.array([x, tools_y, 0]))
            tool_objs.add(t)

        self.play(FadeIn(tool_objs), run_time=1.5)
        self.wait(0.5)

        # Packet dot traveling the path
        packet = make_dot(AMBER, radius=0.1)
        packet.move_to(node_objs[0][0].get_center())
        self.add(packet)

        path_points = [node_objs[i][0].get_center() for i in range(len(node_objs))]
        path = VMobject()
        path.set_points_as_corners(path_points)

        self.play(MoveAlongPath(packet, path), run_time=2.0, rate_func=linear)
        self.wait(1.5)
        self.wait(7.0)  # hold for voiceover pacing

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 6: INSTALL AND RUN
# ═══════════════════════════════════════════════════════════════════════════════

class Scene6_InstallAndRun(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = make_text("Install and run", font_size=40, color=CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        # Code block background
        code_bg = rounded_rect(7.0, 2.4, DIM, fill_color=SURFACE, fill_opacity=0.6, corner_radius=0.15)
        code_bg.to_edge(UP, buff=1.6)
        self.play(FadeIn(code_bg), run_time=0.8)

        code_lines = [
            "git clone https://github.com/",
            "  cuentadeservicio377-cell/partenon.git",
            "cd partenon",
            "./install.sh",
        ]
        code_group = VGroup()
        for i, line in enumerate(code_lines):
            txt = make_text(line, font_size=20, color=TEXT)
            txt.move_to(code_bg.get_top() + DOWN * (0.45 + i * 0.45) + LEFT * 2.8)
            code_group.add(txt)

        self.play(LaggedStart(*[Write(line) for line in code_group], lag_ratio=0.4), run_time=3.0)

        check = make_text("184 tests pass", font_size=22, color=GUARDIAN_COLOR, weight=BOLD)
        check.next_to(code_bg, DOWN, buff=0.4)
        self.play(Write(check), run_time=1.0)
        self.wait(0.5)

        # Workshop card slides up
        workshop_card = rounded_rect(7.0, 2.2, AMBER, fill_color=SURFACE, fill_opacity=0.5, corner_radius=0.15)
        workshop_card.move_to(ORIGIN + DOWN * 1.8)

        workshop_title = make_text("90-MINUTE WORKSHOP", font_size=24, color=AMBER, weight=BOLD)
        workshop_title.move_to(workshop_card.get_top() + DOWN * 0.45)

        bullets = [
            "install locally or on a VPS",
            "meet Scribe, Strategist, Guardian",
            "leave with a live dashboard",
        ]
        bullet_objs = VGroup()
        for i, b in enumerate(bullets):
            dot = make_dot(AMBER, radius=0.06)
            txt = make_text(b, font_size=20, color=TEXT)
            txt.next_to(dot, RIGHT, buff=0.2)
            row = VGroup(dot, txt)
            row.move_to(workshop_card.get_top() + DOWN * (1.0 + i * 0.45) + LEFT * 2.5)
            bullet_objs.add(row)

        self.play(
            workshop_card.animate.shift(DOWN * 0.01),
            FadeIn(workshop_card),
            Write(workshop_title),
            run_time=1.0,
        )
        self.play(LaggedStart(*[FadeIn(b) for b in bullet_objs], lag_ratio=0.3), run_time=2.0)

        self.wait(2.0)
        self.wait(7.0)  # hold for voiceover pacing
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SCENE 7: THE MISSION
# ═══════════════════════════════════════════════════════════════════════════════

class Scene7_TheMission(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = make_text("The mission", font_size=40, color=CYAN, weight=BOLD)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        counter = make_text("10", font_size=96, color=AMBER, weight=BOLD)
        counter.move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(counter), run_time=0.8)

        # Animate counter from 10 toward 1,000,000
        target = 1_000_000
        steps = 30
        for i in range(1, steps + 1):
            value = int(10 + (target - 10) * (i / steps) ** 2)
            new_counter = make_text(f"{value:,}", font_size=96, color=AMBER, weight=BOLD)
            new_counter.move_to(counter.get_center())
            self.play(Transform(counter, new_counter), run_time=0.08)

        self.wait(0.5)

        installations_label = make_text("installations", font_size=28, color=TEXT)
        installations_label.next_to(counter, DOWN, buff=0.3)
        self.play(Write(installations_label), run_time=1.0)

        repo = make_text("github.com/cuentadeservicio377-cell/partenon", font_size=20, color=CYAN)
        repo.next_to(installations_label, DOWN, buff=0.6)
        self.play(FadeIn(repo), run_time=1.0)

        tagline = make_text("Hermes is the agent. The Partenon is the home.", font_size=26, color=TEXT)
        tagline.next_to(repo, DOWN, buff=0.6)
        self.play(Write(tagline), run_time=1.5)

        closing = make_text("Open Source Must Win.", font_size=32, color=AMBER, weight=BOLD)
        closing.next_to(tagline, DOWN, buff=0.6)
        self.play(Write(closing), run_time=1.5)

        self.wait(2.5)
        self.wait(7.0)  # hold for voiceover pacing
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
