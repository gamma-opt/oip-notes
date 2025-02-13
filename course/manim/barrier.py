import numpy as np
import matplotlib.pyplot as plt

from manim import *

TEXT_FONT_SIZE = 32
LABEL_FONT_SIZE = 24

config.max_files_cached = 200

##
# Contour
##
f = lambda x,y: (x-2)**4 + (x-2*y)**2
xs = np.arange(0, 2, 0.001)
zs = [[f(x,y) for x in xs] for y in xs]
paths = plt.contour(xs, xs, zs, [0.3, 1, 2.5, 5, 9]).get_paths()

###
# Optimization code
###

# def f(x):
#     return (x[0]-2)**4 + (x[0]-2*x[1])**2

def g(x):
    return x[0]**2 - x[1] + x[2]

x0 = np.array([0.5, 1, 0.75])
n_p = 3
n_d = 1
N = 16     # Number of iterations (empirically, this is enough for this problem and parameters)
beta = 0.5     # Reduction factor
rho = 10.0     # Around 5 for efficiency.
eps = 1e-3    # Tolerance

def update_newton_dir(x, mu, z, rho):
    X = np.diag(x)
    Z = np.diag(z)
    e = np.ones((n_p,1))

    grad = np.array([
        [4*(x[0]-2)**3 + 2*(x[0]-2*x[1])],
        [-4*(x[0]-2*x[1])],
        [0]
    ])
    jac = np.array([[2*x[0], -1, 1]])  # jacobian of constraints
    hess = np.array([                 # hessian of objective
        [12*(x[0]-2)**2 + 2, -4, 0],
        [-4, 8, 0],
        [0, 0, 0]
    ])

    Nmatrix = np.block([
        [-hess, jac.T,                np.identity(n_p)],
        [jac,   np.zeros((n_d, n_d)), np.zeros((n_d, n_p))],
        [Z,     np.zeros((n_p, n_d)),   X]
    ])

    Nrhs = -np.block([
        [(mu*jac + z).T - grad],
        [g(x)],
        [X@Z@e - rho*e]
    ])

    d = np.linalg.solve(Nmatrix, Nrhs)

    dx = d[:3]
    dv = d[3]
    du = d[4:]
    return dx, dv, du

def calculate_step_size(x, d):
    a = 1-eps
    for i in range(len(d)):
        if d[i] < 0:
            a = min(a, -x[i]/d[i])
    return np.round(a, decimals=3)

def primal_dual_ip(
        rho
    ):

    x = np.zeros((N, n_p))
    v = np.zeros((N, n_d))
    u = np.zeros((N, n_p))

    x[0,:] = x0
    u[0,:] = rho / x0

    for i in range(N-1):
        if np.dot(n_p, rho) < eps:
            break
        dx, dv, du = update_newton_dir(x[i,:], v[i,:], u[i,:], rho)

        alpha_p = calculate_step_size(x[i,:], dx)
        alpha_d = calculate_step_size(u[i,:], du)

        x[i+1,:] = x[i,:] + alpha_p*dx.T[0]
        v[i+1,:] = v[i,:] + alpha_d*dv.T[0]
        u[i+1,:] = u[i,:] + alpha_d*du.T[0]

        rho *= beta

    return x

points = primal_dual_ip(rho)

################################################################

class IPM(Scene):

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
        title = Text("Interior Point Method")
        self.add(title)
        self.wait()
        self.play(
            title.animate.scale(0.7).to_corner(UL).shift(0.2*UP)  # Try to get a bit more space
        )

        ###
        # Introduce problem
        ###
        text = self.create_text("Consider the following problem.")
        opt = MathTex(r"\min~& (x_1-2)^4 + (x_1-2x_2)^2 \\",
                     r"\mathop{\text{s.t.~}}& x_1^2-x_2 \leq 0 \\",
                     r"& x_1,x_2 \geq 0")
        
        self.play(Write(opt))

        ###
        # Contour
        ###
        self.replace_text(text, "Let's plot it.")

        self.play(opt.animate.to_edge(RIGHT))

        opt.save_state()
        self.play(FadeToColor(opt[2], color=YELLOW))
        
        ax = Axes(
            x_range=[0, 2, 0.5],
            y_range=[0, 2, 0.5],
            x_length=6,
            tips=False,
            axis_config={"include_numbers": True}
        )
        labs = ax.get_axis_labels(
            x_label="x_1",
            y_label="x_2"
        )

        height = (title.get_bottom() - text.get_top())[1]
        plane = VGroup(ax, labs).scale_to_fit_height(height).scale(0.8).to_edge(LEFT).shift(0.2*UP)
        self.play(Write(plane))

        self.play(Restore(opt))

        self.play(FadeToColor(opt[0], color=YELLOW))

        contours = []
        #colors = [YELLOW_A, YELLOW_B, YELLOW_C, YELLOW_D, YELLOW_E]
        # viridis
        colors = [ManimColor.from_hex(h) for h in ["#1e9d88", "#35b779", "#6ccd59", "#b5de2c", "#fee727"]]
        for i_p in range(len(paths)):
            vertices = paths[i_p].cleaned().vertices
            c = ax.plot_parametric_curve(
                lambda t: (
                vertices[int(t),0],
                vertices[int(t),1],
                0
            ), color=colors[i_p], t_range=(0, len(paths[i_p])-1, 1))

            contours.append(c)

        # paths[2] includes a(n approximately) vertical line at x_1=2
        # Couldn't figure out how to get rid of it, so I'm painting it over
        contours.append(ax.plot_line_graph([2,2],[0,2], line_color=BLACK, add_vertex_dots=False))

        contours = VGroup(*contours)
        self.play(FadeIn(contours))

        self.play(Restore(opt))

        ###
        # Constraint
        ###
        self.play(FadeToColor(opt[1], color=YELLOW))

        c = ax.plot(lambda x: x**2, x_range=[0, np.sqrt(2)], color=BLUE)
        self.play(Create(c))
        self.play(Restore(opt))

        self.replace_text(text, "We need to find an optimum above the curve.")

        ###
        # Problem rewriting
        ###
        plot = VGroup(ax, labs, contours, c)

        self.replace_text(text, "This is a nonlinear problem.")

        self.replace_text(text, "We will reformulate this problem as follows.")
        self.replace_text(text, "First, we convert the inequality constraint into an equality constraint.")


        target = MathTex(r"\min~& (x_1-2)^4 + (x_1-2x_2)^2 \\",
                     r"\mathop{\text{s.t.~}}& x_1^2-x_2 + x_3 = 0 \\",
                     r"& x_1,x_2,x_3 \geq 0").to_edge(RIGHT)
        
        arrow = Arrow(start=LEFT, end=RIGHT)
        tmp = VGroup(opt.copy(), arrow, target).arrange()

        self.play(
            FadeOut(plot),
            opt.animate.move_to(tmp[0]),
            FadeIn(arrow, target),
        )

        tmp = VGroup(opt, arrow, target).save_state()
        self.play(
            FadeToColor(Group(
                opt[1][11],
                target[1][10:14],
                target[2][6:8]
                ), color=RED)
        )
        self.replace_text(text, "Doing so adds a slack variable.")
        self.wait(2)
        self.play(tmp.animate.restore())


        self.play(
            target.animate.move_to(opt),
            FadeOut(opt, arrow)
        )
        self.remove(opt)
        opt = target
        
        self.replace_text(text, "Then, the non-negativity constraints go into a barrier function.")

        target = MathTex(r"\min~& (x_1-2)^4 + (x_1-2x_2)^2 \\",
                         r"& - \rho \sum_{i=1}^3\ln (x_i) \\"
                         r"\mathop{\text{s.t.~}}& x_1^2-x_2 + x_3 = 0")
        
        tmp = VGroup(opt, arrow, target).arrange().save_state()
        self.play(
            FadeIn(arrow, target)
            )

        self.play(
            FadeToColor(Group(
                opt[2],
                target[1][:13]
                ), color=RED)
        )
        self.wait(2)
        self.play(tmp.animate.restore())

        self.play(
            target.animate.move_to(opt),
            FadeOut(opt, arrow)
        )
        self.remove(opt)
        opt = target

        self.replace_text(text, "Finally, we pose the Lagrangian function.")

        target = MathTex(r"\min~& (x_1-2)^4 + (x_1-2x_2)^2 \\",
                         r"& - \rho \sum_{i=1}^3\ln (x_i) \\"
                         r"& + \mu (x_1^2-x_2 + x_3)")
        
        tmp = VGroup(opt, arrow, target).arrange().save_state()
        self.play(
            FadeIn(arrow, target)
            )

        self.play(
            FadeToColor(Group(
                opt[1][13:],
                target[1][13:]
                ), color=RED)
        )
        self.wait(2)
        self.play(tmp.animate.restore())

        self.play(
            target.animate.center(),
            FadeOut(opt, arrow)
        )
        self.remove(opt)
        opt = target

        ###
        # KKT
        ###
        self.replace_text(text, "The Lagrangian implies the Newton system.")
 
        newton = MathTex(r"\begin{bmatrix}" 
                         r"-H_f(x^k) & J_g(x^k)^\top & I \\"
                         r"J_g(x^k) & 0 & 0 \\"
                         r"Z^k & 0 & X^k "     
                         r"\end{bmatrix}"
                         r"\begin{bmatrix}"
                         r"\Delta x \\"
                         r"\Delta \mu \\"
                         r"\Delta z "
                         r"\end{bmatrix}  ="
                         r"- \begin{bmatrix}"
                         r"J_g(x^k)^\top \mu^k + z^k - \nabla f(x^k) \\"
                         r"g(x) \\"
                         r"-X^kZ^ke + \rho e"
                         r"\end{bmatrix}",
                        font_size=36
                        )
        
        self.play(
            FadeOut(opt),
            FadeIn(newton)
            )
        
        self.replace_text(text, "Here, $H_f$ is the Hessian of the objective.")
        self.replace_text(text, "$g$ is a function that encodes our equality constraints...")
        self.replace_text(text, "... and $J_g$ is its Jacobian.")

        ###
        # Substitution
        ###

        self.replace_text(text, "We can compute the required expressions from our problem.")

        self.play(
            newton.animate.scale(0.7).to_corner(UR),
            FadeIn(opt.center())
            )
        
        grad = MathTex(r"\nabla f(x^k) = \begin{bmatrix}"
                       r"4(x_1-2)^3+2(x_1-2x_2) \\"
                       r"-4(x_1-2x_2) \\"
                       r"0"
                       r"\end{bmatrix}"
                       )
        hess = MathTex(r"H(x^k)=\begin{bmatrix}" 
                         r"12(x^k_1-2)^2+2 & -4 & 0 \\"
                         r"-4 & 8 & 0 \\"
                         r"0 & 0 & 0" 
                         r"\end{bmatrix}"
                         )
        g = MathTex(r"g(x)=x_1^2-x_2+x_3")
        jac = MathTex(r"J(x^k)=\begin{bmatrix}" 
                         r"2x_1 & -1 & 1 "
                         r"\end{bmatrix}"
                         )

        tmp = VGroup(grad, hess, g, jac).scale(0.7).arrange(DOWN).to_edge(RIGHT)


        self.replace_text(text, "First are the gradient and the Hessian of the objective function.")
        self.play(
            opt.animate.to_edge(LEFT),
            FadeIn(grad, hess)
            )
        self.wait(3)

        self.replace_text(text, "Then, the equality constraints and their Jacobian.")
        self.play(FadeIn(g, jac))
        self.wait(2)

        self.replace_text(text, "In this example, we only have a single equality constraint, so it is simple.")
        self.replace_text(text, "When there are more constraints, $g$ can be a vector-valued function.")

        self.replace_text(text, "Plugging these in, our system of equation becomes almost ready.")

        newton_full = MathTex(r"\begin{bmatrix}"
                            r"12(x_1^k-2)^2 & -4 & 0 & 2x_1^k & 1 & 0 & 0 \\"
                            r"-4 & 8 & 0 & -1 & 0 & 1 & 0 \\"
                            r"0 & 0 & 0 & 1 & 0 & 0 & 1 \\"
                            r"2x_1^k & -1 & 1 & 0 & 0 & 0 & 0 \\"
                            r"z_1^k & 0 & 0 & 0 & x_1^k & 0 & 0 \\"
                            r"0 & z_2^k & 0 & 0 & 0 & x_2^k & 0 \\"
                            r"0 & 0 & z_3^k & 0 & 0 & 0 & x_3^k \\"
                            r"\end{bmatrix}"
                            r"\begin{bmatrix}"
                            r"\Delta x_1 \\"
                            r"\Delta x_2 \\"
                            r"\Delta x_3 \\"
                            r"\Delta \mu \\"
                            r"\Delta z_1 \\"
                            r"\Delta z_2 \\"
                            r"\Delta z_3 "
                            r"\end{bmatrix}"
                            r"= "
                            r"\begin{bmatrix}"
                            r"-2x^k_1 \mu^k - z_1^k + 4(x^k_1-2)^3 + 2(x^k_1-2x^k_2) \\"
                            r"\mu^k - z_2^k - 4(x_1^k-2x_2^k)\\"
                            r"-\mu^k - z_3^k\\"
                            r" -(x_1^k)^2+x_2^k-x_3^k\\"
                            r"- x_1^kz_1^k + \rho \\"
                            r"- x_2^kz_2^k + \rho \\"
                            r"- x_3^kz_3^k + \rho"
                            r"\end{bmatrix}"
                            ).scale(0.6)
        
        self.play(
            FadeOut(Group(opt, newton, grad, hess, g, jac)),
            FadeIn(newton_full)
        )

        ###
        # Initial point
        ###

        self.replace_text(text, "We will solve this Newton system iteratively to obtain better and better points.")
        self.replace_text(text, "To start doing so requires us to have an initial point $(x^0,\mu^0,z^0)$.")
        self.replace_text(text, "For $x^0=(x_1^0,x_2^0)$, we only need a feasible point.")

        self.play(
            newton_full.animate.scale(0.6).to_edge(RIGHT),
            FadeIn(plot)
        )

        self.replace_text(text, "For example, $x^0=(0.5,1)$.")

        d1 = Dot(point=ax.c2p([[0.5, 1]]), color=RED)
        l1 = MathTex("(0.5,1)").next_to(d1, 0.8*UP).scale(0.8)
        self.play(Create(d1), Flash(d1), Create(l1))

        self.replace_text(text, r"We won't worry about initializing $\mu$ and $z$ in this video.")
        self.replace_text(text, "Just suppose we have appropriate values for them.")

        self.replace_text(text, r"The final piece of the puzzle is $\rho$.")
        self.replace_text(text, r"We will start with $\rho=10$ and divide it by 2 at every iteration.")

        ###
        # Iterating
        ###
        self.replace_text(text, "We can finally plug in these values and solve the system to obtain the next point...")

        self.play(
            l1.animate.next_to(newton_full, 2*UP)
            )
        
        l2 = MathTex(f"({points[1,0]:.2f},{points[1,1]:.2f})").scale(0.8).next_to(newton_full, 2*DOWN)

        self.play(FadeIn(l2))

        d2 = Dot(ax.c2p([points[1,:2]]))
        self.play(Create(d2), Flash(d2))

        self.replace_text(text, "... and repeat until convergence.")

        self.play(FadeOut(l1, l2))
        for i in range(2, 9):
            d = Dot(ax.c2p([points[i,:2]]))
            self.play(Create(d), Flash(d))
            self.wait(0.5)

        self.wait(4)
