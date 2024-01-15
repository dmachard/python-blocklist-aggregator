
import sys
import yaml
import pkgutil
import requests
import logging
import re
import os
from datetime import date
import cdblib

def percent_list(part_list, whole_list):
    """return percent of the part"""
    w = len(whole_list)
    if not w:
        return (w,0)
    p = 100 * float(len(part_list))/float(w)
    return (w,round(100-p, 2))
    
def inspect_source(pattern, string):
    """inspect string to find domains"""
    logging.debug("*** Searching valid domains...")

    # find all domains according to the pattern
    matched_domains = re.findall(pattern, string, re.M)

    # and eliminate duplicated domains
    domains = list(set(d for d in matched_domains))

    # calculate total domains and percent of duplication
    w,p = percent_list(domains,matched_domains)

    logging.debug("*** domains=%s duplicated=%s%%" % (w,p) )
    return domains
    
def fetch(cfg_update=None, cfg_filename=None):
    """fetch sources"""
    # read default config or from file
    try:
        conf = pkgutil.get_data(__package__, 'blocklist.conf')
        cfg =  yaml.safe_load(conf) 
    except Exception as e:
        logging.error("invalid default config: %s" % e)
        sys.exit(1)

    if cfg_filename is not None:
        try:
            with open(cfg_filename, 'r') as stream:
                cfg =  yaml.safe_load(stream)
        except Exception as e:
            logging.error("invalid external cfg file: %s" % e)
            sys.exit(1)

    # overwrite config with external config ?    
    if cfg_update is not None:
        try:
            cfg.update( yaml.safe_load(cfg_update) )
        except Exception as e:
            logging.error("invalid update config: %s" % e)
            sys.exit(1)

    # init logger
    level = logging.INFO
    if cfg["verbose"]: level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s %(message)s', 
                        stream=sys.stdout, level=level)
    
    domains_bl = []

    # feching all sources
    for s in cfg["sources"]:
        for u in s["urls"]:
            try:
                r = requests.get(u, timeout=float(cfg["timeout"]), verify=cfg["tlsverify"])
            except requests.exceptions.RequestException as e:
                logging.error("requests exception: %s" % e)
            else:
                if r.status_code != 200:
                    logging.error("http error: %s" % r.status_code)
                else:
                    domains_bl.extend(inspect_source(s["pattern"], r.text))  
            
    # add more domains to the blocklist ?
    if cfg["blacklist"] is not None:
        domains_bl.extend(cfg["blacklist"])
    
    # remove duplicated domains
    domains_unified = list(set(d for d in domains_bl))
    w,p = percent_list(domains_unified,domains_bl)
    logging.debug("blocklist origin=%s total=%s duplicated=%s%%" % (len(domains_bl), len(domains_unified),p))
    
    # remove domains from the whilelist
    set_domains = set(domains_unified)
    set_whitelist = set(cfg["whitelist"])
    set_domains.difference_update(set_whitelist)
    domains_unified = list(set_domains)
    logging.debug("blocklist without domains from whitelist total=%s" % len(domains_unified))
    
    return domains_unified

def save_to_file(filename, data):
    """save to file"""
    try:
        with open(filename, 'w') as f:
            f.write(data)
    except Exception as e:
        logging.error("unable to save to file: %s" % e)
        return False
    return True

def save_raw(filename, cfg_update=None, cfg_filename=None):
    """save to file with raw format"""
    # feching bad domains
    domains = fetch(cfg_update=cfg_update, cfg_filename=cfg_filename)

    # to avoid empty file
    if len(domains) == 0:
        logging.error("the domain list is empty")
        return
    
    raw = [ "# Generated with blocklist-aggregator" ]
    raw.append( "# Updated: %s" % date.today() )
    raw.append( "" )
    
    raw.extend(domains)
    
    success = save_to_file(filename, "\n".join(raw) )
    if success: 
        logging.debug("raw file saved")
    
def save_hosts(filename, ip="0.0.0.0", cfg_update=None, cfg_filename=None):
    """save to file with hosts format"""
    # feching bad domains
    domains = fetch(cfg_update=cfg_update, cfg_filename=cfg_filename)
    
    # to avoid empty file
    if len(domains) == 0:
        logging.error("the domain list is empty")
        return
    
    hosts = [ "# Generated with blocklist-aggregator" ]
    hosts.append( "# Updated: %s" % date.today() )
    hosts.append( "" )
    
    domains_ = list(map(lambda p: "%s " % ip + p, domains))
    hosts.extend(domains_)
    
    # save-it in a file
    success = save_to_file(filename, "\n".join(hosts) )
    if success:
        logging.debug("hosts file saved")

def save_cdb(filename, default_value="", cfg_update=None, cfg_filename=None):
    """save to CDB database"""
    # feching domains
    domains = fetch(cfg_update=cfg_update, cfg_filename=cfg_filename)

    # to avoid empty file
    if len(domains) == 0:
        logging.error("the domain list is empty")
        return
    
    try:
        with open(filename, 'wb') as f:
            with cdblib.Writer(f) as writer:
                for d in domains:
                    writer.put(d.encode(), default_value.encode())
    except Exception as e:
        logging.error("error to save in cdb file: %s" % e)
    else:
        logging.debug("cdb file saved with success")