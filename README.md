# Subdomain-Scanner
A handy script for quickly enumerating subdomains before a pentest.

When performing a penetration test against a Web Application, the first step is mapping out the entire attack surface. To that end, I have written this simple but handy script to quickly and methodically enumerate potential subdomains. In particular, this script checks ~60 of the most common subdomain names observed in recent years. The list included can be quickly modified or extended to try different attempts.

```
usage: subdomain_scanner.py [-h] [-t NUM_THREADS] -d DOMAIN

A quick tool for enumerating subdomains

optional arguments:
  -h, --help            show this help message and exit
  -t NUM_THREADS, --threads NUM_THREADS
                        Number of threads to use (Default is 4, Max is 16)
  -d DOMAIN, --domain DOMAIN
                        Domain to enumerate
```
