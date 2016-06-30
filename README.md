# DNS Resolver
Does local DNS resolution using DNS server exports and a list of IP addresses

# Description
Gets hostname for list of IP addresses, created because we have more than 1 authoritative DNS server, each with different DNS records. This consolidates them all and adds some metadata to each record.

# Usage
```
python dns_resolver.py
```

# Prerequisites
* list of all hostname prefixes and corresponding location
* dns records in CSV format

