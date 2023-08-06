from .stage import Stage
from .solution import OcpSolution
from .direct_method import OptiWrapper
from casadi import hcat

class Ocp(Stage):
    def __init__(self, **kwargs):
        """Create an Optimal Control Problem environment

        Parameters
        ----------
        t0 : float or :obj:`~ocpx.freetime.FreeTime`, optional
            Starting time of the optimal control horizon
            Default: 0
        T : float or :obj:`~ocpx.freetime.FreeTime`, optional
            Total horizon of the optimal control horizon
            Default: 1

        Examples
        --------

        >>> ocp = Ocp()
        """
        Stage.__init__(self, **kwargs)
        self.master = self
        # Flag to make solve() faster when solving a second time
        # (e.g. with different parameter values)
        self._is_transcribed = False
        self.opti = OptiWrapper()

    def spy_jacobian(self):
        self._method.spy_jacobian(self.opti)

    def spy_hessian(self):
        self._method.spy_hessian(self.opti)

    def spy(self):
        import matplotlib.pylab as plt
        plt.subplots(1, 2, figsize=(10, 4))
        plt.subplot(1, 2, 1)
        self.spy_jacobian()
        plt.subplot(1, 2, 2)
        self.spy_hessian()

    def solve(self):
        if not self.is_transcribed:
            self.opti.subject_to()
            self.opti.clear_objective()
            placeholders = self._transcribe()
            self._set_transcribed(True)
            return OcpSolution(self.opti.solve(placeholders=placeholders), self)
        else:
            return OcpSolution(self.opti.solve(), self)

    def callback(self, fun):
        self.opti.callback(lambda iter : fun(iter, OcpSolution(self.opti.non_converged_solution, self.master)))

    @property
    def debug(self):
        self.opti.debug

    def solver(self, solver, solver_options={}):
        self.opti.solver(solver, solver_options)

    def show_infeasibilities(self, *args, **kwargs):
        self.opti.debug.show_infeasibilities(*args, **kwargs)

    @property
    def f(self):
        return self.opti.objective

    @property
    def non_converged_solution(self):
        return OcpSolution(self.opti.non_converged_solution, self.master)

    def sample(self,expr):
        """hack"""
        sub_expr = []
        for k in list(range(self._method.N))+[-1]:
            sub_expr.append(self._method.eval_at_control(self, expr, k))
        return hcat(sub_expr)
