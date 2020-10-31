
import unittest

import blocklist_aggregator

class TestSaving(unittest.TestCase):
    def test1_save_raw(self):
        """test save list of domains as raw format"""
        fn = "blocklist_raw.txt"
        blocklist_aggregator.save(filename=fn)
        
        with open(fn, "r") as f:
            data = f.read()
            
        domains = data.splitlines()  
        self.assertIn("doubleclick.net", domains)
        