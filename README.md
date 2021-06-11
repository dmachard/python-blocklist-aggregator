# Blocklist aggregator

![Testing](https://github.com/dmachard/blocklist-aggregator/workflows/Testing/badge.svg) ![Build](https://github.com/dmachard/blocklist-aggregator/workflows/Build/badge.svg) ![Publish](https://github.com/dmachard/blocklist-aggregator/workflows/Publish%20to%20PyPI/badge.svg) 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blocklist_aggregator)

This python module does the aggregation of several ads/tracking/malware lists, and merges them into a unified list with duplicates removed.

See the **[blocklist-domains](https://github.com/dmachard/blocklist-domains)** repository for an implementation.

## Table of contents
* [Installation](#installation)
* [Configuration](#configuration)
* [Basic example](#basic-example)
* [Fetching in verbose mode](#fetching-in-verbose-mode)
* [About](#about)

## Installation

If you want to generate your own unified blocklist, 
install this module with the pip command.

```python
pip install blocklist_aggregator
```

## Configuration

See the default [configuration file](https://github.com/dmachard/blocklist-aggregator/blob/main/blocklist_aggregator/blocklist.conf)

The configuration contains:
- the ads/tracking/malware URL lists with the pattern (regex) to use
- the domains list to exclude (whitelist)
- additionnal domains list to block (blacklist)

```yaml
# verbose mode, true to active debug logs
verbose: false

# http client options
tlsverify: true
timeout: 5.0

# blocklist sources files
# list of url to download and the pattern 
# to find domain in the content
sources:
  - urls:
      - https://easylist.to/easylist/easylist.txt
      - https://raw.githubusercontent.com/paulgb/BarbBlock/master/BarbBlock.txt
    patterns:
      - ^(?:\|\|)((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])(?:\^)$
  - urls:
      - https://winhelp2002.mvps.org/hosts.txt
      - https://adaway.org/hosts.txt
      - https://raw.githubusercontent.com/StevenBlack/hosts/master/data/StevenBlack/hosts
      - https://urlhaus.abuse.ch/downloads/hostfile/
      - https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts;showintro=0
      - https://someonewhocares.org/hosts/hosts
      - https://raw.githubusercontent.com/notracking/hosts-blocklists/master/hostnames.txt
      - https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt
      - https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt
      - https://raw.githubusercontent.com/davidonzo/Threat-Intel/master/lists/latestdomains.piHole.txt
      - https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts
      - https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt
      - https://raw.githubusercontent.com/notracking/hosts-blocklists/master/dnscrypt-proxy/dnscrypt-proxy.blacklist.txt
    patterns:
      # ignore commented lines
      - ^(?!#).+$
      # search domains with result of the previous regex
      - (?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]

# list of domains to exclude from the blocklist
whitelist:
  - localhost.localdomain
  
# list of domains to include in the blocklist
blacklist: []
```

The configuration can be overwritten at runtime.

```python
cfg_yaml = "verbose: true"
unified = blocklist_aggregator.fetch(ext_cfg=cfg_yaml)
```

## Basic example

This basic example enable to get a unified list of domains.
You can save-it in a file or do what you want.

```python
import blocklist_aggregator

unified = blocklist_aggregator.fetch()
print(unified)
[ "doubleclick.net", ..., "telemetry.dropbox.com" ]

print(len(unified))
152978
```

## Fetching in verbose mode

Fetching ads/tracking/malware URL lists in debug mode
```
2020-10-29 06:47:17,220 Starting new HTTPS connection (1): easylist.to:443
2020-10-29 06:47:17,473 https://easylist.to:443 "GET /easylist/easylist.txt HTTP/1.1" 200 472389
2020-10-29 06:47:17,669 *** Searching valid domains...
2020-10-29 06:47:17,710 *** domains=23672 duplicated=10.26%
2020-10-29 06:47:17,710 Starting new HTTPS connection (1): raw.githubusercontent.com:443
2020-10-29 06:47:18,013 https://raw.githubusercontent.com:443 "GET /paulgb/BarbBlock/master/BarbBlock.txt HTTP/1.1" 200 4701
2020-10-29 06:47:18,020 *** Searching valid domains...
2020-10-29 06:47:18,022 *** domains=550 duplicated=1.09%
2020-10-29 06:47:18,027 Starting new HTTPS connection (1): winhelp2002.mvps.org:443
2020-10-29 06:47:19,065 https://winhelp2002.mvps.org:443 "GET /hosts.txt HTTP/1.1" 200 87636
2020-10-29 06:47:19,343 *** Searching valid domains...
2020-10-29 06:47:19,413 *** domains=11730 duplicated=1.49%
2020-10-29 06:47:19,413 Starting new HTTPS connection (1): adaway.org:443
2020-10-29 06:47:19,654 https://adaway.org:443 "GET /hosts.txt HTTP/1.1" 200 48536
2020-10-29 06:47:19,666 *** Searching valid domains...
2020-10-29 06:47:19,714 *** domains=9002 duplicated=7.52%
2020-10-29 06:47:19,721 Starting new HTTPS connection (1): raw.githubusercontent.com:443
2020-10-29 06:47:20,193 https://raw.githubusercontent.com:443 "GET /StevenBlack/hosts/master/data/StevenBlack/hosts HTTP/1.1" 200 21683
2020-10-29 06:47:20,201 *** Searching valid domains...
2020-10-29 06:47:20,212 *** domains=2938 duplicated=0.0%
2020-10-29 06:47:20,212 Starting new HTTPS connection (1): www.malwaredomainlist.com:443
2020-10-29 06:47:20,944 https://www.malwaredomainlist.com:443 "GET /hostslist/hosts.txt HTTP/1.1" 200 35585
2020-10-29 06:47:21,039 *** Searching valid domains...
2020-10-29 06:47:21,057 *** domains=1106 duplicated=0.0%
2020-10-29 06:47:21,057 Starting new HTTPS connection (1): urlhaus.abuse.ch:443
2020-10-29 06:47:21,340 https://urlhaus.abuse.ch:443 "GET /downloads/hostfile/ HTTP/1.1" 200 19478
2020-10-29 06:47:21,459 *** Searching valid domains...
2020-10-29 06:47:21,479 *** domains=2280 duplicated=0.04%
2020-10-29 06:47:21,485 Starting new HTTPS connection (1): pgl.yoyo.org:443
2020-10-29 06:47:21,731 https://pgl.yoyo.org:443 "GET /adservers/serverlist.php?hostformat=hosts;showintro=0 HTTP/1.1" 200 24153
2020-10-29 06:47:21,743 *** Searching valid domains...
2020-10-29 06:47:21,792 *** domains=3568 duplicated=0.14%
2020-10-29 06:47:21,799 Starting new HTTPS connection (1): someonewhocares.org:443
2020-10-29 06:47:22,849 https://someonewhocares.org:443 "GET /hosts/hosts HTTP/1.1" 200 449957
2020-10-29 06:47:24,029 *** Searching valid domains...
2020-10-29 06:47:24,138 *** domains=14662 duplicated=0.85%
2020-10-29 06:47:24,143 Starting new HTTPS connection (1): raw.githubusercontent.com:443
2020-10-29 06:47:24,378 https://raw.githubusercontent.com:443 "GET /notracking/hosts-blocklists/master/hostnames.txt HTTP/1.1" 200 1468999
2020-10-29 06:47:24,738 *** Searching valid domains...
2020-10-29 06:47:25,124 *** domains=194622 duplicated=50.0%
2020-10-29 06:47:25,128 Starting new HTTPS connection (1): s3.amazonaws.com:443
2020-10-29 06:47:25,824 https://s3.amazonaws.com:443 "GET /lists.disconnect.me/simple_ad.txt HTTP/1.1" 200 43616
2020-10-29 06:47:25,866 *** Searching valid domains...
2020-10-29 06:47:25,873 *** domains=2702 duplicated=0.0%
2020-10-29 06:47:25,873 Starting new HTTPS connection (1): s3.amazonaws.com:443
2020-10-29 06:47:26,383 https://s3.amazonaws.com:443 "GET /lists.disconnect.me/simple_tracking.txt HTTP/1.1" 200 613
2020-10-29 06:47:26,390 *** Searching valid domains...
2020-10-29 06:47:26,390 *** domains=35 duplicated=0.0%
2020-10-29 06:47:26,393 Starting new HTTPS connection (1): raw.githubusercontent.com:443
2020-10-29 06:47:26,573 https://raw.githubusercontent.com:443 "GET /davidonzo/Threat-Intel/master/lists/latestdomains.piHole.txt HTTP/1.1" 200 21830
2020-10-29 06:47:26,575 *** Searching valid domains...
2020-10-29 06:47:26,613 *** domains=2193 duplicated=0.05%
2020-10-29 06:47:26,624 Starting new HTTPS connection (1): raw.githubusercontent.com:443
2020-10-29 06:47:26,839 https://raw.githubusercontent.com:443 "GET /mitchellkrogza/Badd-Boyz-Hosts/master/hosts HTTP/1.1" 200 7888
2020-10-29 06:47:26,850 *** Searching valid domains...
2020-10-29 06:47:26,857 *** domains=834 duplicated=0.48%
2020-10-29 06:47:26,893 blocklist total=152978 duplicated=9.57%
2020-10-29 06:47:26,941 blocklist without domains from whitelist total=152977
```

# About

| | |
| ------------- | ------------- |
| Author | Denis Machard <d.machard@gmail.com> |
| PyPI | https://pypi.org/project/blocklist_aggregator/ |
| | |
