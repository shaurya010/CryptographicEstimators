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


from ..base_problem import BaseProblem
from .pe_constants import *
from math import log2, factorial


class PEProblem(BaseProblem):
    def __init__(self, n: int, k: int, q: int, **kwargs):
        """Construct an instance of the Permutation Code Equivalence Problem.

        Args:
            n (int): Code length
            k (int): Code dimension
            q (int): Field size
            **kwargs: Additional keyword arguments
                h: Dimension of the hull (Default: min(n,n-k), i.e., code is assumed to be weakly self dual)
                nsolutions: Number of (expected) solutions of the problem in logarithmic scale
                memory_bound: Maximum allowed memory to use for solving the problem
        """
        super().__init__(**kwargs)
        self.parameters[PE_CODE_LENGTH] = n
        self.parameters[PE_CODE_DIMENSION] = k
        self.parameters[PE_FIELD_SIZE] = q
        self.parameters[PE_HULL_DIMENSION] = kwargs.get("h", min(n, n - k))
        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity corresponding to basic_operations Fq additions.
    
        Args:
            basic_operations (float): Number of field additions (logarithmic)
        """
        _, _, q, _ = self.get_parameters()
        return basic_operations + log2(log2(q))

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of Fq elements to store.
    
        Args:
            elements_to_store (float): Number of elements to store (logarithmic)
        """
        _, _, q, _ = self.get_parameters()
        return elements_to_store + log2(log2(q))

    def expected_number_solutions(self):
        """Returns the logarithm of the expected number of existing solutions to the problem."""
        n, k, q, _ = self.get_parameters()
        return log2(q) * k * k + log2(factorial(n)) - log2(q) * n * k

    def get_parameters(self):
        """Returns n, k, q and h."""
        return self.parameters.values()

    def __repr__(self):
        n, k, q, _ = self.get_parameters()
        rep = "permutation equivalence problem with (n,k,q) = " \
            + "(" + str(n) + "," + str(k) + "," + str(q) + ")"
        return rep
