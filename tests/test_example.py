#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest


class Testrev_ai(unittest.TestCase):
    """Basic tests.
    """
    def test_basic(self):
        """Check basic functionality.
        """
        tests = ((), )
        targets = ((), )
        for test, target in zip(tests, targets):
            assert test == target, \
                   "{0} is not {1}.".format(test, target)
