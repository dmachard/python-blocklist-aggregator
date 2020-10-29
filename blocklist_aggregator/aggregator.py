
import sys
import yaml
import pkgutil
import requests
import logging
import re
import os

def percent_list(part_list, whole_list):
    """return percent of the part"""
    w = len(whole_list)
    p = 100 * float(len(part_list))/float(w)
    return (w,round(100-p, 2))
    
def inspect_source(pattern, string):
    """inspect string to find domains"""
    logging.debug("*** Searching valid domains...")

    # find all domains according to the pattern
    # and eliminate duplicated domains
    domains_all = re.findall(pattern, string)
    domains = list(set(d for d in domains_all))
    
    # calculate total domains and percent of duplication
    w,p = percent_list(domains,domains_all)

    logging.debug("*** domains=%s duplicated=%s%%" % (w,p) )
    return domains
    
def fetch(ext_cfg=None):
    """fetch sources"""
    # read default config
    try:
        conf = pkgutil.get_data(__package__, 'blocklist.conf')
        cfg =  yaml.safe_load(conf) 
    except Exception as e:
        logging.error("invalid config: %s" % e)
        sys.exit(1)

    # overwrite config with external config ?    
    if ext_cfg is not None:
        try:
            cfg.update( yaml.safe_load(ext_cfg) )
        except Exception as e:
            logging.error("invalid external config: %s" % e)
            sys.exit(1)
            
    # init logger
    level = logging.INFO
    if cfg["verbose"]: level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s %(message)s', 
                        stream=sys.stdout, level=level)
    
    domains_bl = []
    domains_wl = []

    # feching all sources
    for s in cfg["sources"]:
        for u in s["urls"]:
            r = requests.get(u)
            if r.status_code != 200:
                logging.error("http error: %s" % r.status_code)
            else:
                domains_bl.extend(inspect_source(s["pattern"], r.text))  

    # remove duplicated domains
    domains_unified = list(set(d for d in domains_bl))
    w,p = percent_list(domains_unified,domains_bl)
    logging.debug("blocklist total=%s duplicated=%s%%" % (len(domains_unified),p))
    
    # remove domains from the whilelist
    domains_unified = list(set(domains_unified) ^ set(cfg["whitelist"]))
    logging.debug("blocklist without domains from whitelist total=%s" % len(domains_unified))
    
    return domains_unified