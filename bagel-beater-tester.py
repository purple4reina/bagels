import unittest

import bagelbeater as bb


class BaseTestUpdatePossibilities(object):
    """
    Base class for all UpdatePossibilities tests in this module. Test cases are
    defined here for each of those. The child class will define what length the
    guesses will be
    """

    def test_same_guess_twice_both_bagel(self):
        # TODO: this assumes guess of length 3
        bb.update_possibilities((1, 2, 3), [bb.BAGELS], self.possibilities)
        bb.update_possibilities((1, 2, 3), [bb.BAGELS], self.possibilities)

    def test_update_bagel_poss(self):
        # TODO: this assumes guess of length 3
        posses = bb.update_bagel_possibilities((1, 2, 3), self.possibilities)

        for poss in posses:
            assert(1 not in poss)
            assert(2 not in poss)
            assert(3 not in poss)

        # include the = for guess len 0 case
        assert(len(posses) <= len(self.possibilities))

    def test_update_pico_poss_make_sure_no_doubles(self):
        posses = bb.update_pico_possibilities((1, 2, 3), self.possibilities)
        assert(len(set(posses)) == len(posses))

    def test_get_responses(self):
        actual = (1, 2, 3)

        guess = (1, 2, 3)
        resp = bb.get_responses_from_guess(guess, actual)
        self.assertEqual(resp, [bb.FERMI, bb.FERMI, bb.FERMI])

        guess = (4, 5, 6)
        resp = bb.get_responses_from_guess(guess, actual)
        self.assertEqual(resp, [bb.BAGELS])

        guess = (1, 5, 6)
        resp = bb.get_responses_from_guess(guess, actual)
        self.assertEqual(resp, [bb.FERMI])

        guess = (3, 1, 2)
        resp = bb.get_responses_from_guess(guess, actual)
        self.assertEqual(resp, [bb.PICO, bb.PICO, bb.PICO])

        guess = (1, 3, 5)
        resp = bb.get_responses_from_guess(guess, actual)
        self.assertEqual(resp, [bb.FERMI, bb.PICO])

        guess = (1, 0, 3)
        actual = (1, 0, 3)
        resp = bb.get_responses_from_guess(guess, actual)
        self.assertEqual(resp, [bb.FERMI, bb.FERMI, bb.FERMI])


class TestUpdatePossibilities3(BaseTestUpdatePossibilities, unittest.TestCase):
    """
    Tests when possibilities are of length 3
    """
    def setUp(self):
        self.possibilities = bb.create_all_possibilities(3)

    def test_fermi_poss(self):
        posses = bb.update_fermi_possibilities((1, 2, 3), self.possibilities)
        assert((4, 5, 6) not in posses)
        # assuming [FERMI, FERMI]
        assert((1, 2, 6) in posses)

    def test_pico_poss_not_in_same_space(self):
        posses = bb.update_pico_possibilities((1, 2, 3), self.possibilities)
        assert((1, 2, 3) not in posses)
        assert((1, 4, 5) not in posses)
        assert((4, 5, 1) in posses)

    def test_two_fermi(self):
        posses = bb.update_two_fermi_possibilities((1, 2, 3), self.possibilities)
        assert((1, 2, 4) in posses)
        assert((1, 5, 6) not in posses)

    def test_two_pico(self):
        posses = bb.update_two_pico_possibilities((1, 2, 3), self.possibilities)
        assert((4, 1, 2) in posses)
        assert((4, 5, 1) not in posses)

    def test_pico_and_fermi(self):
        posses = bb.update_pico_and_fermi_possibilities(
            (1, 2, 3), self.possibilities)
        assert((1, 3, 0) in posses)
        assert((1, 4, 5) not in posses)

    def test_three_pico(self):
        posses = bb.update_three_pico_possibilities(
            (1, 2, 3), self.possibilities)
        assert((2, 3, 1) in posses)
        assert((2, 3, 4) not in posses)

    def test_two_pico_one_fermi(self):
        posses = bb.update_two_pico_one_fermi_possibilities(
            (1, 2, 3), self.possibilities)
        assert((1, 3, 2) in posses)
        assert((2, 3, 1) not in posses)
        assert((1, 2, 4) not in posses)


class TestUpdatePossibilities2(BaseTestUpdatePossibilities, unittest.TestCase):
    """
    Tests when possibilities are of length 2
    """
    def setUp(self):
        self.possibilities = bb.create_all_possibilities(2)

    def test_fermi_poss(self):
        posses = bb.update_fermi_possibilities((1, 2), self.possibilities)
        assert((4, 5) not in posses)


class TestUpdatePossibilities1(BaseTestUpdatePossibilities, unittest.TestCase):
    """
    Tests when possibilities are of length 1
    """
    def setUp(self):
        self.possibilities = bb.create_all_possibilities(1)

    def test_fermi_poss(self):
        posses = bb.update_fermi_possibilities((1,), self.possibilities)
        assert((4,) not in posses)


class TestUpdatePossibilities0(BaseTestUpdatePossibilities, unittest.TestCase):
    """
    Tests when possibilities are of length 0
    """
    def setUp(self):
        self.possibilities = bb.create_all_possibilities(0)


if __name__ == '__main__':
    unittest.main()
