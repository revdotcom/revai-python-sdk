#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest


class TestSpeechrecEndpoints(unittest.TestCase):
    """Basic tests.
    """
    def test_endpoints(self):
        """Check that each call hits the right endpoint.
        """
        tests = ((), )
        targets = ((), )
        for test, target in zip(tests, targets):
            assert test == target, \
                   "{0} is not {1}.".format(test, target)
