
import unittest
import cdblib

import blocklist_aggregator

class TestSaving(unittest.TestCase):
    def test1_save_raw(self):
        """test save list of domains as raw format"""
        fn = "./outputs/blocklist_raw.txt"
        blocklist_aggregator.save_raw(filename=fn)
        
        with open(fn, "r") as f:
            data = f.read()
            
        domains = data.splitlines()  
        self.assertIn("doubleclick.net", domains)
        
    def test2_save_hosts(self):
        """test save list of domains as hosts format"""
        fn = "./outputs/hosts.txt"
        blocklist_aggregator.save_hosts(filename=fn, ip="0.0.0.0")
        
        with open(fn, "r") as f:
            data = f.read()
            
        domains = data.splitlines()  
        self.assertIn("0.0.0.0 doubleclick.net", domains)

    def test3_save_cdb(self):
        """test save cdb"""
        fn = "./outputs/blocklist.cdb"
        blocklist_aggregator.save_cdb(filename=fn)
        
        with open(fn, 'rb') as f:
            data = f.read()
        reader = cdblib.Reader(data)

        domains = []
        for key, _ in reader.iteritems():
            domains.append(key)
        self.assertIn(b"doubleclick.net", domains)