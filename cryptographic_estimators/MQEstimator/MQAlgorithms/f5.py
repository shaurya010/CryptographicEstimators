# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator import degree_of_regularity
from ...MQEstimator.series.nmonomial import NMonomialSeries
from ...helper import ComplexityType
from math import log2, inf
from sage.functions.other import binomial


class F5(MQAlgorithm):
    """
    Construct an instance of F5 complexity estimator

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``w`` -- linear algebra constant (default: 2.81)
    - ``degrees`` -- a list/tuple of degree of the polynomials (default: [2]*m)
    
    
    Note: The F5 time complexity formula takes into account the field equations. Hence, the number columns in a Macaulay 
    matrix corresponding to monomials of degree exactly  `D` in a polynomial ring with `n` variables over `GF(q)` is the 
    coefficient of `z^D`     in the series `H(z) = (1 - z^q)^n / (1-z)^n`

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = F5(MQProblem(n=10, m=5, q=3))
        sage: E
        F5 estimator for the MQ problem with 10 variables and 5 polynomials
    """

    def __init__(self, problem: MQProblem, **kwargs):
        m = problem.npolynomials()
        degrees = kwargs.get('degrees', [2]*m)
        if len(degrees) != m:
            raise ValueError(f"len(degrees) must be equal to {m}")

        super().__init__(problem, **kwargs)
        if degrees == [2]*m:
            self._degrees = [2]*self.npolynomials_reduced()
        else:
            self._degrees = degrees

        self._name = "F5"
        self._time_complexity = None
        self._memory_complexity = None
        self._dreg = None
        self._ncols = None

    def degree_of_polynomials(self):
        """
        Return a list of degree of the polynomials

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=5, q=3))
            sage: E.degree_of_polynomials()
            [2, 2, 2, 2]

        """
        return self._degrees

    def _get_degree_of_regularity(self):
        if self._dreg is None:
            n, m, q = self.get_reduced_parameters()
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        return self._dreg

    def _get_number_of_columns_at_degree_of_regularity(self):
        if self._ncols is None:
            n, _, q = self.get_reduced_parameters()
            dreg = self._get_degree_of_regularity()
            NM = NMonomialSeries(q=q, n=n, max_prec=min(dreg, n) + 2)
            self._ncols = NM.nmonomials_of_degree(dreg)
        return self._ncols

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=15, q=3), bit_complexities=False)
            sage: E.time_complexity()
            29.939974302245272

        TESTS::

            sage: F5(MQProblem(n=10, m=12, q=5)).time_complexity()
            40.46631424550428

        """
        if self.problem.is_underdefined_system():
            raise ValueError("The input system cannot be underdefined")

        _, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        time = w * log2(ncols)
        time += log2(m)
        h = self._h
        return h * log2(q) + max(time, self._time_complexity_fglm())


    def _time_complexity_fglm(self):
        """
        Return the time complexity of the FGLM algorithm for this system

        TEST::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=15, q=3, nsolutions=1))
            sage: E._time_complexity_fglm()
            6.321928094887363
        """
        n, _, q = self.get_reduced_parameters()
        D = 2 ** self.problem.nsolutions
        h = self._h
        return h * log2(q) + log2(n * D ** 3)


    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: F5_ = F5(MQProblem(n=10, m=12, q=5), bit_complexities=False)
            sage: F5_.memory_complexity()
            24.5200748422132

        """
        n, m, _ = self.get_reduced_parameters()
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        memory = max(log2(ncols) * 2, log2(m * n ** 2))
        return memory


    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        """
        if self.problem.is_underdefined_system():
            raise ValueError("The input system cannot be underdefined")

        q = self.problem.order_of_the_field()
        w = self.linear_algebra_constant()
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        time = w * log2(ncols)
        h = self._h
        return h * log2(q) + max(time, self._tilde_o_time_complexity_fglm(parameters))


    def _tilde_o_time_complexity_fglm(self, parameters: dict):
        """
        Return the Ō time complexity of the FGLM algorithm for this system

        """
        q = self.problem.order_of_the_field()
        D = 2 ** self.problem.nsolutions
        h = self._h
        return h * log2(q) + log2(D ** 3)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō  memory complexity of the algorithm for a given set of parameters

        """
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        return log2(ncols) * 2
