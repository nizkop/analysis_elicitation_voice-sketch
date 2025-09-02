import unittest

from src.coding.agreement_rate import agreement_rate


class TestCoding(unittest.TestCase):


    def test_empty_dict(self):
        a = agreement_rate({"gui": 2})
        assert a == 0

        # a = agreement_rate({"gui": 10})
        # assert a == 1
        #TODO

        a = agreement_rate({"gui": 1, "gui2": 1})
        assert a == 0

        a = agreement_rate({"gui": 1, "gui2": 1})
        assert a == 0

        a = agreement_rate({"gui": 1, "gui2": 2})
        assert a == 1/3

        a = agreement_rate({"gui": 10, "gui2": 0})
        assert a == 1

        a = agreement_rate({"gui": 1000000, "gui2": 1000000})
        assert round(a,2) == 0.5

        a = agreement_rate({"gui": 10, "gui2": 10})
        assert round(a,6) == 0.473684

        a = agreement_rate({"gui": 100000, "gui2": 0})
        assert a == 1

        a = agreement_rate({"gui": 10, "gui2": 20})
        assert round(a,5) == 0.54023

        a = agreement_rate({"gui": 2, "gui2": 4})
        assert round(a,6) == 0.466667

        a = agreement_rate({"gui": 20, "gui2": 40})
        assert round(a,6) == 0.548023

        a = agreement_rate({"gui": 1000000, "gui2": 3000000})
        assert round(a,3) == 0.625

        a = agreement_rate({"gui": 1, "gui2": 4})
        assert a == 0.6

        a = agreement_rate({"gui": 10, "gui2": 40})
        assert round(a,6) == 0.673469

if __name__ == "__main__":
    unittest.main()