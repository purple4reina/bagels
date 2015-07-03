"""
A very smart computer that can beat Rachel's Bagels game
"""

from decimal import Decimal
import itertools
import random


# there are three different things that the computer can get back
# Bagels (nothing is right)
# Pico (there is a number that is correct but not in the correct spot)
# Fermi (there is a number that is correct and in the correct spot)
# When a Bagels is found, the we know that none of those three numbers is
# correct, so all three of them could be removed from all three locations. I
# will use a list of sets to represent the possible values. The numbers that
# are in each set will represent the possibilities that are still available
# there. I'll start with the easiest, a 3 number game. There will be 1-9 in the
# first set, then 0-9 in the last two.

# I'll create three different objects to represent each of Bagel, Pico, and
# Fermi

class Response(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

BAGELS = Response('Bagels')
PICO = Response('Pico')
FERMI = Response('Fermi')

# Now I can use real words to represent this stuff

def create_all_possibilities(length):
    """
    Given a length, create a list of tuples that represents all the
    possibilities

    Items are integers, none can repeat, the first cannot be 0
    """

    if length == 1:
        return [(x,) for x in xrange(1, 10)]
    elif length < 1:
        return []

    possibilities = []
    for num in xrange(10 ** length):
        if len(str(num)) < length:
            continue
        elif len(set(str(num))) < length:
            continue
        possibility = tuple(int(digit) for digit in str(num))
        possibilities.append(possibility)

    return possibilities


def update_possibilities(guess, responses, possibilities):
    """
    Given the guess that was made and the list of responses received, update
    the possibilities list and return it

    `guess`: a list of integers
    `responses`: a list of responses (BAGELS, PICO, FERMI)
    """
    # remove the guess from the possibilities
    # TODO: why is it that the guess would be in the possibilities more than
    # once?
    while guess in possibilities:
        possibilities.remove(guess)

    if BAGELS in responses:
        possibilities = update_bagel_possibilities(guess, possibilities)
    if FERMI in responses:
        possibilities = update_fermi_possibilities(guess, possibilities)
    if PICO in responses:
        possibilities = update_pico_possibilities(guess, possibilities)

    if responses.count(FERMI) == 2:
        possibilities = update_two_fermi_possibilities(guess, possibilities)
    if responses.count(PICO) == 2:
        possibilities = update_two_pico_possibilities(guess, possibilities)

    if PICO in responses and FERMI in responses:
        possibilities = update_pico_and_fermi_possibilities(
            guess, possibilities)

    if responses.count(PICO) == 3:
        possibilities = update_three_pico_possibilities(guess, possibilities)

    if responses.count(PICO) == 2 and FERMI in responses:
        possibilities = update_two_pico_one_fermi_possibilities(
            guess, possibilities)

    return possibilities


def update_two_pico_one_fermi_possibilities(guess, possibilities):
    # reduces to 7.358 (which was the same it was before)
    new_possibilities = []
    for poss in possibilities:
        for index_1, index_2, index_3 in itertools.combinations(range(len(guess)), 3):
            g1 = guess[index_1]
            g2 = guess[index_2]
            g3 = guess[index_3]
            p1 = poss[index_1]
            p2 = poss[index_2]
            p3 = poss[index_3]

            if (g1 != p1 and
                    g2 != p2 and
                    g3 != p3):
                continue
            elif (g1 not in poss or
                    g2 not in poss or
                    g3 not in poss):
                continue
            elif g1 == p1 and g2 == p2:
                continue
            elif g1 == p1 and g3 == p3:
                continue
            elif g2 == p2 and g3 == p3:
                continue
            else:
                new_possibilities.append(poss)
    return new_possibilities


def update_three_pico_possibilities(guess, possibilities):
    # this method reduces the tries to 7.358
    new_possibilities = []
    for poss in possibilities:
        # FIXME: this assumes there are only three items in guess
        g1 = guess[0]
        g2 = guess[1]
        g3 = guess[2]
        p1 = poss[0]
        p2 = poss[1]
        p3 = poss[2]

        if g1 not in poss or g2 not in poss or g3 not in poss:
            continue
        elif g1 == p1:
            continue
        elif g2 == p2:
            continue
        elif g3 == p3:
            continue
        else:
            new_possibilities.append(poss)

    return new_possibilities


def update_pico_and_fermi_possibilities(guess, possibilities):
    # means that one must be in the correct place and one must be in the wrong
    # place
    # adding this method increases the total guesses from 7.421 to 7.4398
    # (how? maybe because it changes the order in which the guesses are
    # selected?)
    new_possibilities = []
    for poss in possibilities:
        for index_1, index_2 in itertools.combinations(range(len(guess)), 2):
            g1 = guess[index_1]
            g2 = guess[index_2]
            p1 = poss[index_1]
            p2 = poss[index_2]

            # both numbers must be in the poss
            if g1 not in poss or g2 not in poss:
                continue
            elif g1 == p1 and g2 != p2:
                new_possibilities.append(poss)
            elif g2 == p2 and g1 != g2:
                new_possibilities.append(poss)

    return new_possibilities


def update_two_fermi_possibilities(guess, possibilities):
    # two of them must be correct, not just one
    # adding this method decreases the total guesses from 8.265 to 7.736
    new_possibilities = []
    for poss in possibilities:
        for index_1, index_2 in itertools.combinations(range(len(guess)), 2):
            if (poss[index_1] == guess[index_1] and
                    poss[index_2] == guess[index_2]):
                new_possibilities.append(poss)

    return new_possibilities


def update_two_pico_possibilities(guess, possibilities):
    # adding this methods decreases the total guesses from 7.736 to 7.421
    new_possibilities = []
    for poss in possibilities:
        for index_1, index_2 in itertools.combinations(range(len(guess)), 2):
            g1 = guess[index_1]
            g2 = guess[index_2]
            p1 = poss[index_1]
            p2 = poss[index_2]

            if (g1 != p1 and
                    g2 != p2 and
                    g1 in poss and
                    g2 in poss):
                new_possibilities.append(poss)

    return new_possibilities


def update_bagel_possibilities(guess, possibilities):
    # if the response is bagels, then we know that all the numbers in the
    # guess are not in any of the possibilities
    new_possibilities = []
    for possibility in possibilities:
        for digit in guess:
            if digit in possibility:
                break
        else:
            new_possibilities.append(possibility)
    return new_possibilities


def update_fermi_possibilities(guess, possibilities):
    # one of the numbers is correct, remove any possibilities that have
    # none of the available numbers in them, for example if the guess is
    # [1, 2, 3] then anything that does not have a 1 in the first place, a
    # 2 in the second, or a 3 in the last should be removed.
    new_possibilities = []
    for poss in possibilities:
        for i in xrange(len(guess)):
            if guess[i] == poss[i]:
                new_possibilities.append(poss)

    return new_possibilities


def update_pico_possibilities(guess, possibilities):
    # one of the numbers is correct but in the wrong place. if the guess was
    # [1, 2, 3] then we know that the answer must have a 1, 2, or 3 in it. but,
    # the digit, if in the possibility, cannot be in the same place.
    new_possibilities = []
    for poss in possibilities:
        for digit in guess:
            if digit in poss and guess.index(digit) != poss.index(digit):
                new_possibilities.append(poss)
                break

    return new_possibilities


def get_next_guess_and_updated_possibilities(prev_guess, responses, possibilities):
    """
    Return the computer's next guess based on relavent information

    Return tuple: the next guess, the total possibilities left
    """
    next_possibilities = update_possibilities(prev_guess, responses, possibilities)
    next_guess = get_next_guess(next_possibilities)
    return next_guess, next_possibilities


def get_next_guess(possibilities):
    """
    Given the set of remaining possibilities, return the next guess
    """
    # return the first of the list
    # 10.15895061728395061728395062
    #return possibilities[0]

    # return the middle of the list
    # 8.265432098765432098765432099
    #mid_index = len(possibilities) / 2
    #return possibilities[mid_index]

    # what happens if it is random?
    # this reduces the probability to around 7 (non-precise)
    return random.choice(possibilities)


def get_responses_from_guess(guess, actual):
    """
    Given the guess and the actual answer, return the responses that represent
    which numbers are in the correct location or not
    """
    responses = []
    for index in xrange(len(guess)):
        if guess[index] == actual[index]:
            responses.append(FERMI)
        elif guess[index] in actual:
            responses.append(PICO)
        else:
            responses.append(BAGELS)

    if set(responses) == set([BAGELS]):
        # only return one BAGELS
        responses = [BAGELS]
    elif BAGELS in responses:
        # if something other than BAGELS is in the list, remove all instances
        # of BAGELS
        while BAGELS in responses:
            responses.remove(BAGELS)

    return responses


def test_effectiveness(length=3):
    """
    Given the length of the number to guess, return the average number of
    guesses required to find the solution
    """
    actuals_list = create_all_possibilities(length)
    total_tries = 0
    total_actuals = 0

    for actual in actuals_list:
        tries = get_number_of_tries_required(actual)
        total_tries += tries
        total_actuals += 1

    return Decimal(total_tries) / Decimal(total_actuals)


def get_number_of_tries_required(actual):
    """
    Given the actual answer, return the number of tries it takes for the
    computer to find the answer
    """
    length = len(actual)
    resp = []
    tries = 0
    possibilities = create_all_possibilities(length)

    # assume an empty guess first, the first real guess will be decided the
    # fist time `get_next_guess_and_updated_possibilities` is called
    guess = []

    while resp != [FERMI] * length:
        tries += 1
        guess, possibilities = get_next_guess_and_updated_possibilities(guess, resp, possibilities)
        resp = get_responses_from_guess(guess, actual)

    return tries


if __name__ == '__main__':
    print test_effectiveness()
