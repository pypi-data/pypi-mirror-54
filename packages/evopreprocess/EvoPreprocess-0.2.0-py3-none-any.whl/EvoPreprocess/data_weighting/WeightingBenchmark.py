"""
Helper class which evaluates the weights of instances and transforms the genotype of evolutionary and nature
inspired algorithms from NiaPy to actual weights.
"""

import random

# Authors: Sašo Karakatič <karakatic@gmail.com>
# License: GNU General Public License v3.0
from sklearn.base import ClassifierMixin
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.naive_bayes import GaussianNB


class WeightingBenchmark(object):
    """
    Helper benchmark class for weighting instances.

    Parameters
    ----------
    X : {array-like, sparse matrix}, shape (n_samples, n_features)
        Matrix containing the data which have to be weighted.

    y : array-like, shape (n_samples)
        Corresponding label for each instance in X.

    train_indices : array-like, shape (n_samples)
        Corresponding indices for training instances from X.

    valid_indices : array-like, shape (n_samples)
        Corresponding indices for validation instances from X.

    random_seed : int or None, optional (default=1234)
        It used as seed by the random number generator.

    evaluator : classifier or regressor, optional (default=None)
        The classification or regression object from scikit-learn framework.
        If None, the GausianNB for classification is used.
    """
    def __init__(self,
                 X, y,
                 upper=2,
                 train_indices=None, valid_indices=None,
                 random_seed=1234,
                 evaluator=None):
        self.Lower = 0
        self.Upper = upper  # TODO: Max weight of the instance, should be tested

        self.X_train, self.X_valid = X[train_indices], X[valid_indices]
        self.y_train, self.y_valid = y[train_indices], y[valid_indices]

        self.evaluator = GaussianNB() if evaluator is None else evaluator
        self.evaluator.random_state = random_seed
        self.metric = accuracy_score if self.evaluator is ClassifierMixin else mean_squared_error

        self.random_seed = random_seed
        random.seed(random_seed)

    def function(self):
        def evaluate(D, sol):
            cls = self.evaluator.fit(self.X_train, self.y_train, sample_weight=sol)
            y_predicted = cls.predict(self.X_valid)
            acc = self.metric(self.y_valid, y_predicted)
            acc = (1 - acc) if self.evaluator is ClassifierMixin else acc
            return acc

        return evaluate
