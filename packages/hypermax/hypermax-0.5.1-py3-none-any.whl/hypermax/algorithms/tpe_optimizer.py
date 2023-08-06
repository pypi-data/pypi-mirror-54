from .optimization_algorithm_base import OptimizationAlgorithmBase
import hyperopt
import functools
import random
import numpy
import numpy.random
from hypermax.hyperparameter import Hyperparameter

class TPEOptimizer(OptimizationAlgorithmBase):

    def recommendNextParameters(self, hyperparameterSpace, results, currentTrials, lockedValues=None):
        if lockedValues is None:
            lockedValues = {}

        rstate = numpy.random.RandomState(seed=int(random.randint(1, 2 ** 32 - 1)))

        trials = self.convertResultsToTrials(hyperparameterSpace, results)

        space = Hyperparameter(hyperparameterSpace).createHyperoptSpace(lockedValues)

        params = {}
        def sample(parameters):
            nonlocal params
            params = parameters
            return {"loss": 0.5, 'status': 'ok'}

        hyperopt.fmin(fn=sample,
                      space=space,
                      algo=functools.partial(hyperopt.tpe.suggest, n_EI_candidates=24, gamma=0.25),
                      max_evals=1,
                      trials=trials,
                      rstate=rstate,
                      show_progressbar=False)
        return params

