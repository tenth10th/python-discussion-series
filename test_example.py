import pytest
from io import StringIO


# The default behavior of fixtures to be "function-scoped"
# so that they are called each time they are used by a test case
# (each test case gets its own new a new StringIO object)

# By using module scope, this function/fixture will only be run once per python module
# (Only called once, even if there are multiple test cases in this python module / file)
@pytest.fixture(scope="module")
def simulated_file():
    print("\n(creating a new simulated file)")
    # If we pretend that this is a huge file, that takes a long time to initialize...
    # Only creating it once per module would save some time...
    return StringIO(initial_value="hello world\nthis is line 2\nthis is line 3\nthis is line 4\n")

# "session" scope would only run once per invocation of pytest - even if we use this fixture in multiple files / modules...

@pytest.fixture(scope="function")
def reset_simulated_file(simulated_file):
    print("\n(seeking simulated file to position 0)")
    # But, we want each test to start with the file at position zero
    # (each time this fixture is used, per function)
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
    # The code up to and including the yield, gets run _before_ the test case that depended on this fixture...
    print('\n(expensive generative fixture starting up...)')
    f = open('some_file', 'w')
    yield "1"
    # But the code after the yield, gets run _after_ the the test case has run (and passed or failed)
    # (regardless of whether the test passed or failed)
    print('\n(expensive generative fixture shutting down...)')
    f.close()
    # These will never be reached, because PyTest will instantiate the generator,
    # but only call next() on it once (before the test case(s) in the selected scope)
    yield "2"
    yield "3"

def iterable_generator_factory():
    i = 0
    while i < 10:
        yield i
        i += 1

"""
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


def get_line_three(from_file):
    i = 0
    for line in from_file:
        print(line)
        if i == 2:
            return line
        i += 1
    print("(I guess there is no line 3?!)")
    raise Exception("get_line_three called on a file with less than three lines!")
