from casadi import Opti, jacobian, dot, hessian
from .casadi_helpers import get_meta, merge_meta, single_stacktrace, MX

class DirectMethod:
    """
    Base class for 'direct' solution methods for Optimal Control Problems:
      'first discretize, then optimize'
    """
    
    def configure(self, opti):
        opti.solver(self.solver, self.solver_options)

    def spy_jacobian(self, opti):
        import matplotlib.pylab as plt
        J = jacobian(opti.g, opti.x).sparsity()
        plt.spy(J)
        plt.title("Constraint Jacobian: " + J.dim(True))

    def spy_hessian(self, opti):
        import matplotlib.pylab as plt
        lag = opti.f + dot(opti.lam_g, opti.g)
        H = hessian(lag, opti.x)[0].sparsity()
        plt.spy(H)
        plt.title("Lagrange Hessian: " + H.dim(True))
    
    def register(self, stage):
        pass

    def transcribe(self, stage, opti):
        for c, m, _ in stage._constraints:
            opti.subject_to(c, meta = m)
        opti.add_objective(stage._objective)
        return {}

from casadi import substitute

class OptiWrapper(Opti):
    def set_ocp(self, ocp):
        self.ocp = ocp
        self.constraints = []
        self.objective = 0
        self.placeholders = None

    def subject_to(self, expr=None, meta=None):
        meta = merge_meta(meta, get_meta())
        if expr is None:
            self.constraints = []
        else:
            if isinstance(expr,MX) and expr.is_constant():
                if np.all(np.array(evalf(expr)).squeeze()==1):
                    return
                else:
                    raise Exception("You have a constraint that is never statisfied.")
            self.constraints.append((expr, meta))

    def add_objective(self, expr):
        self.objective = self.objective + expr

    def clear_objective(self):
        self.objective = 0

    def callback(self,fun):
        super().callback(fun)

    @property
    def non_converged_solution(self):
        return OptiSolWrapper(self, super().debug)

    def variable(self,n=1,m=1):
        if n==0 or m==0:
            return MX(n, m)
        else:
            return super().variable(n, m)

    def solve(self, placeholders=None):
        if placeholders is not None:
            ks = list(placeholders.keys())
            vs = [placeholders[k] for k in ks]
            orig = [c[0] for c in self.constraints] + [self.objective]
            res = substitute(orig, ks, vs)
            for c, meta, orig in zip(res[:-1], [c[1] for c in self.constraints], orig[:-1]):
                try:
                    super().subject_to(c)
                except Exception as e:
                    print(meta)
                    raise e
                self.update_user_dict(c, single_stacktrace(meta))
            super().minimize(res[-1])
            self.placeholders = placeholders
        return OptiSolWrapper(self, super().solve())

class OptiSolWrapper:
    def __init__(self, opti_wrapper, sol):
        self.opti_wrapper = opti_wrapper
        self.sol = sol

    def value(self, expr,*args,**kwargs):
        placeholders = self.opti_wrapper.placeholders
        ks = list(placeholders.keys())
        vs = [placeholders[k] for k in ks]
        res = substitute([expr], ks, vs)[0]
        return self.sol.value(res, *args,**kwargs)