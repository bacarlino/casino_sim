import random


class Outcome:
    """Contains a single outcome on which a bet can be played."""

    def __init__(self, name, odds):
        """Parameters: name (str), odds (int)."""
        self.name = name
        self.odds = odds

    def win_amount(self, amount):
        """Returns this outcomes odds multiplied by the given amount."""
        return self.odds * amount

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return '{} ({}:1)'.format(self.name, self.odds)

    def __repr__(self):
        return 'Outcome({}, {})'.format(self.name, self.odds)


class Bin(frozenset):
    """Contains a collection of Outcomes that reflect the winning bets."""
    pass


class Wheel:
    """Contains 38 Bins and can select one at random."""
    def __init__(self):
        self.bins = tuple(Bin() for i in range(38))
        self.rng = random.Random()
        self.all_outcomes = {}

    def add_outcome(self, number, outcome):
        """
        Input: number (int) - bin number in range 0 to 37
               outcome (Outcome) - outcome to add to bin
        Adds the given Outcome to the numbered Bin.
        """
        bins = list(self.bins)
        bin_ = list(bins[number])
        bin_.append(outcome)
        bins[number] = Bin(bin_)
        self.bins = tuple(bins)

        if not outcome.name in self.all_outcomes:
            self.all_outcomes[outcome.name] = outcome

    def next(self):
        return self.rng.choice(self.bins)

    def get(self, bin_num):
        return self.bins[bin_num]

    def get_outcome(self, name):
        if name in self.all_outcomes:
            return self.all_outcomes[name]


class BinBuilder:
    """Creates the Outcomes for all 38 individual Bins on the Wheel."""


    def build_bins(self, wheel):
        """Creates Outcome instances and adds them to the appropriate bins."""

        self.straight(wheel)
        self.split(wheel)
        self.street(wheel)
        self.corner(wheel)
        self.line(wheel)
        self.dozen(wheel)
        self.column(wheel)
        self.even_money(wheel)
        self.five(wheel)

    def straight(self, wheel):
        """Creates straight bets and assigns to bins"""

        for num in range(37):
            outcome = Outcome("Straight {}".format(num), 35)
            wheel.add_outcome(num, outcome)
        outcome = Outcome("Straight 00", 35)
        wheel.add_outcome(37, outcome)

    def split(self, wheel):
        """Creates split bets and assigns to bins"""

        for row in range(12):
            n = 3*row + 1
            outcome = Outcome("Split {}-{}".format(str(n), str(n + 1)), 17)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)

            n = 3*row + 2
            outcome = Outcome("Split {}-{}".format(str(n), str(n + 1)), 17)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)

        for n in range(1, 34):
            outcome = Outcome("Split {}-{}".format(str(n), str(n + 3)), 17)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 3, outcome)

    def street(self, wheel):
        """Creates street bets and adds them to the bins"""

        for row in range(12):
            n = 3*row + 1
            name = "Street {}-{}-{}".format(str(n), str(n + 1), str(n + 2))
            outcome = Outcome(name, 11)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)
            wheel.add_outcome(n + 2, outcome)

    def corner(self, wheel):
        """Creates corner bets and adds to bins"""

        for row in range(11):

            n = 3*row + 1
            name = "Corner {}-{}-{}-{}"\
                   .format(str(n), str(n + 1), str(n + 3), str(n + 4))
            outcome = Outcome(name, 8)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)
            wheel.add_outcome(n + 3, outcome)
            wheel.add_outcome(n + 4, outcome)

            n = 3*row + 2
            name = "Corner {}-{}-{}-{}"\
                   .format(str(n), str(n + 1), str(n + 3), str(n + 4))
            outcome = Outcome(name, 8)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)
            wheel.add_outcome(n + 3, outcome)
            wheel.add_outcome(n + 4, outcome)


    def line(self, wheel):
        """Creates line bets and adds them to the bins"""
        for row in range(11):
            n = 3*row + 1
            name = "Line {}-{}-{}-{}-{}-{}".format(str(n), str(n + 1),\
                    str(n + 2), str(n + 3), str(n + 4), str(n + 5))
            outcome = Outcome(name, 5)
            for bin_ in range(n, n + 6):
                wheel.add_outcome(bin_, outcome)

    def dozen(self, wheel):
        """Creates dozen bets and adds them to bins"""

        for d in range(3):
            outcome = Outcome("Dozen {}".format(str(d + 1)), 2)
            for bin_ in range(12):
                wheel.add_outcome(12*d + bin_ + 1, outcome)

    def column(self, wheel):
        """Creates column bets and adds them to the bins"""

        for c in range(3):
            outcome = Outcome("Column {}".format(str(c + 1)), 2)
            for row in range(12):
                wheel.add_outcome(3*row + c + 1, outcome)

    def even_money(self, wheel):
        for n in range(1, 37):
            if 1 <= n < 19:
                wheel.add_outcome(n, Outcome("Low", 1))
            elif 19 <= n < 37:
                wheel.add_outcome(n, Outcome("High", 1))
            if n % 2 == 0:
                wheel.add_outcome(n, Outcome("Even", 1))
            elif n % 2 != 0:
                wheel.add_outcome(n, Outcome("Odd", 1))
            if n in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, \
                     21, 23, 25, 27, 30, 32, 34, 36]:
                wheel.add_outcome(n, Outcome("Red", 1))
            else:
                wheel.add_outcome(n, Outcome("Black", 1))

    def five(self, wheel):
        """Creates a five bet and adds to bins"""

        for bin_ in (0, 1, 2, 3, 37):
            wheel.add_outcome(bin_, Outcome("Five Bet", 6))


class Bet:
    """Associates an amount with an Outcome and a Player"""

    def __init__(self, amount, outcome):
        self.amount_bet = amount
        self.outcome = outcome

    def win_amount(self):
        return (self.amount_bet * self.outcome.odds) + self.amount_bet

    def lose_amount(self):
        return self.amount_bet

    def __str__(self):
        return "{} on {}".format(str(self.amount_bet), str(self.outcome))

    def __repr__(self):
        return "Bet({}, {})".format(self.amount_bet, self.outcome)
