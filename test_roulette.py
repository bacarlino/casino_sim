import unittest
import random
from roulette import *


class TestOutcome(unittest.TestCase):
    """
    Verifies equality between alike outcomes and that the win_amount
    method returns the correct amount.
    """

    def setUp(self):
        self.outcome1 = Outcome("One", 35)
        self.outcome2 = Outcome("One", 35)
        self.outcome3 = Outcome("Red", 1)

    def test_outcome_equality(self):
        self.assertEqual(self.outcome1, self.outcome2)
        self.assertNotEqual(self.outcome1, self.outcome3)
        self.assertEqual(hash(self.outcome1), hash(self.outcome2))

    def test_win_amount(self):
        self.assertEqual(self.outcome1.win_amount(2), 70)
        self.assertEqual(self.outcome1.win_amount(15), 525)
        self.assertEqual(self.outcome3.win_amount(100), 100)


class TestBin(unittest.TestCase):
    """Proves that Bins can be created and hold Outcomes."""

    def test_bin_creation(self):
        self.outcome1 = Outcome("00-0-1-2-3", 6)
        self.outcome2 = Outcome("0", 35)
        self.outcome3 = Outcome("00", 35)

        self.bin1 = Bin({self.outcome1, self.outcome2})
        self.bin2 = Bin({self.outcome1, self.outcome3})

        self.assertIsInstance(self.bin1, Bin)
        self.assertNotEqual(self.bin1, self.bin2)
        self.assertIn(self.outcome1, self.bin1)
        self.assertNotIn(self.outcome2, self.bin2)


class TestWheel(unittest.TestCase):
    """
    Tests that prove Bins can be added to the wheel and a random bin can be
    returned.
    """

    def setUp(self):
        self.outcome1 = Outcome("Five Bet", 6)
        self.outcome2 = Outcome("Straight 0", 35)
        self.outcome3 = Outcome("Straight 00", 35)

        self.bin1 = Bin({self.outcome1, self.outcome2})
        self.bin2 = Bin({self.outcome1, self.outcome3})

        self.wheel = Wheel()
        self.wheel.rng.seed(1)

        self.builder = BinBuilder()

    def test_add_outcomes_to_bins(self):
        """Tests adding outcomes to individual Bins in the Wheel"""

        self.wheel.add_outcome(0, self.outcome1)
        self.wheel.add_outcome(0, self.outcome2)
        self.wheel.add_outcome(37, self.outcome1)
        self.wheel.add_outcome(37, self.outcome3)

        self.assertIsInstance(self.wheel.bins[0], type(Bin()))
        self.assertIsInstance(self.wheel.bins[1], type(Bin()))
        self.assertIsInstance(self.wheel.bins[37],type(Bin()))

        self.assertIn(self.outcome1, self.wheel.bins[0])
        self.assertIn(self.outcome3, self.wheel.bins[37])

    def test_rng_next(self):
        """Seeds a test random number generator for testing"""

        test_rng = random.Random()
        test_rng.seed(1)
        for _ in range(10):
            self.assertIs(self.wheel.next(), test_rng.choice(self.wheel.bins))

    def test_get_bin(self):
        self.builder.build_bins(self.wheel)

        self.assertIn(self.outcome1, self.wheel.get(0))
        self.assertIn(self.outcome1, self.wheel.get(37))
        self.assertIn(self.outcome2, self.wheel.get(0))
        self.assertIn(self.outcome3, self.wheel.get(37))

    def test_add_outcomes_to_all_outcomes(self):
        self.builder.build_bins(self.wheel)
        oc_dict = self.wheel.all_outcomes

        self.assertTrue(oc_dict["Five Bet"] == self.outcome1)
        self.assertTrue(oc_dict["Straight 0"] == self.outcome2)
        self.assertTrue(oc_dict["Straight 00"] == self.outcome3)

    def test_get_outcome_from_all_outcomes(self):
        self.builder.build_bins(self.wheel)
        oc1 = self.wheel.get_outcome("Five Bet")
        oc2 = self.wheel.get_outcome("Straight 0")
        oc3 = self.wheel.get_outcome("Straight 00")

        self.assertTrue(oc1 == self.outcome1)
        self.assertTrue(oc2 == self.outcome2)
        self.assertTrue(oc3 == self.outcome3)


class TestBinBuilder(unittest.TestCase):
    """Tests that BinBuilder correctly populates the bins on the wheel"""

    def setUp(self):
        self.wheel = Wheel()
        self.builder = BinBuilder()


    def test_straight(self):
        self.builder.straight(self.wheel)

        for bin_ in range(37):
            name = "Straight {}".format(str(bin_))
            self.assertIn(Outcome(name, 35), self.wheel.bins[bin_])
            self.assertIn(Outcome("Straight 00", 35), self.wheel.bins[37])

    def test_split(self):
        self.builder.split(self.wheel)

        for row in range(12):
            n = 3*row + 1
            outcome = Outcome("Split {}-{}".format(str(n), str(n + 1)), 17)
            self.assertIn(outcome, self.wheel.bins[n])
            self.assertIn(outcome, self.wheel.bins[n + 1])

            n = 3*row + 2
            outcome = Outcome("Split {}-{}".format(str(n), str(n + 1)), 17)
            self.assertIn(outcome, self.wheel.bins[n])
            self.assertIn(outcome, self.wheel.bins[n + 1])

        for n in range(1, 34):
            outcome = Outcome("Split {}-{}".format(str(n), str(n + 3)), 17)
            self.assertIn(outcome, self.wheel.bins[n])
            self.assertIn(outcome, self.wheel.bins[n + 3])

    def test_street(self):
        self.builder.street(self.wheel)

        for row in range(12):
            n = 3*row + 1
            name = "Street {}-{}-{}".format(str(n), str(n + 1), str(n + 2))
            outcome = Outcome(name, 11)
            self.assertIn(outcome, self.wheel.bins[n])
            self.assertIn(outcome, self.wheel.bins[n + 1])
            self.assertIn(outcome, self.wheel.bins[n + 2])

    def test_corner(self):
        self.builder.corner(self.wheel)

        for row in range(11):

            n = 3*row + 1
            name = "Corner {}-{}-{}-{}"\
                   .format(str(n), str(n + 1), str(n + 3), str(n + 4))
            outcome = Outcome(name, 8)
            self.assertIn(outcome, self.wheel.bins[n])
            self.assertIn(outcome, self.wheel.bins[n + 1])
            self.assertIn(outcome, self.wheel.bins[n + 3])
            self.assertIn(outcome, self.wheel.bins[n + 4])

            n = 3*row + 2
            name = "Corner {}-{}-{}-{}"\
                   .format(str(n), str(n + 1), str(n + 3), str(n + 4))
            outcome = Outcome(name, 8)
            self.assertIn(outcome, self.wheel.bins[n])
            self.assertIn(outcome, self.wheel.bins[n + 1])
            self.assertIn(outcome, self.wheel.bins[n + 3])
            self.assertIn(outcome, self.wheel.bins[n + 4])

    def test_line(self):
        self.builder.line(self.wheel)

        for row in range(11):
            n = 3*row + 1
            name = "Line {}-{}-{}-{}-{}-{}".format(str(n), str(n + 1),\
                    str(n + 2), str(n + 3), str(n + 4), str(n + 5))
            outcome = Outcome(name, 5)
            for bin_ in range(n, n + 6):
                self.assertIn(outcome, self.wheel.bins[bin_])

    def test_dozen(self):
        self.builder.dozen(self.wheel)

        for d in range(3):
            outcome = Outcome("Dozen {}".format(str(d + 1)), 2)
            for bin_ in range(12):
                self.assertIn(outcome, self.wheel.bins[12*d + bin_ + 1])

    def test_column(self):
        self.builder.column(self.wheel)

        for c in range(3):
            outcome = Outcome("Column {}".format(str(c + 1)), 2)
            for row in range(12):
                self.assertIn(outcome, self.wheel.bins[3*row + c + 1])

    def test_even_money(self):
        self.builder.even_money(self.wheel)

        for n in range(1, 37):
            if 1 <= n < 19:
                self.assertIn(Outcome("Low", 1), self.wheel.bins[n])
            elif 19 <= n < 37:
                self.assertIn(Outcome("High", 1), self.wheel.bins[n])
            if n % 2 == 0:
                self.assertIn(Outcome("Even", 1), self.wheel.bins[n])
            elif n % 2 != 0:
                self.assertIn(Outcome("Odd", 1), self.wheel.bins[n])
            if n in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, \
                     21, 23, 25, 27, 30, 32, 34, 36]:
                self.assertIn(Outcome("Red", 1), self.wheel.bins[n])
            else:
                self.assertIn(Outcome("Black", 1), self.wheel.bins[n])

    def test_build_bins(self):
        self.builder.build_bins(self.wheel)

        for bin_ in range(38):
            self.assertTrue(len(self.wheel.bins[bin_]) > 0)


class TestBet(unittest.TestCase):

    def setUp(self):
        self.outcome1 = Outcome("Five Bet", 6)
        self.outcome2 = Outcome("Straight 0", 35)
        self.outcome3 = Outcome("Red", 1)

        self.bet1 = Bet(32, self.outcome1)
        self.bet2 = Bet(7, self.outcome2)
        self.bet3 = Bet(500, self.outcome3)

    def test_win_amount(self):
        self.assertTrue(self.bet1.win_amount() == 224)
        self.assertTrue(self.bet2.win_amount() == 252)
        self.assertTrue(self.bet3.win_amount() == 1000)

    def test_lose_amount(self):
        self.assertTrue(self.bet1.lose_amount() == 32)
        self.assertTrue(self.bet2.lose_amount() == 7)
        self.assertTrue(self.bet3.lose_amount() == 500)


if __name__ == '__main__':
    unittest.main()
