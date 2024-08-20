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
    def construct(self):
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
        self.add(dummy_plane)

        self.play(
            dummy_plane.animate.shift(2.5*LEFT)
        )

        ###
        # Write Optimisation Problem
        ###
        text = MathTex(r"""
                       \max~&3x_1+2x_2 \\
                       \mathop{\text{s.t.~}}&2x_1+x_2\leq 100 \\
                       &x_1+x_2\leq 80 \\
                       &x_1\leq 40 \\
                       &x_1\geq 0 \\
                       &x_2\geq 0
                       """).next_to(dummy_plane, RIGHT)
        text.save_state()  # save colors etc
        self.play(Write(text))

        ###
        # Highlight nonnegativity constraints
        ###
        # Can do this with a framebox or color
        self.play(FadeToColor(text[0][37:], color=YELLOW))
        #self.wait()

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
        plane = VGroup(ax, labs).next_to(text, LEFT)
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
        self.play(Restore(text))
        #self.wait()

        ###
        # Highlight 3rd constraint
        ###
        self.play(FadeToColor(text[0][32:37], color=YELLOW))

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
        self.play(Restore(text))
        #self.wait()

        ###
        # Highlight 2nd constraint
        ###
        self.play(FadeToColor(text[0][24:32], color=YELLOW))

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
        self.play(Restore(text))
        #self.wait()

        ###
        # Highlight 2nd constraint
        ###
        self.play(FadeToColor(text[0][14:24], color=YELLOW))

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
        self.play(Restore(text))
        #self.wait()

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