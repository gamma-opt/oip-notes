import numpy as np
from manim import *

"""
Script:
1. Have a 2d plane
2. write opt problem on side
3. Display current feasible region (everywhere)
4. highlight nonnegativity constraints and zoom in to first quadrant
5. one by one, highlight remaining constraints and constrict feasible region
6. Talk about why we care about vertices?
7. Mark all vertices
8. Simplex?
...
Profit
"""

class SimplexGiapetto(MovingCameraScene):

    def create_text(self, str):
        """
        Creates the text at the bottom left corner
        """
        text = Text(str, font_size=28).to_corner(DL)
        self.play(Write(text))
        return text

    def replace_text(self, text_mobj, str, wait=1):
        """
        Transforms text_mobj to one with str, with some hardcoded settings
        """
        tmp = Text(str, font_size=28).to_corner(DL)
        self.play(Transform(text_mobj, tmp))
        self.wait(wait)

    def construct(self):
        ###
        # Title
        ###
        title = Text("Simplex Algorithm")
        self.add(title)
        self.wait()
        self.play(
            title.animate.scale(0.7).to_corner(UL).shift(0.2*UP)  # Try to get a bit more space
        )

        ###
        # Narration text
        ###
        text = self.create_text("To visualise the algorithm, we will consider a problem of 2 variables.")

        ###
        # Construct dummy plane
        ###
        dummy_ax = Axes(
            x_length=8,
            y_length=5,
            tips=False
        )
        dummy_labs = dummy_ax.get_axis_labels(
            x_label="x_1",
            y_label="x_2"
        )
        dummy_plane = VGroup(dummy_ax, dummy_labs)
        self.play(FadeIn(dummy_plane))

        self.play(
            dummy_plane.animate.next_to(title, DOWN).shift(1.8*RIGHT)
        )

        ###
        # Write Optimisation Problem
        ###
        text_opt = MathTex(r"""
                       \max~&3x_1+2x_2 \\
                       \mathop{\text{s.t.~}}&2x_1+x_2\leq 100 \\
                       &x_1+x_2\leq 80 \\
                       &x_1\leq 40 \\
                       &x_1, x_2\geq 0
                       """).next_to(dummy_plane, RIGHT)
        text_opt.save_state()  # save colors etc
        self.play(Write(text_opt))

        ###
        ###
        self.replace_text(text, "What is the feasible region for this problem?")
        self.replace_text(text, "We can start by considering the nonnegativity constraints.")

        ###
        # Highlight nonnegativity constraints
        ###
        # Can do this with a framebox or color
        self.play(FadeToColor(text[31:-1], color=YELLOW))
        self.play(FadeToColor(text_opt[0][37:], color=YELLOW))
        self.wait()

        ###
        ###
        self.replace_text(text, "The solutions are constrainted to the first quadrant.")

        ###
        # Transition to first quadrant
        ###
        # Can do this with a Transform or zoom in
        ax = Axes(
            x_range=[0, 90, 20],
            y_range=[0, 110, 20],
            x_length=6,
            tips=False,
            axis_config={"include_numbers": True}
        )
        labs = ax.get_axis_labels(
            x_label="x_1",
            y_label="x_2"
        )

        height = (title.get_bottom() - text.get_top())[1]
        plane = VGroup(ax, labs).scale_to_fit_height(height).scale(0.95).to_edge(LEFT).shift(0.2*UP)
        self.play(
            ReplacementTransform(
                dummy_plane,
                plane
            )
        )
        #self.wait()

        ###
        # Highlight first quadrant
        ###
        y_limit = ax.plot(lambda _: 110)
        area = ax.get_area(
            y_limit,
            x_range=[0, 90],
            opacity=0.5
        )
        self.play(DrawBorderThenFill(area))
        #self.wait()

        ###
        # Remove constraint highlight
        ###
        self.play(
            Restore(text_opt),
            FadeOut(text)
            )
        #self.wait()

        ###
        ###
        text = self.create_text("We can then apply the remaining constraints.")

        ###
        # Highlight 3rd constraint
        ###
        self.play(FadeToColor(text_opt[0][32:37], color=YELLOW))

        ###
        # Add constraint to area highlight
        ###
        c3 = Line(
            start=ax.c2p([[40, 0]]),
            end=ax.c2p([[40, 110]]),
            color=BLUE
            )
        self.play(Create(c3))
        new_width = np.abs(np.subtract(*ax.c2p([[0,0],[40,0]])[:,0]))  # calculate the actual distance between points 0 and 40 on the x-axis
        self.play(area.animate.stretch_to_fit_width(new_width).align_to(c3, RIGHT))
        #self.wait()
        
        ###
        # Remove constraint highlight
        ###
        self.play(Restore(text_opt))
        #self.wait()

        ###
        # Highlight 2nd constraint
        ###
        self.play(FadeToColor(text_opt[0][24:32], color=YELLOW))

        ###
        # Add constraint to area highlight
        ###
        c2 = Line(
            start=ax.c2p([[80, 0]]),
            end=ax.c2p([[0, 80]]),
            color=BLUE
            )
        self.play(Create(c2))
        temp = ax.get_area(
            ax.plot(lambda x: 80-x),
            x_range=[0,40],
            opacity=0.5
        )
        # not sure how to make this smoother
        self.play(Transform(area, temp))
        #self.wait()

        ###
        # Remove constraint highlight
        ###
        self.play(Restore(text_opt))
        #self.wait()

        ###
        # Highlight 2nd constraint
        ###
        self.play(FadeToColor(text_opt[0][14:24], color=YELLOW))

        ###
        # Add constraint to area highlight
        ###
        c1 = Line(
            start=ax.c2p([[50, 0]]),
            end=ax.c2p([[0, 100]]),
            color=BLUE
            )
        self.play(Create(c1))
        temp = ax.get_area(
            ax.plot(lambda x: np.min([80-x, 100-2*x])),
            x_range=[0,40],
            opacity=0.5
        )
        # not sure how to make this smoother
        self.play(Transform(area, temp))
        

        ###
        # Remove constraint highlight
        ###
        self.play(Restore(text_opt))
        #self.wait()

        ###
        ###
        self.play(FadeOut(text))
        self.wait()
        text = self.create_text("There are 5 vertices that are possibly the optimum.")


        ###
        # Label vertices
        ###
        vertex_coords = [
            [0,   0],
            [40,  0],
            [40, 20],
            [20, 60],
            [0,  80]
        ]
        dots = [Dot(c, color=RED) for c in ax.c2p(vertex_coords)]
        self.play(Create(VGroup(*dots)))
        self.wait()

        ###
        ###
        self.replace_text(text, "With only 5 points, one could try bruteforcing.")
        self.replace_text(text, "But that is not feasible in larger problems.")
        self.replace_text(text, "We need a smarter solution.")
        self.replace_text(text, "The simplex algorithm offers a smart way of iterating through the vertices.")

        ###
        # Save before Simplex explanation
        ###
        graph = VGroup(plane, c1, c2, c3, area, *dots)
        graph.save_state()
        text_opt.save_state()
        self.play(FadeOut(graph), FadeOut(text))
        self.wait()

        ###
        # Rewrite: slack vars
        ###
        text = self.create_text("To show the algorithm, we need to rewrite the problem in the standard form.")
        self.play(text_opt.animate.center())
        self.wait(1)
        self.replace_text(text, "First, inequalities are changed to equality constraint using slack variables.")

        text_opt2 = MathTex(r"""
                       \max~&3x_1+2x_2 \\
                       \mathop{\text{s.t.~}}&2x_1+x_2+x_3= 100 \\
                       &x_1+x_2 + x_4 = 80 \\
                       &x_1 + x_5 = 40 \\
                       &x_1,\dots,x_5\geq 0
                       """)
        arrow = Arrow(start=LEFT, end=RIGHT)
        tmp = VGroup(text_opt.copy(), arrow, text_opt2).arrange()
        self.play(
            text_opt.animate.move_to(tmp[0]),
            FadeIn(arrow, text_opt2),
        )
        tmp = VGroup(text_opt, arrow, text_opt2, text).save_state()
        self.play(
            FadeToColor(Group(
                *list(map(text_opt[0].__getitem__, [20, 29, 34])),
                text[53:-1],
                text_opt2[0][20:24],
                text_opt2[0][32:36],
                text_opt2[0][40:44],
                text_opt2[0][49:55]
                ), color=RED)
        )
        self.wait(2)
        tmp.restore()
        self.play(
            text_opt2.animate.move_to(text_opt),
            FadeOut(text_opt, arrow)
        )

        ###
        # Rewrite: nonnegativity
        ###
        self.replace_text(text, "We also need to make all variables nonnegative.")
        self.replace_text(text, "That is not an issue in this problem.")

        ###
        # Rewrite: free variables
        ###
        self.replace_text(text, "We will also rewrite the constraints so that the slack variables are left alone.")
        text_opt3 = MathTex(r"""
                       \max~&3x_1+2x_2 \\
                       \mathop{\text{s.t.~}}&x_3= 100-2x_1-x_2 \\
                       &x_4 = 80-x_1-x_2 \\
                       &x_5 = 40-x_1 \\
                       &x_1,\dots,x_5\geq 0
                       """)
        tmp = VGroup(text_opt2, arrow, text_opt3).arrange()
        self.play(
            FadeIn(arrow, text_opt3)
            )


        self.wait(5)