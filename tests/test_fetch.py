
import time
import unittest
import subprocess
import logging

import blocklist_aggregator

class TestFetching(unittest.TestCase):
    def test1_fetch(self):
        """test fetch"""
        domains = blocklist_aggregator.fetch()
        
        self.assertIn("doubleclick.net", domains)