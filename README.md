# Blocklist aggregator

![Testing](https://github.com/dmachard/blocklist-aggregator/workflows/Testing/badge.svg) ![Build](https://github.com/dmachard/blocklist-aggregator/workflows/Build/badge.svg) ![Publish](https://github.com/dmachard/blocklist-aggregator/workflows/Publish%20to%20PyPI/badge.svg) 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blocklist_aggregator)

This python module does the aggregation of several ads/tracking/malware lists, and merges them into a unified list with duplicates removed.

See the **[blocklist-domains](https://github.com/dmachard/blocklist-domains)** repository for an implementation.

## Table of contents
* [Installation](#installation)
* [Configuration](#configuration)
* [Basic fetching example](#basic-fetching-example)
* [Fetch and save-it to files](#fetch-and-save-it-to-files)
* [About](#about)

## Installation

If you want to generate your own unified blocklist, 
install this module with the pip command.

```python
pip install blocklist_aggregator
```

## Configuration

See the default [configuration file](../blocklist_aggregator/blocklist.conf)

The configuration contains:
- the ads/tracking/malware URL lists with the pattern (regex) to use
- the domains list to exclude (whitelist)
- additionnal domains list to block (blacklist)

The configuration can be overwritten at runtime.

```python
cfg_yaml = "verbose: true"
unified = blocklist_aggregator.fetch(ext_cfg=cfg_yaml)
```

## Basic fetch example

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

## Fetch and save-it to files

This module can be used to export the list in several format:
- text
- hosts
- CDB (key/value database)

```python
import blocklist_aggregator

# fetch domains
unified = blocklist_aggregator.fetch()

# save to a text file
blocklist_aggregator.save_raw(filename="/tmp/unified_list.txt")

# save to hosts file
blocklist_aggregator.save_hosts(filename="/tmp/unified_hosts.txt", ip="0.0.0.0")

# save to CDB
blocklist_aggregator.save_cdb(filename="/tmp/unified_domains.cdb")
```

## For developpers

Run test units

```bash
python3 -m unittest discover tests/
```
