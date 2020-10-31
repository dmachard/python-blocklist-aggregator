
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
        
    def test2_blacklist(self):
        """test blacklist feature"""
        cfg_yaml = "blacklist: [ blocklist-helloworld.com ]"
        
        domains = blocklist_aggregator.fetch(ext_cfg=cfg_yaml)
   
        self.assertIn("blocklist-helloworld.com", domains)