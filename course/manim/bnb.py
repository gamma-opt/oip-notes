import numpy as np
from manim import *

TEXT_FONT_SIZE = 32
LABEL_FONT_SIZE = 24

config.max_files_cached = 200

def circleWithTex(str):
    c = Circle(radius=0.5)
    t = MathTex(str, font_size=32).move_to(c)
    return VGroup(c,t)


class BNB(Scene):

    def create_text(self, str):
        """
        Creates the text at the bottom left corner
        """
        text = Tex(str, font_size=TEXT_FONT_SIZE).to_corner(DL)
        self.play(Write(text))
        return text

    def replace_text(self, text_mobj, str, *, wait=1.5):
        """
        Transforms text_mobj to one with str, with some hardcoded settings
        """
        tmp = Tex(str, font_size=TEXT_FONT_SIZE).to_corner(DL)
        self.play(Transform(text_mobj, tmp))
        self.remove(tmp)
        self.wait(wait)

    def construct(self):
        ###
        # Title
        ###
        title = Text("Branch and Bound")
        self.add(title)
        self.wait()
        self.play(
            title.animate.scale(0.7).to_corner(UL).shift(0.2*UP)  # Try to get a bit more space
        )

        ###
        # Introduce problem
        ###
        text = self.create_text("Consider the following problem.")
        lp = MathTex(r"\max~& 11x_1+14x_2 \\",
                     r"\mathop{\text{s.t.~}}& x_1+x_2\leq 17 \\",
                     r"& 3x_1+7x_2\leq 63 \\",
                     r"& 3x_1+5x_2\leq 48 \\",
                     r"& 3x_1+x_2\leq 30 \\",
                     r"& x_1, x_2\geq 0 \\")
        
        integrality = MathTex(r"& x_1,x_2\in \mathbb{Z}").next_to(lp, DOWN)
        opt = VGroup(lp, integrality)
        self.play(Write(opt))

        ###
        # Highlight MILP nature
        ###
        self.replace_text(text, "This is like any linear problem we have seen before, with one key difference.")
        self.replace_text(text, "There is a constraint that forces variables to be integers.")
        self.play(Circumscribe(integrality))

        ###
        # Solve relaxation
        ###
        self.replace_text(text, "If we could ignore it ...")
        self.play(FadeOut(integrality),
                  lp.animate.to_edge(RIGHT)
                  )
        self.replace_text(text, "... we could solve the problem using the simplex method.")

        ## Constraint: x_1,x_2 \geq 0
        lp.save_state()
        self.play(FadeToColor(lp[5], color=YELLOW))

        ax = Axes(
            x_range=[0, 13, 2],
            y_range=[0, 13, 2],
            x_length=8,
            tips=False,
            axis_config={"include_numbers": True}
        )
        labs = ax.get_axis_labels(
            x_label="x_1",
            y_label="x_2"
        )

        height = (title.get_bottom() - text.get_top())[1]
        plane = VGroup(ax, labs).scale_to_fit_height(height).scale(0.95).to_edge(LEFT).shift(0.2*UP)
        self.play(Write(plane))

        y_limit = ax.plot(lambda _: 12)
        area = ax.get_area(
            y_limit,
            x_range=[0, 12],
            opacity=0.5
        )
        self.play(DrawBorderThenFill(area))
        self.play(Restore(lp))
        ##

        ## Constraint: 3x_1+x_2 \leq 30
        self.play(FadeToColor(lp[4], color=YELLOW))
        c4 = Line(
            start=ax.c2p([[10, 0]]),
            end=ax.c2p([[17/3, 13]]),
            color=BLUE
            )
        self.play(Create(c4))
        temp = ax.get_area(
            ax.plot(lambda x: 12 if x < 6 else 30-3*x),
            x_range=[0,10],
            opacity=0.5
        )
        self.play(Transform(area, temp))
        self.play(Restore(lp))
        ##

        ## Constraint: 3x_1+5x_2 \leq 48
        self.play(FadeToColor(lp[3], color=YELLOW))
        c3 = Line(
            start=ax.c2p([[13, 9/5]]),
            end=ax.c2p([[0, 9.6]]),
            color=BLUE
            )
        self.play(Create(c3))
        temp = ax.get_area(
            ax.plot(lambda x: np.min([(48-3*x)/5, 30-3*x])),
            x_range=[0,10],
            opacity=0.5
        )
        self.play(Transform(area, temp))
        self.play(Restore(lp))
        ##

        ## Constraint: 3x_1+7x_2 \leq 63
        self.play(FadeToColor(lp[2], color=YELLOW))
        c2 = Line(
            start=ax.c2p([[13, 24/7]]),
            end=ax.c2p([[0, 9]]),
            color=BLUE
            )
        self.play(Create(c2))
        temp = ax.get_area(
            ax.plot(lambda x: np.min([(63-3*x)/7, (48-3*x)/5, 30-3*x])),
            x_range=[0,10],
            opacity=0.5
        )
        self.play(Transform(area, temp))
        self.play(Restore(lp))
        ##

        ## Constraint: x_1+x_2 \leq 17
        self.play(FadeToColor(lp[1], color=YELLOW))
        c1 = Line(
            start=ax.c2p([[13, 4]]),
            end=ax.c2p([[4, 13]]),
            color=BLUE
            )
        self.play(Create(c1))
        self.replace_text(text, "This last constraint is redundant so we will just ignore it.")
        self.play(Restore(lp), FadeOut(c1))
        ##

        ## Possible solutions
        self.replace_text(text, "There are 5 possible optima.")
        vertex_coords = [
            [0,   0],
            [10,  0],
            [8.5, 4.5],
            [3.5, 7.5],
            [0,  9]
        ]
        dots = [Dot(c, color=RED) for c in ax.c2p(vertex_coords)]
        for dot in dots:
            self.play(Create(dot), Flash(dot))
        ##

        ## Highlight solution
        self.replace_text(text, "In fact, this one turns out to be the optimal solution.")
        label = MathTex("(8.5,4.5)").next_to(dots[2], UP+RIGHT)
        self.play(
            FadeOut(VGroup(*[d for i,d in enumerate(dots) if i!=2])),
            FadeIn(label),
            Flash(dots[2])
            )
        ##

        ###
        # Back to MILP world
        ###
        integrality.next_to(lp, DOWN)
        self.replace_text(text, "However, this solution is infeasible for our original problem.")
        self.play(Write(integrality), Circumscribe(integrality))
        self.replace_text(text, "Here, both $x_1$ and $x_2$ are not integers.")
        self.replace_text(text, "How do we deal with this?")

        ###
        # Branch on x_1, x_1 \geq 9
        ###
        self.replace_text(text, "One idea is the following:", wait=2)
        self.replace_text(text, "First, we pick a variable that violates the integrality constraint, say $x_1$.", wait=3)
        self.replace_text(text, "Since we don't want $x_1=8.5$, we can add additional constraints to exclude it.", wait=3)
        self.replace_text(text, r"There are two options: $x_1\leq 8$ or $x_1\geq 9$.")
        self.replace_text(text, r"Let's start with $x_1\geq 9$.")
        self.replace_text(text,  "We add it to our problem and use the simplex again.")

        branch = MathTex(r"x_1\geq 9").next_to(integrality, DOWN).align_to(integrality, LEFT).set_color_by_tex("9", ORANGE)
        c_branch = Line(
            start=ax.c2p([[9, 0]]),
            end=ax.c2p([[9, 13]]),
            color=ORANGE
            )
        area.save_state()
        temp = ax.get_area(
            ax.plot(lambda x: 30-3*x),
            x_range=[9,10],
            opacity=0.5
        )
        self.play(FadeOut(dots[2], label))
        self.play(Write(branch))
        self.play(Write(c_branch))
        self.play(Transform(area, temp))

        self.replace_text(text, "The new optimum is $(9,3)$, with objective value 141.")
        dot_branch = Dot(ax.c2p([[9,3]]), color=RED)
        label_branch = MathTex("(9,3)").next_to(dot_branch, LEFT)
        branch_optim = VGroup(dot_branch, label_branch)
        self.play(FadeIn(branch_optim))

        self.replace_text(text, "This new solution satisfies the integrality constraint!")
        self.replace_text(text, "Does this mean we are done and this is the best we can get?", wait=3)
        self.replace_text(text, "Not quite. Let's take a step back.")

        ###
        # Clear everything but the opt problem
        ###
        self.play(FadeOut(
            plane, branch_optim, c2, c3, c4, c_branch, branch, text, area
        ))

        ###
        # Draw tree root
        ###
        text = self.create_text("Suppose we name the optimisation problem $P_0$, ignoring the integrality constraint.")
        p0 = circleWithTex("P_0")
        p0_p = MathTex("x=(8.5,4.5)", font_size=LABEL_FONT_SIZE).next_to(p0, UP)
        p0_o = MathTex("obj=156.5", font_size=LABEL_FONT_SIZE).next_to(p0, DOWN)
        node0 = VGroup(p0_p, p0, p0_o).arrange(DOWN).next_to(title, DOWN).to_edge(LEFT)
        self.play(FadeIn(p0))
        self.wait(3)
        self.replace_text(text, "We know that the optimum of this problem is $(8.5,4,5)$.")
        self.play(FadeIn(p0_p))
        self.replace_text(text, "And we can calculate its objective value as 156.5.")
        self.play(FadeIn(p0_o))

        ###
        # Branch on x_1, x_1 \geq 9
        ###
        self.replace_text(text, "Next, we branched on $x_1$, added a new constraint, and obtained a new problem $P_1$.")
        p1 = circleWithTex("P_1")
        p1_p = MathTex("x=(9,3)", font_size=LABEL_FONT_SIZE).next_to(p1, LEFT)
        p1_o = MathTex("obj=141", font_size=LABEL_FONT_SIZE).next_to(p1, RIGHT)
        node1 = VGroup(p1_p, p1, p1_o).arrange(DOWN).next_to(node0, 4*DOWN)
        a_01 = Arrow(start=p0_o.get_center(), end=p1_p)
        l_01 = MathTex(r"x_1\geq 9", font_size=LABEL_FONT_SIZE).next_to(a_01, RIGHT)
        self.play(Write(VGroup(a_01, l_01)), FadeIn(p1))
        
        self.replace_text(text, "This problem has its optimum at $(9,3)$, which is feasible for our original problem.")
        self.play(FadeIn(p1_p))
        self.wait()
        self.replace_text(text, "And the objective value is 141.")
        self.play(FadeIn(p1_o))
        self.wait()

        self.replace_text(text, "Notice that the objective value for $P_1$ is lower than that of $P_0$.", wait=3)
        self.replace_text(text, "This is not surprising, since $P_1$ is a more restricted version of $P_0$.", wait=3)

        ###
        # Branch on x_1, x_1 \leq 8
        ###
        self.replace_text(text, r"There is nothing in the original problem that requires $x_1\geq 9$.", wait=3)
        self.replace_text(text, r"So now, we need to explore the case of $x_1\leq 8$ as well.")
        p2 = circleWithTex("P_2")
        p2_p = MathTex("x=(8,4.8)", font_size=LABEL_FONT_SIZE).next_to(p2, UP)
        p2_o = MathTex("obj=155.2", font_size=LABEL_FONT_SIZE).next_to(p2, DOWN)
        node2 = VGroup(p2_p, p2, p2_o).arrange(DOWN).next_to(node0, 4*RIGHT)
        a_02 = Arrow(start=p0, end=p2)
        l_02 = MathTex(r"x_1\leq 8", font_size=LABEL_FONT_SIZE).next_to(a_02, UP)
        self.play(Write(VGroup(a_02, l_02)), FadeIn(p2))

        self.replace_text(text, "The solution for this problem turns out to be $(8,4.8)$.")
        self.play(FadeIn(p2_p), FadeIn(p2_o))
        self.replace_text(text, "This is not a feasible solution for the original problem either, $x_2$ is not an integer.", wait=3)
        self.replace_text(text, "So we branch again.")

        ###
        # Branch on x_2, x_2 \leq 4
        ###
        self.replace_text(text, r"First, we do $x_2\leq 4$.")
        p3 = circleWithTex("P_3")
        p3_p = MathTex("x=(8,4)", font_size=LABEL_FONT_SIZE).next_to(p3, LEFT)
        p3_o = MathTex("obj=144", font_size=LABEL_FONT_SIZE).next_to(p3, RIGHT)
        node3 = VGroup(p3_p, p3, p3_o).arrange(DOWN).next_to(node2, 4*DOWN)
        a_23 = Arrow(start=p2_o.get_center(), end=p3_p)
        l_23 = MathTex(r"x_2\leq 4", font_size=LABEL_FONT_SIZE).next_to(a_23, RIGHT)
        self.play(Write(VGroup(a_23, l_23)), FadeIn(p3))

        self.play(FadeIn(p3_p), FadeIn(p3_o))
        self.replace_text(text, "This solution is also feasible, but there is another side to investigate.")
        
        ###
        # Branch on x_2, x_2 \geq 5
        ###
        self.replace_text(text, r"Now, we do $x_2\geq 5$.")
        p4 = circleWithTex("P_4")
        p4_p = MathTex("x=(7.67,5)", font_size=LABEL_FONT_SIZE).next_to(p4, UP)
        p4_o = MathTex("obj=154.3", font_size=LABEL_FONT_SIZE).next_to(p4, DOWN)
        node4 = VGroup(p4_p, p4, p4_o).arrange(DOWN).next_to(node2, 4*RIGHT)
        a_24 = Arrow(start=p2, end=p4)
        l_24 = MathTex(r"x_2\geq 5", font_size=LABEL_FONT_SIZE).next_to(a_24, UP)
        self.play(Write(VGroup(a_24, l_24)), FadeIn(p4))
        
        self.play(FadeIn(p4_p), FadeIn(p4_o))
        self.replace_text(text, "Another non-integer solution means another opportunity to branch.", wait=3)

        ###
        # Branch on x_1, x_1 \geq 8 is infeasible
        ###
        self.replace_text(text, r"We could try branching here with $x_1\geq 8$.")
        self.replace_text(text, r"But notice the constraints we added to get here: $x_1\leq 8$ and $x_2\geq 5$.")
        self.play(FadeToColor(VGroup(l_02, l_24), color=YELLOW))
        self.wait()
        self.replace_text(text, r"Adding $x_1\geq 8$ implies that $x_1=8$.")
        self.replace_text(text, "However, $x_1=8$ means that by the third constraint ...")
        opt.save_state()
        self.play(FadeToColor(lp[3], color=YELLOW))
        self.replace_text(text, r"we have $24+5x_2\leq 48$, which means $x_2\leq 4.8$.", wait=3)
        self.replace_text(text, r"This contradicts $x_2\geq 5$.", wait=3)
        self.replace_text(text, "Therefore, this new problem is infeasible, so we will skip it.", wait=3)
        self.play(Restore(opt), FadeToColor(VGroup(l_02, l_24), color=WHITE))

        ###
        # Branch on x_1, x_1 \leq 7
        ###
        self.replace_text(text, r"We continue to $x_1\leq 7$.")
        p5 = circleWithTex("P_5")
        p5_p = MathTex("x=(7,5.4)", font_size=LABEL_FONT_SIZE).next_to(p5, UP)
        p5_o = MathTex("obj=152.6", font_size=LABEL_FONT_SIZE).next_to(p5, DOWN)
        node5 = VGroup(p5_p, p5, p5_o).arrange(DOWN).next_to(node4, 4*RIGHT)
        a_45 = Arrow(start=p4, end=p5)
        l_45 = MathTex(r"x_1\leq 7", font_size=LABEL_FONT_SIZE).next_to(a_45, UP)
        self.play(Write(VGroup(a_45, l_45)), FadeIn(p5))
        
        self.play(FadeIn(p5_p), FadeIn(p5_o))
        self.replace_text(text, "Non-integer solution, we branch again.")

        ###
        # Branch on x_2, x_2 \leq 5
        ###
        p6 = circleWithTex("P_6")
        p6_p = MathTex("x=(7,5)", font_size=LABEL_FONT_SIZE).next_to(p6, UP)
        p6_o = MathTex("obj=147", font_size=LABEL_FONT_SIZE).next_to(p6, DOWN)
        node6 = VGroup(p6_p, p6, p6_o).arrange(DOWN).next_to(node4, 4*DOWN)
        a_56 = Line(start=p5.get_corner(DOWN+LEFT), end=p6.get_corner(UP+RIGHT)).add_tip(tip_length=0.15, tip_width=0.15)
        l_56 = MathTex(r"x_2\leq 5", font_size=LABEL_FONT_SIZE).next_to(a_56, LEFT, buff=0)
        self.play(Write(VGroup(a_56, l_56)), FadeIn(p6))
        
        self.play(FadeIn(p6_p), FadeIn(p6_o))

        ###
        # Branch on x_2, x_2 \geq 6
        ###
        p7 = circleWithTex("P_7")
        p7_p = MathTex("x=(6,6)", font_size=LABEL_FONT_SIZE).next_to(p7, UP)
        p7_o = MathTex("obj=150", font_size=LABEL_FONT_SIZE).next_to(p7, DOWN)
        node7 = VGroup(p7_p, p7, p7_o).arrange(DOWN).next_to(node5, 4*DOWN)
        a_57 = Arrow(start=p5_o.get_center(), end=p7_p)
        l_57 = MathTex(r"x_2\geq 5", font_size=LABEL_FONT_SIZE).next_to(a_57, 0.8*RIGHT)
        self.play(Write(VGroup(a_57, l_57)), FadeIn(p7))
        
        self.play(FadeIn(p7_p), FadeIn(p7_o))

        ###
        # Pick the optimum
        ###
        self.replace_text(text, "We have reached a point where we cannot branch anymore.")
        self.replace_text(text, "All the leaf nodes are solutions to our original problem.", wait=3)
        self.replace_text(text, "By comparing the objective values, we can observe that $x=(6,6)$ is the optimal solution to our MILP.")
        self.play(Circumscribe(node7))

        ###
        # Alternative branching
        ###
        self.replace_text(text, "What happens if we branched differently?")
        self.replace_text(text, "We started by branching on $x_1$ for $P_0$, but $x_2$ is an equally valid option.")
        self.replace_text(text, "Let's see what happens if we chose that.")

        self.play(FadeOut(Group(
            node1, node2, node3, node4, node5, node6, node7,
            a_01, a_02, a_23, a_24, a_45, a_56, a_57,
            l_01, l_02, l_23, l_24, l_45, l_56, l_57
            )))
        
        reuse = Group(node4, node5, node6, node7, a_45, l_45, a_56, l_56, a_57, l_57)
        Group(reuse, a_24, l_24).shift(p0.get_right()-a_24.get_left()+[0.25,0,0])

        self.replace_text(text, "If we were to start with $x_2\geq 5$, ...")
        self.play(FadeIn(Group(a_24,l_24)))
        self.replace_text(text, "... we would immediately find ourselves in the section containing the optimum.")
        self.play(FadeIn(reuse))

        self.replace_text(text, "We also need to explore the direction of $x_2\leq 4$.")
        p8 = circleWithTex("P_8")
        p8_p = MathTex("x=(8.5,4)", font_size=LABEL_FONT_SIZE).next_to(p8, UP)
        p8_o = MathTex("obj=149.5", font_size=LABEL_FONT_SIZE).next_to(p8, DOWN)
        node8 = VGroup(p8_p, p8, p8_o).arrange(DOWN).next_to(node0, 4*DOWN)
        a_08 = Arrow(start=p0_o.get_center(), end=p8_p)
        l_08 = MathTex(r"x_2\leq 4", font_size=LABEL_FONT_SIZE).next_to(a_08, RIGHT)
        self.play(Write(VGroup(a_08, l_08)), FadeIn(node8))

        self.replace_text(text, "Since the objective value is smaller than that of $P_7$, we are done.")
        self.replace_text(text, "Overall, our search tree is smaller than before.")

        ###
        # Ending note
        ###
        self.replace_text(text, "This highlights the difficulty of MILPs.")
        self.replace_text(text, "In larger problems with many variables, it is often unclear which variable to branch on and in which direction.")
        self.replace_text(text, "Consequently, the search trees often end up being very large, thus problems can take long times to be solved.")


        self.wait(5)