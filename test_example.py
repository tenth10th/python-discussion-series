import pytest
from io import StringIO


# The default behavior of fixtures to be "function-scoped"
# so that they are called each time they are used by a test case
# (each test case gets its own new a new StringIO object)

# By using module scope, this function/fixture will only be run once per python module
# (Only called once, even if there are multiple test cases in this python module / file)
@pytest.fixture(scope="module")
def simulated_file():
    """
    Simulates a file using an in-memory "file-like" object - faster and more reliable than a real file
    (while having a near-identical identical API)
    """
    print("\n(creating a new simulated file)")
    # If we pretend that this is a huge file, that takes a long time to initialize...
    # Only creating it once per module would save some time...
    return StringIO(initial_value="hello world\nthis is line 2\nthis is line 3\nthis is line 4\n")

# "session" scope would only run once per invocation of pytest - even if we use this fixture in multiple files / modules...

@pytest.fixture(scope="function")
def reset_simulated_file(simulated_file):
    """
    "higher order" fixture: Resets the position of simulated_file's "file" to 0 before returning
    """
    print("\n(seeking simulated file to position 0)")
    # we want each test to start with the file at position zero
    # (each time this fixture is used - per function!)
    simulated_file.seek(0)
    return simulated_file

# When PyTest calls a Fixture, it reacts to Generators in a special way...
# It both calls the Generator, and essentially calls next() on it
# (so that the yielded value can be passed to Test Case(s)
# But it will continue after the Test Case(s) have run, at the selected scope.
# (after each Function at function scope, or after the module or session is completed in those scopes.)
# NOTE: it will only call next() once, and yield a single value!
# additional yields will not be reached!
@pytest.fixture(scope="function")
def expensive_generative_fixture():
    """
    Example of a generator fixture, which uses yield to implement "before" and "after" behaviors
    """
    # The code up to and including the yield, gets run _before_ the test case that depended on this fixture...
    print('\n(expensive generative fixture starting up...)')
    f = open('some_file', 'w')
    yield "1"
    # But the code after the yield, gets run _after_ the the test case has run (and passed or failed)
    # (regardless of whether the test passed or failed)
    print('\n(expensive generative fixture shutting down...)')
    f.close()
    # These will never be reached, because PyTest will instantiate the generator,
    # but only call next() on it once (before the test case(s) in the selected scope).
    # (actually, the current version PyTest will throw an error in this case!)
    # (so we have to comment out the additional yields for this fixture to be considered valid...)
    # yield "2"
    # yield "3"

def iterable_generator_factory():
    """
    More typical example of a Generator:
    Calling it returns iterable instances of a generator
    (functions that yield are sort of like "generator factories"?)
    """
    i = 0
    while i < 10:
        # Return i, and suspend here until the next iteration...
        yield i
        # Continue here after the next iteration...
        i += 1
    # (Automatically raises StopIteration at this point)

"""
gf = iterable_generator_factory()
for x in gf:

is basically doing something like:
while True:
    try:
        return next(gf)
    except StopIteration:
        break
"""

def test_generative_fixture_A(expensive_generative_fixture):
    print("test_generative_fixture A got result:", expensive_generative_fixture)

def test_generative_fixture_B(expensive_generative_fixture):
    print("test_generative_fixture B got result:", expensive_generative_fixture)


def test_get_line_three_exactly(reset_simulated_file):
    # Assert that our function's output exactly, literally matches
    assert get_line_three(reset_simulated_file) == "this is line 3\n"


def test_get_line_three_roughly(reset_simulated_file):
    # Assert that our function is close enough (ignoring whitespace, including line feed)
    assert get_line_three(reset_simulated_file).strip() == "this is line 3"

def test_with_no_assertions():
    # Just trying to prove that some_function still takes single or multiple arguments!
    some_function(1)
    some_function(1, 2)


def get_line_three(from_file):
    i = 0
    for line in from_file:
        print(line)
        if i == 2:
            return line
        i += 1
    print("(I guess there is no line 3?!)")
    raise Exception("get_line_three called on a file with less than three lines!")

def test_shared_toplevel_fixtures(toplevel_fixture):
    print("toplevel_fixture value:", toplevel_fixture)

# def test_shared_fixtures(example_fixture):
#     print("example_fixture value:", example_fixture)

def some_function(*args):
    return len(args)


@pytest.mark.parametrize(("numbers", "expected_total"), [
    ([1,], 1),
    ([1, 2], 3),
    ([1, 2, 3], 6),
    ([5, 6, 7, 8], 26),
])
def test_sum(numbers, expected_total):
    assert sum(numbers) == expected_total


class SumTestData:
    def __init__(self, numbers, expected_total):
        self.numbers = numbers
        self.expected_total = expected_total

@pytest.fixture(params=[
    SumTestData(numbers=[1, 2], expected_total=3),
    SumTestData(numbers=[1, 2, 3], expected_total=6),
])
def sum_data(request):
    return request.param

def test_sum_with_fixture(sum_data):
    print("Testing with Number:", sum_data)
    assert sum(sum_data.numbers) == sum_data.expected_total


@pytest.fixture(params=['a', 'b', 'c', 'd', 'e', 'f'])
def x_coords(request):
    """
    This fixture has parameters - It will cause a test case to run repeatedly
    (once per parameter value), creating multiple "items", a.k.a. "nodes"
    """
    return request.param

@pytest.fixture(params=[1, 2, 3, 4, 5, 6])
def y_coords(request):
    """
    Another one, but with numerical parameters instead of letters
    """
    return request.param

def battleship(x, y):
    # Pretend this function is doing something really complicated and worth testing...
    if (x == 'c' and y == 5):
        raise Exception("Um, Actually, C5 is not a valid move in this context...")
    print(f"{x}{y}")

def test_battleship(x_coords, y_coords):
    """
    This test depends on two parameterized fixtures - it gets the cartesian product of all the parameters!
    (very similar to what itertools.combinations does - 6 letters x 6 numbers = 36 letter/numbers)
    """
    if (x_coords == 'c' and y_coords == 5):
        pytest.skip("C5 is not valid in this context, but we haven't handled those rules yet...")
    battleship(x_coords, y_coords)

# Multiple fixtures that provide parameters, will 

# More fun with Arguments...

def battleship_2(x, y=1, z=2):
    print(f"{x}{y}{z}")

# X is required, Y is optional (and defaults to 1)
def battleship_3(x, y=1):
    print(f"{x}{y}")

# The * operator implies 0 or more positional arguments
def battleship_4(x, y, *z):
    print(f"{x}{y}{z}")

# The ** operator implies 0 or more keyword arguments
def battleship_5(x, y, **z):
    print(f"{x}{y}{z}")

# This just feels rude?
def battleship_6(x, y, *, z):
    print(f"{x}{y}{z}")

# But this makes the optional z argument more explicit
def battleship_7(x, y, *, z=3):
    print(f"{x}{y}{z}")

import functools

battleship_a = functools.partial(battleship, x='a')

def check_length(indexable, max_size):
    if len(indexable) < max_size:
        return False
    return True

"""
Color (Red, Black)

Suits ('Club', 'Spade', 'Diamond', 'Heart')
Value ('Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King')

A Deck Of Cards = Suit * Value (Cartesian Product of all Suits and all Values)
"""
import itertools

two_letter_combos = itertools.combinations("ABCDEF", 2)  # Get all 15 unique combinations of two letters
two_letter_perms = itertools.permutations("ABCDEF", 2)   # Get all 51 ordered permutations of two letters

print()
print("Combos:", len(list(two_letter_combos)))
print("Perms:", len(list(two_letter_perms)))
print()
