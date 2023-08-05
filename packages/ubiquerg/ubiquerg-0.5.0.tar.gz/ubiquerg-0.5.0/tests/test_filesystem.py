""" Tests for filesystem utilities """

import os
import pytest
from ubiquerg import expandpath

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


class PathTestCase(object):
    """ Bundle data and expectation with context management for a test case. """

    def __init__(self, path, expected, **envs):
        """
        Create the case with raw path, expected result, and envvar updates.

        :param str path: raw path value to use as input to function under test
        :param str expected: expected result of applying function under test
            to raw path value
        """
        self.path = path
        self.expected = expected
        self._originals = {k: os.environ[k] for k in envs if k in os.environ}
        self._updates = envs

    def __enter__(self):
        """ Update environment variables. """
        for k, v in self._updates.items():
            os.environ[k] = v
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Restore environment variables. """
        for k in self._updates:
            try:
                os.environ[k] = self._originals[k]
            except KeyError:
                del os.environ[k]
        for k, v in self._originals.items():
            assert v == os.environ[k]
        for k in set(self._updates.keys()) - set(self._originals.keys()):
            assert k not in os.environ

    def __repr__(self):
        """ Conveniently represent the test case instance. """
        return "Path={}, Exp={}, Envs={}".\
            format(self.path, self.expected, self._updates)


@pytest.mark.parametrize("case", [
    PathTestCase("/a/b//c.txt", "/a/b/c.txt"),
    PathTestCase("double//slash//2.txt", "double/slash/2.txt"),
    PathTestCase(os.path.join("random", "$LIKELY_NEWVAL", "leaf.md"),
                 os.path.join("random", "newval", "leaf.md"),
                 LIKELY_NEWVAL="newval"),
    PathTestCase(os.path.join("arbitrary", "$HOME", "leaf.rst"),
                 os.path.join("arbitrary", "uibvreal", "leaf.rst"),
                 HOME="uibvreal")
])
def test_expandpath(case):
    """ Validate expected path expansion behavior. """
    with case:
        assert case.expected == expandpath(case.path)
