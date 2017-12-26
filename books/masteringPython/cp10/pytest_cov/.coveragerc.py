[report]
# The test coverage you require, keeping to 100% is not easily possible for all
# projects but it's a good default for new projects.
fail_under = 100

# These functions are generally only needed for debugging and/or extra safety so
# we want to ignore them from the coverage requirements
exclude_lines =
# Make it possible to ignore blocks of code
pragma: no
cover


# Generally only debug code uses this
def __repr__


# if a debug setting is set, skip testing
if self\.debug:
    if settings.DEBUG

# Don't worry about safety checks and expected errors
raise AssertionError
raise NotImplementedError

# This code will probably never run so don't complain about that
if 0:
    if __name__ == '__main__':


    @abc.abstractmethod


[run]
# make sure we require that all branches of the code is covered.
# so both the if and the else
branch = True

# No need to test the testing code
omit = test_ *.py
