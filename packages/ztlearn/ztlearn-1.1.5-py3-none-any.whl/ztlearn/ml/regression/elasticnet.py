# -*- coding: utf-8 -*-

from .base import Regression
from ztlearn.utils import normalize
from sklearn.preprocessing import PolynomialFeatures


class ElasticNetRegression(Regression):

    def __init__(self,
                       degree         = 2,
                       epochs         = 100,
                       loss           = 'mean_squared_error',
                       init_method    = 'random_normal',
                       optimizer      = {},
                       penalty        = 'elastic',
                       penalty_weight = 0.5,
                       l1_ratio       = 0.5):

        self.degree = degree
        super(ElasticNetRegression, self).__init__(epochs         = epochs,
                                                   loss           = loss,
                                                   init_method    = init_method,
                                                   optimizer      = optimizer,
                                                   penalty        = 'elastic', # force to elastic
                                                   penalty_weight = penalty_weight,
                                                   l1_ratio       = l1_ratio)

    def fit(self, inputs, targets, verbose = False, normalized = True):
        polynomial_inputs = PolynomialFeatures(degree = self.degree).fit_transform(inputs)

        if normalized:
            polynomial_inputs = normalize(polynomial_inputs)

        fit_stats = super(ElasticNetRegression, self).fit(polynomial_inputs, targets, verbose)

        return fit_stats

    def predict(self, inputs, normalized = True):
        polynomial_inputs = PolynomialFeatures(degree = self.degree).fit_transform(inputs)

        if normalized:
            polynomial_inputs = normalize(polynomial_inputs)

        return super(ElasticNetRegression, self).predict(polynomial_inputs)
