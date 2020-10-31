
import unittest

import blocklist_aggregator

class TestSaving(unittest.TestCase):
    def test1_save_raw(self):
        """test save list of domains as raw format"""
        fn = "blocklist_raw.txt"
        blocklist_aggregator.save_raw(filename=fn)
        
        with open(fn, "r") as f:
            data = f.read()
            
        domains = data.splitlines()  
        self.assertIn("doubleclick.net", domains)
        
    def test2_save_hosts(self):
        """test save list of domains as hosts format"""
        fn = "hosts.txt"
        blocklist_aggregator.save_hosts(filename=fn, ip="0.0.0.0")
        
        with open(fn, "r") as f:
            data = f.read()
            
        domains = data.splitlines()  
        self.assertIn("0.0.0.0 doubleclick.net", domains)