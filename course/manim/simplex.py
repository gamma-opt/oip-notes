import numpy as np
from manim import *

"""
Ideas:
- Change the title at certain points/fade it out
- label constraints with color (either the text or add small marker), and the lines accordingly as well
"""

TEXT_FONT_SIZE = 32

class SimplexGiapetto(MovingCameraScene):

    def create_text(self, str):
        """
        Creates the text at the bottom left corner
        """
        text = Tex(str, font_size=TEXT_FONT_SIZE).to_corner(DL)
        self.play(Write(text))
        return text

    def replace_text(self, text_mobj, str, *, wait=1.5, t2c=None):
        """
        Transforms text_mobj to one with str, with some hardcoded settings
        """
        if type(str) == tuple:
            tmp = Tex(*str, font_size=TEXT_FONT_SIZE).to_corner(DL)
        else:    
            tmp = Tex(str, font_size=TEXT_FONT_SIZE).to_corner(DL)
        if t2c:
            for k,v in t2c.items():
                tmp.set_color_by_tex(k, v)
        self.play(Transform(text_mobj, tmp))
        self.remove(tmp)
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
        self.wait()

        self.play(
            dummy_plane.animate.next_to(title, DOWN).shift(2*RIGHT)
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
                       """).to_edge(RIGHT)
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
        plane = VGroup(ax, labs).scale_to_fit_height(height).scale(0.95).to_edge(LEFT).shift(0.15*UP)
        self.play(
            ReplacementTransform(
                dummy_plane,
                plane
            )
        )
        self.remove(dummy_plane)

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

        ###
        # Remove constraint highlight
        ###
        self.play(
            Restore(text_opt),
            FadeOut(text)
            )
        self.remove(text)

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
        
        ###
        # Remove constraint highlight
        ###
        self.play(Restore(text_opt))

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
        self.remove(temp)

        ###
        # Remove constraint highlight
        ###
        self.play(Restore(text_opt))

        ###
        # Highlight 1st constraint
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
        self.remove(temp)
        

        ###
        # Remove constraint highlight
        ###
        self.play(Restore(text_opt))

        ###
        ###
        self.play(FadeOut(text))
        self.remove(text)
        self.wait()
        text = self.create_text("There are 5 vertices that are possibly the optimum.")
        self.wait()


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
        for dot in dots:
            self.play(Create(dot), Flash(dot))
        #self.play(Create(VGroup(*dots)), *[Flash(dot) for dot in dots])
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
        self.play(FadeOut(graph), FadeOut(text))
        self.remove(text)
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
                       \mathop{\text{s.t.~}}&2x_1+x_2+s_1= 100 \\
                       &x_1+x_2 + s_2 = 80 \\
                       &x_1 + s_3 = 40 \\
                       &x_1,\dots,s_3\geq 0
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
        self.play(tmp.animate.restore())
        self.play(
            text_opt2.animate.move_to(text_opt),
            FadeOut(text_opt, arrow)
        )
        self.remove(text_opt)

        ###
        # Rewrite: nonnegativity
        ###
        self.replace_text(text, "We also need to make all variables nonnegative.")
        self.replace_text(text, "That is not an issue in this problem.")

        ###
        # Rewrite: free variables
        ###
        self.replace_text(text, "We will also rewrite the constraints so that the slack variables are left alone.")
        text_opt3 = MathTex(
                       r"\max~&3x_1+2x_2 \\",
                       r"\mathop{\text{s.t.~}}",r"&s_1= 100-2x_1-x_2 \\",
                       r"&s_2 = 80-x_1-x_2 \\",
                       r"&s_3 = 40-x_1 \\",
                       r"&x_1,\dots,s_3\geq 0"
                       )
        text_opt3.save_state()
        tmp = VGroup(text_opt2, arrow, text_opt3).arrange().save_state()
        self.play(
            FadeIn(arrow, text_opt3)
            )

        self.play(
            FadeToColor(Group(
                text_opt2[0][21:23],
                text_opt2[0][33:35],
                text_opt2[0][41:43],
                text_opt3[2][0:2],
                text_opt3[3][0:2],
                text_opt3[4][0:2]
                ), color=RED)
        )
        self.wait()
        self.play(
            text_opt3.animate.center(),
            FadeOut(text_opt2, arrow, text)
        )
        self.remove(text_opt2, arrow, text)
        text_opt = text_opt3

        ###
        # Dictionary
        ###
        text = self.create_text('The variables on the left make up our "dictionary".')
        self.play(FadeToColor(Group(
            text[0][30:-1]
        ), color=RED))
        self.replace_text(text, ("We will rewrite the objective variables in terms of those in the ", "dictionary."), t2c={"dictionary":RED})
        self.play(FadeToColor(Group(
            text[0][16:34],
            text_opt[0][4:6],
            text_opt[0][8:10]
        ), color=YELLOW))
        self.wait()

        self.play(
            text_opt.animate.restore(),
        )
        self.replace_text(text, "In doing so, we will make all variables in the objective function have a negative sign.")
        self.replace_text(text, "Since these variables have negative signs and are nonegative, maximisation is achieved when they are zero.")
        self.play(FadeOut(text))
        self.remove(text)

        ###
        # Go back to graph
        ###
        self.play(
            FadeIn(graph),
            text_opt.animate.to_edge(RIGHT)
        )

        ###
        # Pick x_1 to rewrite with s_3
        ###
        text = self.create_text("We need to pick which variable to rewrite.")
        self.wait(2)
        self.replace_text(text, "And also which constraint to rewrite with.")
        self.replace_text(text, "Suppose we pick this pair.", wait=0.5)
        self.play(
            FadeToColor(text_opt[0][4:6], color=YELLOW),
            FadeToColor(text_opt[4][0:2], color=RED)
            )
        self.wait()
        
        # rewrite constraint
        tmp = MathTex(r"\max~&3{{x_1}}+2x_2 \\",
                      r"\mathop{\text{s.t.~}}",
                      r"&s_1= 100-2x_1-x_2 \\",
                      r"&s_2 = 80-x_1-x_2 \\",
                      r"&x_1 = 40-s_3 \\",
                      r"&x_1,\dots,s_3\geq 0"
                       ).move_to(text_opt)
        self.play(TransformMatchingShapes(text_opt, tmp))
        self.remove(text_opt)
        text_opt = tmp
        self.wait()

        # Swap constraints
        height = text_opt[4].get_y() - text_opt[5].get_y()
        self.play(
            text_opt[4].animate.shift(height*DOWN),
            text_opt[5].animate.shift(height*DOWN),
            text_opt[6].animate.shift(2*height*UP)
        )
        self.wait()

        # Substitute
        target = MathTex(r"\max~&", r"3{{(40-s_3)}}+2x_2 \\",
                         r"\mathop{\text{s.t.~}}",
                         r"&x_1 = 40-s_3 \\",
                         r"&s_1= 100-2{{x_1}}-x_2 \\",
                         r"&s_2 = 80-{{x_1}}-x_2 \\",
                         r"&x_1,\dots,s_3\geq 0").move_to(text_opt)
        moving = MathTex("{{(40-s_3)}}").move_to(text_opt[6], RIGHT)
        self.play(TransformMatchingTex(VGroup(text_opt, moving), target))
        self.remove(text_opt, moving)
        text_opt = target
        self.wait(1)

        # Expand
        tmp = MathTex(r"120+2x_2-3s_3 \\").move_to(text_opt[3], UR)
        self.play(Transform(Group(*text_opt[1:4]), tmp))
        self.remove(tmp)

        self.replace_text(text, "Since the new variable has a negative sign, we want to set it to zero.")
        self.replace_text(text, "Doing so means, by the first constraint, that $x_1$ is equal to 40.")
        self.replace_text(text, "So we have moved from this point ...")
        self.play(Flash(dots[0]))
        self.replace_text(text, "... to this point.")
        self.play(Flash(dots[1]))

        # Substitute
        ## Awkward animation here
        self.replace_text(text, "We substitute the remaining $x_1$s here...")
        target = MathTex(r"\max~&120+2x_2-3s_3 \\",
                         r"\mathop{\text{s.t.~}}",
                         r"&x_1 = 40-s_3 \\",
                         r"&s_1 =", r"100-2{{(40-s_3)}}-x_2 \\",
                         r"&s_2 =", r"80-{{(40-s_3)}}-x_2 \\",
                         r"&x_1,\dots,s_3\geq 0").to_edge(RIGHT)
        self.play(text_opt.animate.align_to(target, UL))
        moving = MathTex("{{(40-s_3)}}").move_to(text_opt[5], RIGHT)
        self.play(TransformMatchingTex(VGroup(text_opt, moving), target))
        self.remove(text_opt, moving)
        text_opt = target
        self.wait()

        # Expand
        tmp1 = MathTex(r"20-x_2+2s_3 \\").align_to(text_opt[4], UL)
        tmp2 = MathTex(r"40-x_2+s_3 \\").align_to(text_opt[8], UL)
        self.play(
            Transform(Group(*text_opt[4:7]), tmp1),
            Transform(Group(*text_opt[8:11]), tmp2)
            )
        self.remove(tmp1, tmp2)
        self.play(text_opt.animate.to_edge(RIGHT))

        ###
        # Pick x_2 to rewrite with x_1
        ###
        self.replace_text(text, "The objective still contains variables without a negative sign.")
        self.replace_text(text, "So we continue similarly.")
        self.replace_text(text, "Let's pick these two.")
        self.play(
            FadeToColor(text_opt[0][8:10], color=YELLOW),
            FadeToColor(text_opt[3][0:2], color=RED)
            )
        self.wait()
        
        # Rewrite constraint
        ## Awkward
        tmp = MathTex(r"&x_2 = 20-s_1+2s_3 \\").move_to(text_opt[3], LEFT)
        self.play(Transform(Group(*text_opt[3:7]), tmp))
        self.wait()

        # Substitute
        target = MathTex(r"\max~&", "120+2", "{{(20-s_1+2s_3)}}", r"-3s_3 \\",
                         r"\mathop{\text{s.t.~}}",
                         r"&x_1 = 40-s_3 \\",
                         r"&x_2 = 20-s_1+2s_3 \\",
                         r"&s_2 = 40-{{x_2}}+s_3 \\",
                         r"&x_1,\dots,s_3\geq 0").to_edge(RIGHT)
        self.play(text_opt.animate.align_to(target, UL))
        moving = MathTex("{{(20-s_1+2s_3)}}").move_to(text_opt[5], RIGHT)
        self.play(TransformMatchingTex(VGroup(text_opt, moving), target))
        text_opt = target
        self.wait()

        # Expand
        tmp = MathTex(r"160-2s_1+s_3 \\").move_to(text_opt[1], UL)
        self.play(Transform(Group(*text_opt[1:4]), tmp))
        self.play(text_opt.animate.to_edge(RIGHT))

        self.replace_text(text, "Doing so, we move from here ...")
        self.play(Flash(dots[1]))
        self.replace_text(text, "... to here.")
        self.play(Flash(dots[2]))

        # Substitute
        ## Awkward animation here
        self.replace_text(text, "We substitute the remaining $x_2$ ...")
        target = MathTex(r"\max~&160-2s_1+{{s_3}} \\",
                         r"\mathop{\text{s.t.~}}",
                         r"&x_1 = 40-s_3 \\",
                         r"&x_2 = 20-s_1+2s_3 \\",
                         r"&s_2 =", r"40-{{(20-s_1+2s_3)}}+s_3 \\",
                         r"&x_1,\dots,s_3\geq 0").to_edge(RIGHT)
        self.play(text_opt.animate.align_to(target, UL))
        moving = MathTex("{{(20-s_1+2s_3)}}").move_to(text_opt[6], RIGHT)
        self.play(TransformMatchingTex(VGroup(text_opt, moving), target))
        text_opt = target
        self.wait()

        # Expand
        tmp = MathTex(r"20+s_1-s_3 \\").align_to(text_opt[7], UL)
        self.play(Transform(Group(*text_opt[7:10]), tmp))
        self.play(text_opt.animate.to_edge(RIGHT))

        ###
        # Pick s_3 to rewrite with s_2
        ###
        self.replace_text(text, "Now, these two.")
        self.play(
            FadeToColor(text_opt[1][0:2], color=YELLOW),
            FadeToColor(text_opt[6][0:2], color=RED)
            )
        
        # Rewrite constraint
        ## Awkward
        tmp = MathTex(r"&s_3 = 20+s_1-s_2 \\").move_to(text_opt[6], LEFT)
        self.play(Transform(VGroup(*text_opt[6:10]), tmp))
        self.wait()

        # Substitute
        target = MathTex(r"\max~&{{160-2s_1+}}{{(20+s_1-s_2)}} \\",
                         r"\mathop{\text{s.t.~}}",
                         r"&x_1 = 40-s_3 \\",
                         r"&x_2 = 20-s_1+2{{s_3}} \\",
                         r"&s_3 = 20+s_1-s_2 \\",
                         r"&x_1,\dots,s_3\geq 0").to_edge(RIGHT)
        self.play(text_opt.animate.align_to(target, UL))
        moving = MathTex("{{(20+s_1-s_2)}}").move_to(text_opt[7], RIGHT)
        self.play(TransformMatchingTex(VGroup(text_opt, moving), target))
        text_opt = target
        self.wait()

        # Expand
        tmp = MathTex(r"180-s_1-s_2 \\").move_to(text_opt[1], UL)
        self.play(Transform(Group(*text_opt[1:4]), tmp))
        self.play(text_opt.animate.to_edge(RIGHT))

        # Substitute
        self.replace_text(text, "Substitute the remaining $s_3$ ...")
        target = MathTex(r"\max~&180-s_1-s_2 \\",
                         r"\mathop{\text{s.t.~}}",
                         r"&x_1 = 40-s_3 \\",
                         r"&x_2 = {{20-s_1+2}}{{(20+s_1-s_2)}} \\",
                         r"&s_3 = 20+s_1-s_2 \\",
                         r"&x_1,\dots,s_3\geq 0").to_edge(RIGHT)
        self.play(text_opt.animate.align_to(target, UL))
        moving = MathTex("{{(20+s_1-s_2)}}").move_to(text_opt[5], RIGHT)
        self.play(TransformMatchingTex(VGroup(text_opt, moving), target))
        text_opt = target
        self.wait()

        # Expand
        tmp = MathTex(r"60+s_1-2s_2 \\").align_to(text_opt[4], UL)
        self.play(Transform(Group(*text_opt[4:7]), tmp))
        self.play(text_opt.animate.to_edge(RIGHT))

        self.replace_text(text, "Now, the objective contains only negative signs.")
        self.replace_text(text, "So we can infer that the maximum value is 180.")
        self.replace_text(text, "Setting the objective variables to zero, we see that $x_1=40$.")
        text_opt.save_state()
        self.play(FadeToColor(text_opt[2], color=YELLOW))
        self.play(Restore(text_opt))
        self.replace_text(text, "And $x_2=60$.")
        self.play(FadeToColor(Group(text_opt[3:5]), color=YELLOW))
        self.play(Restore(text_opt))
        self.replace_text(text, "We move from here ...")
        self.play(Flash(dots[2]))
        self.replace_text(text, "... to here.")
        self.play(Flash(dots[3]))


        self.wait(5)