
import unittest
import warnings

import blocklist_aggregator

class TestFetching(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings('ignore', message='Unverified HTTPS request')

    def test1_fetch(self):
        """test fetch"""
        domains = blocklist_aggregator.fetch()
        
        self.assertIn("doubleclick.net", domains)
        self.assertNotIn("github.com", domains)
        
    def test2_blacklist(self):
        """test blacklist feature"""
        cfg_yaml = "blacklist: [ blocklist-helloworld.com ]"
        
        domains = blocklist_aggregator.fetch(ext_cfg=cfg_yaml)
   
        self.assertIn("blocklist-helloworld.com", domains)
        
    def test3_whitelist(self):
        """test whitelist feature"""
        cfg_yaml = "whitelist: [ doubleclick.net ]"
        
        domains = blocklist_aggregator.fetch(ext_cfg=cfg_yaml)
   
        self.assertNotIn("doubleclick.net", domains)