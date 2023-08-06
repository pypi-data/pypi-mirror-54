"""
Class to perform sampling with evolutionary and nature inspired algorithms.
"""

# Authors: Sašo Karakatič <karakatic@gmail.com>
# License: GNU General Public License v3.0

import logging
import sys
import time
from multiprocessing import Pool

import numpy as np
from NiaPy.algorithms.basic.ga import GeneticAlgorithm
from imblearn.over_sampling.base import BaseOverSampler
from scipy import stats
from sklearn.base import ClassifierMixin
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import check_random_state, safe_indexing

from EvoPreprocess.data_sampling.SamplingBenchmark import SamplingBenchmark
from EvoPreprocess.data_sampling.settings import EvoSettings as es

logging.basicConfig()
logger = logging.getLogger('examples')
logger.setLevel('INFO')


class EvoSampling(BaseOverSampler):
    """
    Sample data with evolutionary and nature-inspired methods.

    Parameters
    ----------
    random_seed : int or None, optional (default=None)
        It used as seed by the random number generator.
        If None, the current system time is used for the seed.

    evaluator : classifier or regressor, optional (default=None)
        The classification or regression object from scikit-learn framework.
        If None, the GausianNB for classification is used.

    optimizer : evolutionary or nature-inspired optimization method, optional (default=GeneticAlgorithm)
        The evolutionary or or nature-inspired optimization method from NiaPy framework.

    n_runs : int, optional (default=10)
        The number of runs on each fold. Only the best performing result of all runs is used.

    n_folds : int, optional (default=3)
        The number of folds for cross-validation split into the training and validation sets.

    benchmark : object, optional (default=SamplingBenchmark)
        The benchmark object with mapping and fitness value calculation.

    n_jobs : int, optional (default=None)
        The number of jobs to run in parallel.
        If None, then the number of jobs is set to the number of cores.
    """

    def __init__(self,
                 random_seed=None,
                 evaluator=None,
                 optimizer=GeneticAlgorithm,
                 n_runs=10,
                 n_folds=3,
                 benchmark=SamplingBenchmark,
                 n_jobs=None):
        super(EvoSampling, self).__init__()

        self.evaluator = GaussianNB() if evaluator is None else evaluator

        self.random_seed = int(time.time()) if random_seed is None else random_seed
        self.random_state = check_random_state(self.random_seed)
        self.optimizer = optimizer
        self.n_runs = n_runs
        self.n_folds = n_folds
        self.n_jobs = n_jobs
        self.benchmark = benchmark

    def _fit_resample(self, X, y):
        """Method for resampling the dataset.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Matrix containing the data which have to be sampled.

        y : array-like, shape (n_samples)
            Corresponding label for each instance in X.

        Returns
        -------
        X_resampled : {ndarray, sparse matrix}, shape (n_samples_new, n_features)
            The array containing the resampled data.

        y_resampled : ndarray, shape (n_samples_new,)
            The corresponding labels of `X_resampled`
        """

        return self._sample(X, y)

    def _sample(self, X, y):
        """Resample the dataset.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Matrix containing the data which have to be sampled.

        y : array-like, shape (n_samples)
            Corresponding label for each sample in X.

        Returns
        -------
        X_resampled : {ndarray, sparse matrix}, shape \
            (n_samples_new, n_features)
            The array containing the resampled data.

        y_resampled : ndarray, shape (n_samples_new,)
            The corresponding label of `X_resampled`
        """

        mask = []
        if self.evaluator is ClassifierMixin:
            skf = StratifiedKFold(n_splits=self.n_folds, shuffle=True, random_state=self.random_state)
        else:
            skf = KFold(n_splits=self.n_folds, shuffle=True, random_state=self.random_state)

        evos = []  # Parameters for parallel threaded evolution run

        y_len = len(y)

        for train_index, val_index in skf.split(X, y):
            mask.append(train_index)
            for j in range(self.n_runs):
                evos.append(
                    (X, y, train_index, val_index, self.random_seed + j + 1, self.optimizer, self.evaluator,
                     self.benchmark))

        with Pool(processes=self.n_jobs) as pool:
            results = pool.starmap(EvoSampling._run, evos)
        occurrences = EvoSampling._reduce(mask, results, self.n_runs, self.n_folds, self.benchmark, y_len)
        phenotype = self.benchmark.map_to_phenotype(occurrences)
        return (safe_indexing(X, phenotype),
                safe_indexing(y, phenotype))

    @staticmethod
    def _run(X, y, train_index, val_index, random_seed, optimizer, evaluator, benchmark):
        benchm = benchmark(X=X, y=y,
                           train_indices=train_index, valid_indices=val_index,
                           random_seed=random_seed,
                           evaluator=evaluator)
        evo = optimizer(seed=random_seed, **EvoSampling._get_args(optimizer, benchm))
        return evo.run()

    @staticmethod
    def _reduce(mask, results, runs, cv, benchmark, len_y=10):
        occurrences = np.full((len_y, cv), np.nan)  # Columns are number of occurrences in one run

        result_list = [results[x:x + runs] for x in range(0, cv * runs, runs)]
        i = 0
        for cv_one in result_list:
            best_fitness = sys.float_info.max
            best_solution = None
            for result_one in cv_one:
                if (best_solution is None) or (best_fitness > result_one[1]):
                    best_solution, best_fitness = result_one[0], result_one[1]

            occurrences[mask[i], i] = benchmark.genotype_to_map(best_solution)
            i = i + 1

        occurrences = stats.mode(occurrences, axis=1, nan_policy='omit')[0].flatten()

        return occurrences.astype(np.int8)

    @staticmethod
    def _get_args(algorithm, benchmark):
        kwargs = {**es.all_kwargs,
                  **es.kwargs[algorithm],
                  **{'D': len(benchmark.y_train), 'benchmark': benchmark}}
        return kwargs
