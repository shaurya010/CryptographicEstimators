# Beullens
from math import log, inf

load("tests/external_estimators/helpers/attack_cost.sage")

def ext_beullens():
    """Special value test."""

    inputs = [(250r, 125r, q) for q in [11r, 17r, 31r, 53r]]

    def gen_single_kat(input):
        n, k, q = input
        expected_complexity = attack_cost(n, k, q) + log(n, 2r)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_beullens_range():
    """Small values test."""
    inputs = [
        (n, k, q) for n in range(100r, 103r) for k in range(50r, 53r) for q in [7r, 11r]
    ]

    def gen_single_kat(input):
        n, k, q = input

        candidate_1 = attack_cost(n, k, q)
        candidate_2 = attack_cost(n, k, q)

        if candidate_1 is None and candidate_2 is None:
            return None

        final_candidate = min(candidate_1, candidate_2)
        if final_candidate == inf:
            return None

        expected_complexity = final_candidate + log(n, 2)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))

    return [element for element in inputs_with_expected_outputs if element is not None]

# BBPS
load("tests/external_estimators/helpers/cost.sage")


def ext_bbps_1():
    """Special value test."""

    inputs = [(200r, 100r, q) for q in [17r, 31r]]

    def gen_single_kat(input):
        n, k, q = input
        print(n, k, q)
        print(type(n), type(k), type(q))

        expected_complexity, _, _, _ = improved_linear_beullens(n, k, q)

        return input, float(expected_complexity)

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_bbps_2():
    """Special value test.

    For small q we need to allow for a slightly larger tolerance, because the coupon collector approximation is less accurate.
    """

    inputs = [(200r, 100r, 11r)]

    def gen_single_kat(input):
        n, k, q = input

        expected_complexity, _, _, _ = improved_linear_beullens(n, k, q)

        return input, float(expected_complexity)

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


# def correct_coupon_collector(L_prime, Nw_prime):
#     """We use an approximation of the coupon collector for efficiency reasons leading to small deviations for small instances."""
#     if L_prime > Nw_prime - 1:
#         L_prime = 2 ^ L_prime
#         Nw_prime = 2 ^ Nw_prime
#         #      ____________________Approximation_________________   _________________Coupon Collector___________________________
#         return (log2(L_prime) - log2(Nw_prime) + log2(log2(L_prime))) - log2(
#             2 * log(1.0 - L_prime / Nw_prime) / log(1.0 - 1 / Nw_prime) / Nw_prime
#         )
#     return 0


# def ext_bbps_range():
#     """Generic test."""
#     inputs = [
#         (n, k, q)
#         for n in range(100r, 120r, 5r)
#         for k in range(n // 2r, n // 2r + 10r, 2r)
#         for q in [7r, 11r, 17r, 31r]
#     ]
#
#     def gen_single_kat(input):
#         n, k, q = input
#
#         candidate_complexity, _, _, _ = improved_linear_beullens(n, k, q)
#
#         if t2 == 100000000000000:
#             return None
#
#         # FIX: We now don't have "A" (our estimator) to make a correction
#         correction_info = A._get_verbose_information()
#         L, N = verb["L_prime"], verb["Nw_prime"]
#
#         expected_complexity += correct_coupon_collector(L, N)
#
#         return input, expected_complexity
#
#     inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
#
#     return [element for element in inputs_with_expected_outputs if element is not None]
