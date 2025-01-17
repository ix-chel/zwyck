from colorama import Fore, init, Style
from os import path
from builtwith import builtwith
from modules.favicon import *
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin, urlencode, parse_qs, quote_plus
from modules import useragent_list
from modules import sub_output
from googlesearch import search
from alive_progress import alive_bar
from queue import Queue
from shutil import which
from collections import defaultdict
from threading import Semaphore
from ratelimit import limits, sleep_and_retry
from modules.jwt_analyzer import JWTAnalyzer
from modules.ss3sec import S3Scanner
from datetime import datetime
from modules.heap_dump import HeapdumpAnalyzer
import waybackpy
import threading
import os.path
import concurrent.futures
import multiprocessing
import dns.resolver
import os.path
import whois
import socket
import subprocess
import sys
import socket
import os
import argparse
import time
import codecs
import requests
import mmh3
import urllib3
import warnings
import re
import json
import shodan
import ipaddress
import random
import string
import html
import asyncio
import aiohttp
import hashlib
import urllib
import nmap3
import ssl
import shutil


warnings.filterwarnings(action='ignore',module='bs4')

requests.packages.urllib3.disable_warnings()

banner = f"""

███████╗██╗    ██╗██╗   ██╗ ██████╗██╗  ██╗
╚══███╔╝██║    ██║╚██╗ ██╔╝██╔════╝██║ ██╔╝
  ███╔╝ ██║ █╗ ██║ ╚████╔╝ ██║     █████╔╝ 
 ███╔╝  ██║███╗██║  ╚██╔╝  ██║     ██╔═██╗ 
███████╗╚███╔███╔╝   ██║   ╚██████╗██║  ██╗
╚══════╝ ╚══╝╚══╝    ╚═╝    ╚═════╝╚═╝  ╚═╝
                                           
{Fore.WHITE}v1
{Fore.WHITE}XceeeL
{Fore.RESET}
"""

print(Fore.MAGENTA + banner)
print(Fore.WHITE)

def commands(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        pass

def scan(command: str) -> str:
    cmd = command
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    out = out.decode() 
    return out

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

update_group = parser.add_argument_group('Update')
nuclei_group = parser.add_argument_group('Nuclei Scans')
vuln_group = parser.add_argument_group('Vulnerability')
crawlers_group = parser.add_argument_group('Crawlers')
passiverecon_group = parser.add_argument_group('Passive Recon')
fuzzing_group = parser.add_argument_group('Fuzzing')
portscanning_group = parser.add_argument_group('Port Scanning')

group.add_argument('-sv', '--save', action='store',
                   help="save output to file",
                   metavar="filename.txt")

group.add_argument('-wl', '--wordlist', action='store',
                   help="wordlist to use",
                   metavar="filename.txt")

parser.add_argument('-th', '--threads',
                    type=str, help='default 25',
                    metavar='25')

passiverecon_group.add_argument('-s',
                    type=str, help='scan for subdomains',
                    metavar='domain.com')

passiverecon_group.add_argument('-t', '--tech',
                    type=str, help='find technologies',
                    metavar='domain.com')

passiverecon_group.add_argument('-d', '--dns',
                    type=str, help='scan a list of domains for dns records',
                    metavar='domains.txt')

parser.add_argument('-p', '--probe',
                    type=str, help='probe domains.',
                    metavar='domains.txt')

parser.add_argument('-r', '--redirects',
                    type=str, help='links getting redirected',
                    metavar='domains.txt')

vuln_group.add_argument('-b', '--brokenlinks',
                    type=str, help='search for broken links',
                    metavar='domains.txt')

crawlers_group.add_argument('-pspider', '--paramspider',
                    type=str, help='extract parameters from a domain',
                    metavar='domain.com')

crawlers_group.add_argument('-w', '--waybackurls',
                    type=str, help='scan for waybackurls',
                    metavar='https://domain.com')

crawlers_group.add_argument('-j',
                    type=str, help='find javascript files',
                    metavar='domain.com')

crawlers_group.add_argument('-wc', '--webcrawler',
                    type=str, help='scan for urls and js files',
                    metavar='https://domain.com')

parser.add_argument('-fi', '--favicon',
                    type=str, help='get favicon hashes',
                    metavar='https://domain.com')

parser.add_argument('-fm', '--faviconmulti',
                    type=str, help='get favicon hashes',
                    metavar='https://domain.com')

passiverecon_group.add_argument('-na', '--networkanalyzer',
                    type=str, help='net analyzer',
                    metavar='https://domain.com')

parser.add_argument('-ri', '--reverseip',
                    type=str, help='reverse ip lookup',
                    metavar='IP')

parser.add_argument('-rim', '--reverseipmulti',
                    type=str, help='reverse ip lookup for multiple ips',
                    metavar='IP')

parser.add_argument('-sc', '--statuscode',
                    type=str, help='statuscode',
                    metavar='domain.com')

vuln_group.add_argument('-ph', '--pathhunt',
                    type=str, help='check for directory traversal',
                    metavar='domain.txt')

vuln_group.add_argument('-co', '--corsmisconfig',
                    type=str, help='cors misconfiguration',
                    metavar='domains.txt')

vuln_group.add_argument('-hh', '--hostheaderinjection',
                    type=str, help='host header injection',
                    metavar='domain.com')

parser.add_argument('-sh', '--securityheaders',
                    type=str, help='scan for security headers',
                    metavar='domain.com')

parser.add_argument('-ed', '--enumeratedomain',
                    type=str, help='enumerate domains',
                    metavar='domain.com')

vuln_group.add_argument('-smu', '--smuggler',
                    type=str, help='enumerate domains',
                    metavar='domain.com')

passiverecon_group.add_argument('-ips', '--ipaddresses',
                    type=str, help='get the ips from a list of domains',
                    metavar='domain list')

passiverecon_group.add_argument('-dinfo', '--domaininfo',
                    type=str, help='get domain information like codes,server,content length',
                    metavar='domain list')

parser.add_argument('-isubs', '--importantsubdomains',
                    type=str, help='extract interesting subdomains from a list like dev, admin, test and etc..',
                    metavar='domain list')

fuzzing_group.add_argument('-nft', '--not_found',
                    type=str, help='check for 404 status code',
                    metavar='domains.txt')

portscanning_group.add_argument('-n', '--nmap',
                    type=str, help='Scan a target with nmap',
                    metavar='domain.com or IP')

fuzzing_group.add_argument('-api', '--api_fuzzer',
                    type=str, help='Look for API endpoints',
                    metavar='domain.com')

passiverecon_group.add_argument('-sho', '--shodan',
                    type=str, help='Recon with shodan',
                    metavar='domain.com')

vuln_group.add_argument('-fp', '--forbiddenpass',
                    type=str, help='Bypass 403 forbidden',
                    metavar='domain.com')

fuzzing_group.add_argument('-db', '--directorybrute',
                    type=str, help='Brute force filenames and directories',
                    metavar='domain.com')

portscanning_group.add_argument('-cidr', '--cidr_notation',
                    type=str, help='Scan an ip range to find assets and services',
                    metavar='IP/24')

portscanning_group.add_argument('-ps', '--ports',
                    type=str, help='Port numbers to scan',
                    metavar='80,443,8443')

portscanning_group.add_argument('-pai', '--print_all_ips',
                    type=str, help='Print all ips',
                    metavar='IP/24')

vuln_group.add_argument('-xss', '--xss_scan',
                 type=str, help='scan for XSS vulnerabilities',
                 metavar='https://example.com/page?param=value')

vuln_group.add_argument('-sqli', '--sqli_scan',
                 type=str, help='scan for SQLi vulnerabilities',
                 metavar='https://example.com/page?param=value')

passiverecon_group.add_argument('-shodan', '--shodan_api',
                    type=str, help='shodan api key',
                    metavar='KEY')

parser.add_argument('-webserver', '--webserver_scan',
                    type=str, help='webserver scan',
                    metavar='domain.com')

crawlers_group.add_argument('-javascript', '--javascript_scan',
                    type=str, help='scan for sensitive info in javascript files',
                    metavar='domain.com')

crawlers_group.add_argument('-dp', '--depth',
                    type=str, help='depth of the crawl',
                    metavar='10')

crawlers_group.add_argument('-je', '--javascript_endpoints',
                    type=str, help='extract javascript endpoints',
                    metavar='file.txt')

crawlers_group.add_argument('-hibp', '--haveibeenpwned',
                    type=str, help='check if the password has been pwned',
                    metavar='password')

fuzzing_group.add_argument('-pm', '--param_miner',
                    type=str, help='param miner',
                    metavar='domain.com')

fuzzing_group.add_argument('-ch', '--custom_headers',
                    type=str, help='custom headers',
                    metavar='domain.com')

vuln_group.add_argument('-or', '--openredirect',
                    type=str, help='open redirect',
                    metavar='domain.com')

fuzzing_group.add_argument('-asn', '--automoussystemnumber',
                    type=str, help='asn',
                    metavar='AS55555')

vuln_group.add_argument('-st', '--subdomaintakeover', 
                    type=str, help='subdomain takeover',
                    metavar='subdomains.txt')

fuzzing_group.add_argument('-ar', '--autorecon',
                    type=str, help='auto recon',
                    metavar='domain.com')

vuln_group.add_argument('-jwt', '--jwt_scan',
                     type=str, help='analyze JWT token for vulnerabilities',
                     metavar='token')

vuln_group.add_argument('-jwt-modify', '--jwt_modify',
                     type=str, help='modify JWT token',
                     metavar='token')

vuln_group.add_argument('-heapds', '--heapdump_scan',
                     type=str, help='scan for heapdump endpoints',
                     metavar='domain.com')


parser.add_argument('--s3-scan', help='Scan for exposed S3 buckets')

parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

parser.add_argument("-c", "--concurrency", type=int, default=10, help="Maximum number of concurrent requests")

nuclei_group.add_argument('-nl', '--nuclei_lfi', action='store_true', help="Find Local File Inclusion with nuclei")

passiverecon_group.add_argument('-gs', '--google', action='store_true', help='Google Search')

fuzzing_group.add_argument("-e", "--extensions", help="Comma-separated list of file extensions to scan", default="")

fuzzing_group.add_argument("-x", "--exclude", help="Comma-separated list of status codes to exclude", default="")

update_group.add_argument('-u', '--update', action='store_true', help='Update the script')

parser.add_argument('--shodan-api', help='Shodan API key for subdomain enumeration')

parser.add_argument('--proxy', help='Use a proxy (e.g., http://proxy.com:8080)')

parser.add_argument('--proxy-file', help='Load proxies from file')

parser.add_argument('--heapdump', help='Analyze Java heapdump file')

parser.add_argument('--output-dir', help='Output directory', default='.')




args = parser.parse_args()

user_agent = useragent_list.get_useragent()
header = {"User-Agent": user_agent}

async def update_script():
    try:
        # Store current version
        current_version = "1.0.0"  # Replace with your version tracking system
        backup_dir = "backups"
        
        print(f"{Fore.CYAN}Checking for updates...{Style.RESET_ALL}")
        
        # Create backups directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Create backup of current version
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"spyhunt_backup_{timestamp}")
        
        print(f"{Fore.YELLOW}Creating backup...{Style.RESET_ALL}")
        try:
            shutil.copytree(".", backup_path, ignore=shutil.ignore_patterns(
                '.git*', '__pycache__', 'backups', '*.pyc'
            ))
            print(f"{Fore.GREEN}Backup created at: {backup_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Backup failed: {str(e)}{Style.RESET_ALL}")
            return False

        # Check remote repository for updates
        print(f"{Fore.CYAN}Checking remote repository...{Style.RESET_ALL}")
        try:
            # Fetch without merging
            subprocess.run(["git", "fetch"], check=True, capture_output=True)
            
            # Get current and remote commit hashes
            current = subprocess.run(["git", "rev-parse", "HEAD"], 
                                   check=True, capture_output=True, text=True).stdout.strip()
            remote = subprocess.run(["git", "rev-parse", "@{u}"], 
                                  check=True, capture_output=True, text=True).stdout.strip()
            
            if current == remote:
                print(f"{Fore.GREEN}SpyHunt is already up to date!{Style.RESET_ALL}")
                return True
                
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Failed to check for updates: {str(e)}{Style.RESET_ALL}")
            return False

        # Perform update
        print(f"{Fore.CYAN}Updating SpyHunt...{Style.RESET_ALL}")
        try:
            # Pull changes
            result = subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
            
            if "Already up to date" in result.stdout:
                print(f"{Fore.GREEN}SpyHunt is already up to date!{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Update successful!{Style.RESET_ALL}")
                
                # Check for dependency updates
                requirements_path = "requirements.txt"
                if os.path.exists(requirements_path):
                    print(f"{Fore.CYAN}Updating dependencies...{Style.RESET_ALL}")
                    subprocess.run(["pip", "install", "-r", requirements_path, "--upgrade"], 
                                 check=True)
                    print(f"{Fore.GREEN}Dependencies updated!{Style.RESET_ALL}")
                
                print(f"\n{Fore.GREEN}SpyHunt has been updated successfully!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Please restart SpyHunt to apply the updates.{Style.RESET_ALL}")
            
            return True

        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Update failed: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Restoring from backup...{Style.RESET_ALL}")
            
            # Restore from backup
            try:
                shutil.rmtree(".", ignore_errors=True)
                shutil.copytree(backup_path, ".", dirs_exist_ok=True)
                print(f"{Fore.GREEN}Restore successful!{Style.RESET_ALL}")
            except Exception as restore_error:
                print(f"{Fore.RED}Restore failed: {str(restore_error)}{Style.RESET_ALL}")
                print(f"{Fore.RED}Please restore manually from: {backup_path}{Style.RESET_ALL}")
            
            return False

    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
        return False

# In your argument handler:
if args.update:
    if asyncio.run(update_script()):
        sys.exit(0)
    else:
        sys.exit(1)

if args.s:
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    spotter_path = os.path.join(current_script_dir, 'scripts', 'spotter.sh')
    certsh_path = os.path.join(current_script_dir, 'scripts', 'certsh.sh')
    if args.save:
        print(Fore.CYAN + "Saving output to {}...".format(args.save))
        cmd = f"subfinder -d {args.s} -silent"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        out = out.decode() 
        with open(f"{args.save}", "a") as subfinder:
            subfinder.writelines(out)
        if path.exists(f"{args.save}"):
            print(Fore.GREEN + "DONE!")
        if not path.exists(f"{args.save}"):
            print(Fore.RED + "ERROR!")
            sys.exit(1)

        cmd = f"{spotter_path} {args.s} | uniq | sort"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        spotterout, err = p.communicate()
        spotterout = spotterout.decode()
        with open(f"{args.save}", "a") as spotter:
            spotter.writelines(spotterout)

        cmd = f"{certsh_path} {args.s} | uniq | sort"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        certshout, err = p.communicate()
        certshout = certshout.decode()
        with open(f"{args.save}", "a") as certsh:
            certsh.writelines(certshout)

        # Shodan subdomain extraction
        if args.shodan_api:
            api = shodan.Shodan(args.shodan_api)
            try:
                results = api.search(f'hostname:*.{args.s}')
                shodan_subdomains = set()
                for result in results['matches']:
                    hostnames = result.get('hostnames', [])
                    for hostname in hostnames:
                        if hostname.endswith(args.s) and hostname != args.s:
                            shodan_subdomains.add(hostname)
                with open(f"{args.save}", "a") as shodan_file:
                    for subdomain in sorted(shodan_subdomains):
                        shodan_file.write(f"{subdomain}\n")
                print(Fore.GREEN + f"Added {len(shodan_subdomains)} subdomains from Shodan")
            except shodan.APIError as e:
                print(Fore.RED + f"Error querying Shodan: {e}")
    else:
        commands(f"subfinder -d {args.s}")
        commands(f"assetfinder -subs-only {args.s} | uniq | sort")
        commands(f"{spotter_path} {args.s} | uniq | sort")
        commands(f"{certsh_path} {args.s} | uniq | sort")

        # Shodan subdomain extraction
        if args.shodan_api:
            api = shodan.Shodan(args.shodan_api)
            try:
                results = api.search(f'hostname:*.{args.s}')
                shodan_subdomains = set()
                for result in results['matches']:
                    hostnames = result.get('hostnames', [])
                    for hostname in hostnames:
                        if hostname.endswith(args.s) and hostname != args.s:
                            shodan_subdomains.add(hostname)
                print(Fore.CYAN + "Subdomains found from Shodan:")
                for subdomain in sorted(shodan_subdomains):
                    print(subdomain)
                print(Fore.GREEN + f"Found {len(shodan_subdomains)} subdomains from Shodan")
            except shodan.APIError as e:
                print(Fore.RED + f"Error querying Shodan: {e}")

if args.reverseip:
    domain = socket.gethostbyaddr(args.reverseip)
    print(f"{Fore.CYAN}Domain: {Fore.GREEN} {domain[0]}")

if args.reverseipmulti:
    try:
        with open(f"{args.reverseipmulti}") as f:
            ipadd = [x.strip() for x in f.readlines()]
            for ips in ipadd:
                print(f"{socket.gethostbyaddr(ips)}\n")
    except socket.herror:
        pass
    except FileNotFoundError:
        print(f"{Fore.RED} File not found!")


if args.webcrawler:
    if args.save:
        print(Fore.CYAN + f"Saving output to {args.save}")
        commands(f"echo {args.webcrawler} | hakrawler >> {args.save}")
    else:
        commands(f"echo {args.webcrawler} | hakrawler")


if args.statuscode:
    commands(f"echo '{args.statuscode}' | httpx -silent -status-code")

if args.favicon:
        response = requests.get(f'{args.favicon}/favicon.ico', verify=False)
        favicon = codecs.encode(response.content,"base64")
        hash = mmh3.hash(favicon)
        print(hash)

if args.enumeratedomain:
    try:
        server = []
        r = requests.get(f"{args.enumeratedomain}", verify=False, headers=header) 
        domain = args.enumeratedomain
        if "https://" in domain:
            domain = domain.replace("https://", "")
        if "http://" in domain:
            domain = domain.replace("http://", "")
        ip = socket.gethostbyname(domain)
        for value, key in r.headers.items():
            if value == "Server" or value == "server":
                server.append(key)
        if server:
            print(f"{Fore.WHITE}{args.enumeratedomain}{Fore.MAGENTA}: {Fore.CYAN}[{ip}] {Fore.WHITE}Server:{Fore.GREEN} {server}")
        else:
            print(f"{Fore.WHITE}{args.enumeratedomain}{Fore.MAGENTA}: {Fore.CYAN}[{ip}]")
    except requests.exceptions.MissingSchema as e:
        print(e)
    

if args.faviconmulti:
    print(f"{Fore.MAGENTA}\t\t\t FavIcon Hashes\n")
    with open(f"{args.faviconmulti}") as f:
        domains = [x.strip() for x in f.readlines()]
        try:
            for domainlist in domains:
                response = requests.get(f'{domainlist}/favicon.ico', verify=False, timeout=60, headers=header)
                if response.status_code == 200:
                    favicon = codecs.encode(response.content,"base64")
                    hash = mmh3.hash(favicon)
                    hashes = {}
                response = requests.get(f'{domainlist}/favicon.ico', verify=False, timeout=5, headers=header)
                if response.status_code == 200:
                    favicon = codecs.encode(response.content,"base64")
                    hash = mmh3.hash(favicon)
                    if "https" in domainlist:
                        domainlist = domainlist.replace("https://", "")
                    if "http" in domainlist:
                        domainlist = domainlist.replace("http://", "")
                    ip = socket.gethostbyname(domainlist)
                    if hash == "0":
                        pass
                    for value, item in fingerprint.items():
                        if hash == value:
                            hashes[hash].append(item)
                            print(f"{Fore.WHITE}{domainlist} {Fore.MAGENTA}: {Fore.CYAN}[{hash}] {Fore.GREEN}[{ip}]{Fore.YELLOW} [{item}]")  
                    print(f"{Fore.WHITE}{domainlist} {Fore.MAGENTA}: {Fore.CYAN}[{hash}] {Fore.GREEN}[{ip}]{Fore.YELLOW}")
                    for v,i in hashes.items():
                        print(f"{Fore.MAGENTA}Servers Found")
                        print()
                        print(f"{v}:{i}")
                    else:
                        print(f"{Fore.WHITE}{domainlist} {Fore.MAGENTA}: {Fore.CYAN}{hash} {Fore.GREEN}{ip}")
                else:
                    pass
        except TimeoutError:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except urllib3.exceptions.ProtocolError:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        except KeyError:
            pass

if args.corsmisconfig:
    print(f"\\t\\t\\t{Fore.CYAN}CORS {Fore.MAGENTA}Misconfiguration {Fore.GREEN}Module\\n\\n")

    try:    
        with open(args.corsmisconfig, "r") as f:
            domains = [x.strip() for x in f.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}File {args.corsmisconfig} not found!")
        sys.exit(1)

    def check_cors(domainlist):
        try:
            payload = [domainlist, "evil.com"]
            header = {'Origin': ', '.join(payload)}
            session = requests.Session()
            session.max_redirects = 10
            resp = session.get(domainlist, verify=False, headers=header, timeout=(5, 10))

            allow_origin = resp.headers.get("Access-Control-Allow-Origin", "")
            allowed_methods = resp.headers.get("Access-Control-Allow-Credentials", "")
            if allow_origin == "evil.com" and allowed_methods == "true":
                print(f"{Fore.YELLOW}VULNERABLE: {Fore.GREEN}{domainlist} {Fore.CYAN}PAYLOADS: {Fore.MAGENTA}{', '.join(payload)}")
                return
            print(f"{Fore.CYAN}NOT VULNERABLE: {Fore.GREEN}{domainlist} {Fore.CYAN}PAYLOADS: {Fore.MAGENTA}{', '.join(payload)}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.LIGHTBLACK_EX}Error processing {domainlist}: {e}{Fore.RESET}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_cors, domain) for domain in domains]

    for future in futures:
        try:
            future.result()
        except Exception as e:
            print(f"An error occurred: {e}")


if args.hostheaderinjection:
    def setup_proxies(proxy=None, proxy_file=None):
        """Setup proxy configuration"""
        proxies = []
        if proxy:
            if not proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                proxy = f"http://{proxy}"
            proxies.append({'http': proxy, 'https': proxy})
            
        if proxy_file:
            try:
                with open(proxy_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            proxy = line.strip()
                            if not proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                                proxy = f"http://{proxy}"
                            proxies.append({'http': proxy, 'https': proxy})
            except Exception as e:
                print(f"{Fore.RED}Error loading proxy file: {str(e)}{Style.RESET_ALL}")
        return proxies

    def check_host_header_injection(domainlist):
        session = requests.Session()
        headers = {
            "X-Forwarded-Host": "evil.com",
            "Host": "evil.com",
            "X-Forwarded-For": "evil.com",
            "X-Client-IP": "evil.com",
            "X-Remote-IP": "evil.com",
            "X-Remote-Addr": "evil.com",
            "X-Host": "evil.com"
        }

        # Get proxy list
        proxies = setup_proxies(args.proxy, args.proxy_file)
        current_proxy = None

        try:
            # Select proxy if available
            if proxies:
                current_proxy = random.choice(proxies)

            # Normal request with proxy
            normal_resp = session.get(
                domainlist, 
                verify=False, 
                timeout=5,
                proxies=current_proxy
            )
            normal_content = normal_resp.text

            for header_name, header_value in headers.items():
                try:
                    resp = session.get(
                        domainlist, 
                        verify=False, 
                        headers={header_name: header_value}, 
                        timeout=5,
                        proxies=current_proxy
                    )
                    
                    if resp.status_code in {301, 302, 303, 307, 308}:
                        location = resp.headers.get('Location', '').lower()
                        if location == "evil.com":
                            print(f"{Fore.RED}VULNERABLE: {Fore.GREEN}{domainlist} {Fore.YELLOW}(Redirect to evil.com in Location header)")
                            return
                        
                    if resp.text != normal_content:
                        if 'evil.com' in resp.text.lower():
                            soup = BeautifulSoup(resp.text, 'html.parser')
                            title = soup.title.string
                            if "Evil.Com" in title:
                                print(f"{Fore.RED}VULNERABLE: {Fore.GREEN}{domainlist} {Fore.YELLOW}(evil.com found in response body)")
                                print(f"{Fore.YELLOW}Title: {Fore.GREEN}{title}")
                                return
                            else:
                                pass

                except requests.exceptions.ProxyError:
                    if proxies:
                        current_proxy = random.choice(proxies)
                    continue
                except requests.exceptions.ConnectTimeout:
                    print(f"{Fore.RED}Proxy connection timeout{Style.RESET_ALL}")
                    continue

            print(f"{Fore.CYAN}Not Vulnerable: {Fore.GREEN}{domainlist}")

        except requests.exceptions.RequestException as e:
            if "proxy" in str(e).lower():
                pass
            pass

    def main(args):
        print(f"{Fore.MAGENTA}\t\t Host Header Injection \n")
        print(f"{Fore.WHITE}Checking for {Fore.CYAN}X-Forwarded-Host {Fore.WHITE}and {Fore.CYAN}Host {Fore.WHITE}injections.....\n")

        if args.proxy:
            print(f"{Fore.YELLOW}Using proxy: {args.proxy}{Style.RESET_ALL}")
        elif args.proxy_file:
            print(f"{Fore.YELLOW}Loading proxies from: {args.proxy_file}{Style.RESET_ALL}")

        with open(args.hostheaderinjection, "r") as f:
            domains = [x.strip() for x in f.readlines()]

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(check_host_header_injection, domains)

    if __name__ == "__main__":
        if args.hostheaderinjection:
            main(args)


if args.securityheaders:
    print(f"{Fore.MAGENTA}\t\t Security Headers\n")
    security_headers = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "X-XSS-Protection"]
    session = requests.Session()
    no_sec = []
    found_hd = []
    no_dup = []
    no_dup_found = []
    lower = [x.lower() for x in security_headers]
    capital = [x.upper() for x in security_headers]
    resp = session.get(f"{args.securityheaders}", verify=False)
    print(f"{Fore.CYAN}Domain: {Fore.GREEN}{args.securityheaders}\n")
    for item, key in resp.headers.items():
        for sec_headers in security_headers:
            if sec_headers  == item or lower == item or capital == item:
                found_hd.append(sec_headers)
                [no_dup_found.append(x) for x in found_hd if x not in no_dup_found]
        print(f"{Fore.CYAN}{item}: {Fore.YELLOW}{key}")
    no_dup = ", ".join(no_dup)
    print(lower)
    print("\n")
    print(f"{Fore.GREEN} Found Security Headers: {Fore.YELLOW} {len(no_dup_found)}\n")
    no_dup_found = ", ".join(no_dup_found)
    print(f"{Fore.YELLOW} {no_dup_found}\n")
    no_headers = [item for item in security_headers if item not in no_dup_found]
    print(f"{Fore.RED} Found Missing headers: {Fore.YELLOW} {len(no_headers)}\n")
    no_headers = ", ".join(no_headers)
    print(f"{Fore.YELLOW} {no_headers}")


if args.networkanalyzer:
    print(f"{Fore.MAGENTA}\t\t Analyzing Network Vulnerabilities \n")
    print(f"{Fore.CYAN}IP Range: {Fore.GREEN}{args.networkanalyzer}\n")
    print(f"{Fore.WHITE}")
    commands(f"shodan stats --facets port net:{args.networkanalyzer}")
    commands(f"shodan stats --facets vuln net:{args.networkanalyzer}")


if args.waybackurls:
    if args.save:
        print(Fore.CYAN + f"Saving output to {args.save}")
        commands(f"waybackurls {args.waybackurls} | anew >> {args.save}")
        print(Fore.GREEN + "DONE!")
    else:
        commands(f"waybackurls {args.waybackurls}")

if args.j:
    init(autoreset=True)

    async def fetch(session, url):
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 404:
                    # Silently ignore 404 errors
                    return None
                else:
                    print(f"{Fore.YELLOW}Warning: {url} returned status code {response.status}{Style.RESET_ALL}")
                    return None
        except aiohttp.ClientError as e:
            print(f"{Fore.RED}Error fetching {url}: {e}{Style.RESET_ALL}")
        except asyncio.TimeoutError:
            print(f"{Fore.RED}Timeout error fetching {url}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Unexpected error fetching {url}: {e}{Style.RESET_ALL}")
        return None

    def is_valid_url(url):
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        except Exception as e:
            print(f"{Fore.RED}Error parsing URL {url}: {e}{Style.RESET_ALL}")
            return False

    def is_same_domain(url, domain):
        try:
            return urlparse(url).netloc == domain
        except Exception as e:
            print(f"{Fore.RED}Error comparing domains for {url}: {e}{Style.RESET_ALL}")
            return False

    async def get_js_links(session, url, domain):
        js_links = set()
        new_links = set()
        html = await fetch(session, url)
        if html:
            try:
                soup = BeautifulSoup(html, 'html.parser')
                
                for script in soup.find_all('script', src=True):
                    script_url = urljoin(url, script['src'])
                    if is_valid_url(script_url) and is_same_domain(script_url, domain):
                        js_links.add(script_url)
                
                for script in soup.find_all('script'):
                    if script.string:
                        js_urls = re.findall(r'[\'"]([^\'"]*\.js)[\'"]', script.string)
                        for js_url in js_urls:
                            full_js_url = urljoin(url, js_url)
                            if is_valid_url(full_js_url) and is_same_domain(full_js_url, domain):
                                js_links.add(full_js_url)
                
                new_links = set(urljoin(url, link['href']) for link in soup.find_all('a', href=True))
            except Exception as e:
                print(f"{Fore.RED}Error parsing HTML from {url}: {e}{Style.RESET_ALL}")
        
        return js_links, new_links

    async def crawl_website(url, max_depth, concurrency):
        try:
            domain = urlparse(url).netloc
            visited = set()
            to_visit = {url}
            js_files = set()
            semaphore = asyncio.Semaphore(concurrency)

            async def bounded_get_js_links(session, url, domain):
                async with semaphore:
                    return await get_js_links(session, url, domain)

            async with aiohttp.ClientSession() as session:
                for depth in range(int(max_depth) + 1):
                    if not to_visit:
                        break

                    tasks = [bounded_get_js_links(session, url, domain) for url in to_visit]
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    visited.update(to_visit)
                    to_visit = set()

                    for result in results:
                        if isinstance(result, Exception):
                            print(f"{Fore.RED}Error during crawl: {result}{Style.RESET_ALL}")
                            continue
                        js_links, new_links = result
                        js_files.update(js_links)
                        to_visit.update(link for link in new_links 
                                        if is_valid_url(link) and is_same_domain(link, domain) and link not in visited)

                    print(f"{Fore.CYAN}Depth {depth}: Found {len(js_files)} JS files, {len(to_visit)} new URLs to visit{Style.RESET_ALL}")

            return js_files
        except Exception as e:
            print(f"{Fore.RED}Unexpected error during crawl: {e}{Style.RESET_ALL}")
            return set()

    async def main():
        try:
            print(f"{Fore.CYAN}Crawling {Fore.GREEN}{args.j}{Fore.CYAN} for JavaScript files...{Style.RESET_ALL}\n")
            js_files = await crawl_website(args.j, args.depth, args.concurrency)

            if js_files:
                print(f"\n{Fore.YELLOW}Found {len(js_files)} JavaScript files:{Style.RESET_ALL}")
                for js_file in sorted(js_files):
                    print(js_file)

                if args.save:
                    try:
                        with open(args.save, 'w') as f:
                            for js_file in sorted(js_files):
                                f.write(f"{js_file}\n")
                        print(f"\n{Fore.GREEN}Results saved to {args.save}{Style.RESET_ALL}")
                    except IOError as e:
                        print(f"{Fore.RED}Error saving results to file: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No JavaScript files found.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Unexpected error in main function: {e}{Style.RESET_ALL}")

    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Crawl interrupted by user.{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
            sys.exit(1)

if args.dns:
    if args.save:
        print(Fore.CYAN + "Saving output to {}...".format(args.save))
        commands(f"cat {args.dns} | dnsx -silent -a -resp >> {args.save}")
        commands(f"cat {args.dns} | dnsx -silent -ns -resp >> {args.save}")
        commands(f"cat {args.dns} | dnsx -silent -cname -resp >> {args.save}")
    else:
        print(Fore.CYAN + "Printing A records...\n")
        time.sleep(2)
        commands(f"cat {args.dns} | dnsx -silent -a -resp\n")
        print(Fore.CYAN + "Printing NS Records...\n")
        time.sleep(2)
        commands(f"cat {args.dns} | dnsx -silent -ns -resp\n")
        print(Fore.CYAN + "Printing CNAME records...\n")
        time.sleep(2)
        commands(f"cat {args.dns} | dnsx -silent -cname -resp\n")            

if args.probe:
    if args.save:
        print(Fore.CYAN + "Saving output to {}...".format(args.save))
        commands(f'cat {args.probe} | httprobe -c 100 | anew >> {args.save}')
        if path.exists(f"{args.save}"):
            print(Fore.GREEN + "DONE!")
        if not path.exists(f"{args.save}"):
            print(Fore.RED + "ERROR!")
    else:
        commands(f'sudo cat {args.probe} | httprobe | anew')    


if args.redirects:
    if args.save:
        print(Fore.CYAN + "Saving output to {}}..".format(args.save))
        if which("httpx"):
            print("Please uninstall httpx and install httpx-toolkit from https://github.com/projectdiscovery/httpx-toolkit")
            sys.exit()
        commands(f"cat {args.redirects} | httpx -silent -location -mc 301,302 | anew >> redirects.txt")
        if path.exists(f"{args.save}"):
            print(Fore.GREEN + "DONE!")
        if not path.exists(f"{args.save}"):
            print(Fore.RED + "ERROR!")
    else:
        commands(f"cat {args.redirects} | httpx -silent -location -mc 301,302")   


if args.brokenlinks:
    if args.save:
        print(Fore.CYAN + "Saving output to {}".format(args.save))
        commands(f"blc -r --filter-level 2 {args.brokenlinks}")
        if path.exists(f"{args.save}"):
            print(Fore.CYAN + "DONE!")
        if not path.exists(f"{args.save}"):
            print(Fore.CYAN + "ERROR!")
    else:
        commands(f"blc -r --filter-level 2 {args.brokenlinks}")

if args.tech:
    try:
        print("\n")
        print (Fore.CYAN + "Scanning..." + "\n")
        info = builtwith(f"{args.tech}")
        for framework, tech in info.items():
            print (Fore.GREEN + framework, ":", tech)
    except UnicodeDecodeError:
        pass

if args.smuggler:
    smug_path = os.path.abspath(os.getcwd())
    commands(f"python3 {smug_path}/tools/smuggler/smuggler.py -u {args.smuggler} -q")

if args.ipaddresses:
    ip_list = []

    with open(f"{args.ipaddresses}", "r") as f:
        domains = [x.strip() for x in f.readlines()]

    def scan(domain: str):
        try:
            ips = socket.gethostbyname(domain)
            ip_list.append(ips)
            print(f"{Fore.GREEN} {domain} {Fore.WHITE}- {Fore.CYAN}{ips}")
        except socket.gaierror:
            pass
        except UnicodeError:
            pass

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan, domain) for domain in domains]
        
        for future in futures:
            future.result()
    
    with open("ips.txt", "w") as file:
        ip_list = list(dict.fromkeys(ip_list))
        for iplist in ip_list:
            file.write(f"{iplist}\n")


if args.domaininfo:
    with open(f"{args.domaininfo}", "r") as f:
        domains = [x.strip() for x in f.readlines()]
    ip_list = []
    server = []
    new_server = set()
    for domain_list in domains:
        try:
            sessions = requests.Session()
            r = sessions.get(domain_list, verify=False, headers=header)
            if "https://" in domain_list:
                domain_list = domain_list.replace("https://", "")
            if "http://" in domain_list:
                domain_list = domain_list.replace("https://", "")
            for v, k in r.headers.items():
                if "Server" in v:
                    server.append(k)
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.find("title")
            ips = socket.gethostbyname(domain_list)
            ip_check = os.system(f"ping -c1 -W1 {ips} > /dev/null")
            if ip_check == 0:
                ip_list.append(ips)
            else:
                pass
            with open(f"ips.txt", "w") as f:
                for ipaddresses in ip_list:
                    f.writelines(f"{ipaddresses}\n")
            new_server.update(server)
            if r.status_code == 200:
                print(f"{Fore.GREEN} {domain_list} {Fore.WHITE}- {Fore.YELLOW}[{ips}]{Fore.BLUE}[{title.get_text()}]{Fore.GREEN}[{r.status_code}]{Fore.LIGHTMAGENTA_EX}[{', '.join(map(str,new_server))}]")
            if r.status_code == 403:
                print(f"{Fore.GREEN} {domain_list} {Fore.WHITE}- {Fore.YELLOW}[{ips}]{Fore.BLUE}[{title.get_text()}]{Fore.RED}[{r.status_code}]{Fore.LIGHTMAGENTA_EX}[{', '.join(map(str,new_server))}]")
            else:
                print(f"{Fore.GREEN} {domain_list} {Fore.WHITE}- {Fore.YELLOW}[{ips}]{Fore.BLUE}[{title.get_text()}]{Fore.CYAN}[{r.status_code}]{Fore.LIGHTMAGENTA_EX}[{', '.join(map(str,new_server))}]")
        except socket.gaierror:
            pass
        except requests.exceptions.MissingSchema:
            print(f"{Fore.RED} Please use http:// or https://")
        except requests.exceptions.SSLError:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except AttributeError:
            print(f"{Fore.GREEN} {domain_list} {Fore.WHITE}- {Fore.YELLOW}[{ips}]{Fore.BLUE}[No title]{Fore.CYAN}[{r.status_code}]{Fore.LIGHTMAGENTA_EX}[{', '.join(map(str,new_server))}]")
        except UnicodeDecodeError:
            pass
        except requests.exceptions.InvalidURL:
            pass
        except KeyboardInterrupt:
            sys.exit()
        except:
            pass

if args.importantsubdomains:
    with open(f"{args.importantsubdomains}", "r") as f:
        important_subs = []
        subdomains = [x.strip() for x in f.readlines()]
        for subdomain_list in subdomains:
            if "admin" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "dev" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "test" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "api" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "staging" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "prod" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "beta" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "manage" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "jira" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
            if "github" in subdomain_list:
                important_subs.append(f"{subdomain_list}")
        for pos, value in enumerate(important_subs):
            print(f"{Fore.CYAN}{pos}: {Fore.GREEN}{value}")
        with open("juice_subs.txt", "w") as f:
            for goodsubs in important_subs:
                f.writelines(f"{goodsubs}\n")


if args.not_found:
    session = requests.Session()
    session.headers.update(header)

    def check_status(domain):
        try:
            r = session.get(domain, verify=False, headers=header, timeout=10)
            if r.status_code == 404:
                return domain
        except requests.exceptions.RequestException:
            pass

    def get_results(links, output_file):
        pool = ThreadPool(processes=multiprocessing.cpu_count())
        results = pool.imap_unordered(check_status, links)
        with open(output_file, "w") as f:
            for result in results:
                if result:
                    f.write(f"{result}\n")
                    print(result)
        pool.close()
        pool.join()

    with open(args.not_found, "r") as f:
        links = (f"{x.strip()}" for x in f.readlines())
        output_file = "results.txt"
        get_results(links, output_file)

if args.paramspider:
    commands(f"paramspider -d {args.paramspider}")

if args.pathhunt:
    def commands(cmd):
        try:
            subprocess.check_call(cmd, shell=True)
        except:
            pass
    pathhunt_path = os.path.abspath(os.getcwd())
    commands(f"python3 {pathhunt_path}/tools/pathhunt.py -t {args.pathhunt}")   
    
if args.nmap:
    print(f"{Fore.WHITE}Scanning {Fore.CYAN}{args.nmap}\n")
    nmap = nmap3.Nmap()
    results = nmap.nmap_version_detection(f"{args.nmap}")

    with open("nmap_results.json", "w") as f:
        json.dump(results, f, indent=4)

    with open('nmap_results.json', 'r') as file:
        data = json.load(file)

    for host, host_data in data.items():
        if host != "runtime" and host != "stats" and host != "task_results":
            ports = host_data.get("ports", [])
            for port in ports:
                portid = port.get("portid")
                service = port.get("service", {})
                product = service.get("product")
                print(f"{Fore.WHITE}Port: {Fore.CYAN}{portid}, {Fore.WHITE}Product: {Fore.CYAN}{product}")

if args.api_fuzzer:
    error_patterns = [
        "404",
        "Page Not Found",
        "Not Found",
        "Error 404",
        "404 Not Found",
        "The page you requested was not found",
        "The requested URL was not found",
        "This page does not exist",
        "The requested page could not be found",
        "Sorry, we couldn't find that page",
        "Page doesn't exist"
    ]
    s = requests.Session()
    with open("payloads/api-endpoints.txt", "r") as file:
        api_endpoints = [x.strip() for x in file.readlines()]
    
    def check_endpoint(endpoint):
        url = f"{args.api_fuzzer}/{endpoint}"
        try:
            r = s.get(url, verify=False, headers=header, timeout=5)

            # Check response text for error patterns
            page_text = r.text.lower()
            found_patterns = []
            for pattern in error_patterns:
                if pattern.lower() in page_text:
                    found_patterns.append(pattern)
            if found_patterns:
                return f"{Fore.RED}{url} - {', '.join(found_patterns)}"

            # Check beautifulsoup for error patterns
            soup = BeautifulSoup(r.text, "html.parser")
            if soup.find("title") and "404" in soup.find("title").text.lower():
                pass
            elif soup.find("title") and "Page Not Found" in soup.find("title").text.lower():
                pass
            elif r.status_code == 403:
                pass
            elif r.status_code == 200:
                return f"{Fore.GREEN}{url}"
            elif r.status_code == 404:
                pass
            else:
                return f"{Fore.RED}{url} [{r.status_code}]"
        except requests.RequestException:
            return f"{Fore.YELLOW}{url} [Error]"
    
    print(f"Scanning {len(api_endpoints)} endpoints for {args.api_fuzzer}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_endpoint, endpoint) for endpoint in api_endpoints]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                if result.startswith(Fore.GREEN):
                    print(result)
            else:
                pass
            

if args.shodan:
    key = input("Shodan Key: ")
    print("\n")
    api = shodan.Shodan(str(key))
    try:
        results = api.search(args.shodan)
        results_ = []
        results_5 = []
        for result in results['matches']:
            results_.append(result['ip_str'])
        results_5.append(results_[0:50])
        if results_5:
            print(f"{Fore.MAGENTA}[+] {Fore.CYAN}-{Fore.WHITE} Shodan IPs: {Fore.GREEN}{', '.join(map(str,results_5))}")
        if not results_5:
            pass
    except shodan.APIError:
        print(f"{Fore.MAGENTA}[+] {Fore.CYAN}-{Fore.YELLOW} Shodan Key: {Fore.GREEN} Invalid Key")
    except socket.herror:
        pass


if args.forbiddenpass:
    def word_list(wordlist: str) -> str:
        try:
            with open(wordlist, "r") as f:
                data = [x.strip() for x in f.readlines()] 
            return data
        except FileNotFoundError as e:
            print(f"File not found: {e}")

    wordlist = word_list("payloads/bypasses.txt")

    def header_bypass():
        headers = [
            {'User-Agent': user_agent},
            {'User-Agent': str(user_agent), 'X-Custom-IP-Authorization': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Forwarded-For': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Forwarded-For': '127.0.0.1:80'},
            {'User-Agent': str(user_agent), 'X-Originally-Forwarded-For': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Originating-': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Originating-IP': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'True-Client-IP': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-WAP-Profile': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Arbitrary': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-HTTP-DestinationURL': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Forwarded-Proto': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'Destination': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Remote-IP': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Client-IP': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Host': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Forwarded-Host': 'http://127.0.0.1'},
            {'User-Agent': str(user_agent), 'X-Forwarded-Port': '4443'},
            {'User-Agent': str(user_agent), 'X-Forwarded-Port': '80'},
            {'User-Agent': str(user_agent), 'X-Forwarded-Port': '8080'},
            {'User-Agent': str(user_agent), 'X-Forwarded-Port': '8443'},
            {'User-Agent': str(user_agent), 'X-ProxyUser-Ip': '127.0.0.1'},
            {'User-Agent': str(user_agent), 'Client-IP': '127.0.0.1'}

        ]
        return headers
    
    def do_request(url: str, stream=False):
        headers = header_bypass()
        try:
            for header in headers:
                if stream:
                    s = requests.Session()
                    r = s.get(url, stream=True, headers=header)
                else:
                    s = requests.Session()
                    r = s.get(url, headers=header)
                if r.status_code == 200:
                    print(Fore.WHITE + url + ' ' + json.dumps(list(header.items())[-1]) + Fore.GREEN + " [{}]".format(r.status_code))
                else:
                    print(Fore.WHITE + url + ' ' + json.dumps(list(header.items())[-1]) + Fore.RED + " [{}]".format(r.status_code))
        except requests.exceptions.ConnectionError as ce_error:
            pass
        except requests.exceptions.Timeout as t_error:
            print("Connection Timeout Error: ", t_error)
            pass
        except requests.exceptions.RequestException as req_err:
            print("Some Ambiguous Exception:", req_err)
            pass

    def main(wordlist):
        for bypass in wordlist:
            links = f"{args.forbiddenpass}{bypass}"
            do_request(links)

    if __name__ == "__main__":
        main(wordlist)

if args.directorybrute:
    if args.wordlist:
        if args.threads:
            def filter_wordlist(wordlist, extensions):
                if not extensions:
                    return wordlist
                ext_list = [ext.strip() for ext in extensions.split(',')]
                return [word for word in wordlist if any(word.endswith(ext) for ext in ext_list)]

            def dorequests(wordlist: str, base_url: str, headers: dict, is_file_only: bool, excluded_codes: set, bar, print_lock):
                s = requests.Session()
                
                def check_and_print(url, type_str):
                    try:
                        r = s.get(url, verify=False, headers=headers, timeout=10)
                        if r.status_code not in excluded_codes:
                            if r.status_code == 200 and "Welcome" in r.text:
                                color = Fore.GREEN
                            elif r.status_code == 301 or r.status_code == 302:
                                color = Fore.YELLOW
                            else:
                                color = Fore.BLUE
                            with print_lock:
                                print(f"\n{url} - {color}{type_str} Found (Status: {r.status_code}){Fore.RESET}\n")
                    except requests.RequestException:
                        pass
                    finally:
                        bar()

                if is_file_only:
                    url = f"{base_url}/{wordlist}"
                    check_and_print(url, "File")
                else:
                    dir_url = f"{base_url}/{wordlist}/"
                    check_and_print(dir_url, "Directory")
                    
            def main():
                with open(args.wordlist, "r") as f:
                    wordlist_ = [x.strip() for x in f.readlines()]
                
                is_file_only = bool(args.extensions)
                
                filtered_wordlist = filter_wordlist(wordlist_, args.extensions)
                
                excluded_codes = set(int(code.strip()) for code in args.exclude.split(',') if code.strip())
                
                print(f"Target: {Fore.CYAN}{args.directorybrute}{Fore.RESET}\n"
                    f"Wordlist: {Fore.CYAN}{args.wordlist}{Fore.RESET}\n"
                    f"Extensions: {Fore.CYAN}{args.extensions or 'All'}{Fore.RESET}\n"
                    f"Excluded Status Codes: {Fore.CYAN}{', '.join(map(str, excluded_codes)) or 'None'}{Fore.RESET}\n")

                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                print_lock = threading.Lock()

                with alive_bar(len(filtered_wordlist), title="Scanning", bar="classic", spinner="classic") as bar:
                    with ThreadPoolExecutor(max_workers=int(args.threads)) as executor:
                        futures = [executor.submit(dorequests, wordlist, args.directorybrute, headers, is_file_only, excluded_codes, bar, print_lock) 
                                for wordlist in filtered_wordlist]
                        
                        for future in as_completed(futures):
                            future.result()

            if __name__ == "__main__":
                main()

if args.nuclei_lfi:
    vulnerability = []
    FileOrTarget = str(input("Do you want to scan a file or a single target?? Ex: F or T:  "))
    if FileOrTarget == "F" or FileOrTarget == "f":
        File = str(input("Filename: "))
        print(f"Scanning File {File} ..... \n")
        results = scan(f"nuclei -l {File} -tags lfi -c 100")
        vulnerability.append(results)
        if vulnerability:
            for vulns in vulnerability:
                print(vulns)
    elif FileOrTarget == "T" or FileOrTarget == "t":
        Target = str(input("Target: "))
        print(f"Scanning Target {Target} ..... \n")
        results = scan(f"nuclei -u {Target} -tags lfi -c 100")
        vulnerability.append(results)
        if vulnerability:
            for vulns in vulnerability:
                print(vulns)
    else:
        print("Enter either T or F")


if args.google:
    def search_google(dorks: str, page) -> str:
        for url in search(dork, num_results=int(page)):
            return url
    try: 
        dork = input("Enter Dork: ")
        numpage = input("Enter number of links to display: ")
        print ("\n")
        search_google(dork, numpage)
        print("\n")
        print ("Found: {} links".format(numpage))
    except Exception as e:
        print(str(e))

    save = input("Save results to a file (y/n)?: ").lower()
    if save == "y":
        dorklist = input("Filename: ")
        with open(dorklist, "w") as f:
            for url in search(dork, num_results=int(numpage)):
                f.writelines(url)
                f.writelines("\n")
        if path.exists(dorklist):
            print ("File saved successfully")
        if not path.exists(dorklist):
            print ("File was not saved")
    elif save == "n":
        pass        
            
if args.cidr_notation:
    if args.ports:
        if args.threads:
            def scan_ip(ip, ports):
                open_ports = []
                for port in ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((str(ip), port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                return ip, open_ports

            def scan_subnet(subnet, ports, max_threads=100):
                network = ipaddress.ip_network(subnet, strict=False)
                
                with ThreadPoolExecutor(max_workers=int(args.threads)) as executor:
                    futures = [executor.submit(scan_ip, ip, ports) for ip in network.hosts()]
                    
                    for future in as_completed(futures):
                        ip, open_ports = future.result()
                        if open_ports:
                            print(f"IP: {Fore.GREEN}{ip}:{Fore.CYAN}{','.join(map(str, open_ports))}{Fore.RESET}")

            def parse_ports(ports):
                if isinstance(ports, list):
                    return [int(p) for p in ports]
                return [int(p.strip()) for p in ports.split(',')]
            
            def main():
                ports = parse_ports(args.ports)
                scan_subnet(args.cidr_notation, ports, args.threads)

            if __name__ == "__main__":
                main()
    
if args.print_all_ips:
    def extract_ip(ip):
        return str(ip)

    def extract_ips(subnet, max_workers=100):
        network = ipaddress.ip_network(subnet, strict=False)
        ips = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(extract_ip, ip) for ip in network.hosts()]
            for future in as_completed(futures):
                ips.append(future.result())
        return ips

    print(f"Extracting IPs from {args.print_all_ips}...")
    ips = extract_ips(args.print_all_ips)
    
    print(f"\nExtracted IPs from {args.print_all_ips}:")
    for ip in ips:
        print(f"{Fore.GREEN}{ip}{Fore.RESET}")
    
    print(f"\nTotal IPs: {len(ips)}")

    save = input("Do you want to save these IPs to a file? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename to save IPs: ")
        with open(filename, 'w') as f:
            for ip in ips:
                f.write(f"{ip}\n")
        print(f"IPs saved to {filename}")


if args.xss_scan:
    # Define rate limit: 5 calls per second
    CALLS = 5
    RATE_LIMIT = 1

    @sleep_and_retry
    @limits(calls=CALLS, period=RATE_LIMIT)
    def rate_limited_request(url, headers, timeout):
        return requests.get(url, verify=False, headers=headers, timeout=timeout)

    def generate_random_string(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def encode_payload(payload):
        encodings = [
            lambda x: x,  # No encoding
            lambda x: quote_plus(x),  # URL encoding
            lambda x: html.escape(x),  # HTML entity encoding
            lambda x: ''.join(f'%{ord(c):02X}' for c in x),  # Full URL encoding
            lambda x: ''.join(f'&#x{ord(c):02X};' for c in x),  # Hex entity encoding
            lambda x: ''.join(f'\\u{ord(c):04X}' for c in x),  # Unicode escape
        ]
        return random.choice(encodings)(payload)

    def print_vulnerability(vuln):
        if vuln['execution_likelihood'] == 'High':
            print(f"\n{Fore.RED}High likelihood XSS vulnerability found:{Fore.RESET}")
            print(f"URL: {Fore.CYAN}{vuln['url']}{Fore.RESET}")
            print(f"Parameter: {Fore.YELLOW}{vuln['parameter']}{Fore.RESET}")
            print(f"Payload: {Fore.MAGENTA}{vuln['payload']}{Fore.RESET}")
            print(f"Test URL: {Fore.BLUE}{vuln['test_url']}{Fore.RESET}")

    def xss_scan_url(url, payloads, bar):
        print(f"{Fore.CYAN}Scanning for XSS vulnerabilities: {Fore.GREEN}{url}{Fore.RESET}")
        
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        vulnerabilities = []
        
        for param in params:
            for payload in payloads:
                random_string = generate_random_string()
                test_payload = payload.replace("XSS", random_string)
                encoded_payload = encode_payload(test_payload)
                
                test_params = params.copy()
                test_params[param] = [encoded_payload]
                test_url = parsed_url._replace(query=urlencode(test_params, doseq=True)).geturl()
                
                try:
                    response = rate_limited_request(test_url, headers=header, timeout=10)
                    response_text = response.text.lower()
                    
                    if random_string.lower() in response_text:
                        vulnerability = {
                            "url": url,
                            "parameter": param,
                            "payload": encoded_payload,
                            "test_url": test_url
                        }
                        pattern_script = r'<script>.*?alert\([\'"]{}[\'"]\).*?</script>'.format(re.escape(random_string))
                        pattern_event = r'on\w+\s*=.*?alert\([\'"]{}[\'"]\)'.format(re.escape(random_string))
                        if re.search(pattern_script, response_text, re.IGNORECASE | re.DOTALL) or \
                           re.search(pattern_event, response_text, re.IGNORECASE):
                            vulnerability["execution_likelihood"] = "High"
                            vulnerabilities.append(vulnerability)
                            print_vulnerability(vulnerability)
                except requests.RequestException as e:
                    print(f"{Fore.YELLOW}Error scanning {test_url}: {str(e)}{Fore.RESET}")
                finally:
                    bar()  # Increment the progress bar for each payload scanned
        
        return vulnerabilities

    def xss_scanner(target):
        if os.path.isfile(target):
            with open(target, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
            
            with open("payloads/xss.txt", "r") as f:
                payloads = [x.strip() for x in f.readlines()]
            
            total_payloads = 0
            # Calculate total payloads based on number of URLs and number of payloads per URL
            for url in urls:
                parsed_url = urlparse(url)
                params = parse_qs(parsed_url.query)
                total_payloads += len(params) * len(payloads)
            
            all_vulnerabilities = []
            with alive_bar(total_payloads, title="Scanning XSS Vulnerabilities") as bar:
                with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                    future_to_url = {executor.submit(xss_scan_url, url, payloads, bar): url for url in urls}
                    for future in as_completed(future_to_url):
                        url = future_to_url[future]
                        try:
                            vulnerabilities = future.result()
                            all_vulnerabilities.extend(vulnerabilities)
                        except Exception as exc:
                            print(f'{Fore.RED}Error scanning {url}: {exc}{Fore.RESET}')
            
            return all_vulnerabilities
        else:
            target_url = target
            with open("payloads/xss.txt", "r") as f:
                payloads = [x.strip() for x in f.readlines()]
            
            params = parse_qs(urlparse(target_url).query)
            total_payloads = len(params) * len(payloads)
            
            all_vulnerabilities = []
            with alive_bar(total_payloads, title="Scanning XSS Vulnerabilities") as bar:
                vulnerabilities = xss_scan_url(target_url, payloads, bar)
                all_vulnerabilities.extend(vulnerabilities)
            
            return all_vulnerabilities

    if __name__ == "__main__":
        vulnerabilities = xss_scanner(args.xss_scan)
        if not vulnerabilities:
            print(f"\n{Fore.GREEN}No XSS vulnerabilities found.{Fore.RESET}")
        else:
            print(f"\n{Fore.RED}Total XSS vulnerabilities found: {len(vulnerabilities)}{Fore.RESET}")


if args.sqli_scan:
    init(autoreset=True)

    # Rate Limiting Configuration
    RATE_LIMIT = 5  # Maximum number of requests per second
    REQUEST_INTERVAL = 1 / RATE_LIMIT  # Interval between requests in seconds

    def generate_random_string(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def encode_payload(payload):
        encodings = [
            lambda x: x,  # No encoding
            lambda x: quote_plus(x),  # URL encoding
            lambda x: ''.join(f'%{ord(c):02X}' for c in x),  # Full URL encoding
        ]
        return random.choice(encodings)(payload)

    def print_vulnerability(vuln):
        print(f"\n{Fore.RED}SQL Injection vulnerability found:{Fore.RESET}")
        print(f"URL: {Fore.CYAN}{vuln['url']}{Fore.RESET}")
        print(f"Parameter: {Fore.YELLOW}{vuln['parameter']}{Fore.RESET}")
        print(f"Payload: {Fore.MAGENTA}{vuln['payload']}{Fore.RESET}")
        print(f"Test URL: {Fore.BLUE}{vuln['test_url']}{Fore.RESET}")
        print(f"Type: {Fore.GREEN}{vuln['type']}{Fore.RESET}")

    def sqli_scan_url(url, print_queue, bar, rate_limiter):
        print_queue.put(f"{Fore.CYAN}Scanning for SQL injection vulnerabilities: {url}{Fore.RESET}")
        
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        for param in params:
            # Error-based SQLi
            error_payloads = [
                "' OR '1'='1",
                "' OR '1'='1' --",
                "' UNION SELECT NULL, NULL, NULL --",
                "1' ORDER BY 1--+",
                "1' ORDER BY 2--+",
                "1' ORDER BY 3--+",
                "1 UNION SELECT NULL, NULL, NULL --",
            ]
            
            for payload in error_payloads:
                rate_limiter.acquire()
                encoded_payload = encode_payload(payload)
                test_params = params.copy()
                test_params[param] = [encoded_payload]
                test_url = parsed_url._replace(query=urlencode(test_params, doseq=True)).geturl()
                
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/58.0.3029.110 Safari/537.3'
                    }
                    response = requests.get(test_url, verify=False, headers=headers, timeout=10)
                    
                    sql_errors = [
                        r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result",
                        r"MySqlClient\.", r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*",
                        r"valid PostgreSQL result", r"Npgsql\.", r"Driver.*SQL SERVER",
                        r"OLE DB.*SQL SERVER", r"SQL Server.*Driver", r"Warning.*mssql_.*",
                        r"Microsoft SQL Native Client error '[0-9a-fA-F]{8}",
                        r"ODBC SQL Server Driver", r"SQLServer JDBC Driver", r"Oracle error",
                        r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*"
                    ]
                    
                    for error in sql_errors:
                        if re.search(error, response.text, re.IGNORECASE):
                            vulnerability = {
                                "url": url,
                                "parameter": param,
                                "payload": encoded_payload,
                                "test_url": test_url,
                                "type": "Error-based SQLi"
                            }
                            print_queue.put(vulnerability)
                            bar()  # Increment progress bar upon finding a vulnerability
                            return  # Exit after finding a vulnerability
                    
                except requests.RequestException as e:
                    print_queue.put(f"{Fore.YELLOW}Error scanning {test_url}: {str(e)}{Fore.RESET}")
                finally:
                    bar()  # Increment the progress bar for each payload scanned
            
            # Boolean-based blind SQLi
            rate_limiter.acquire()
            original_params = params.copy()
            original_params[param] = ["1 AND 1=1"]
            true_url = parsed_url._replace(query=urlencode(original_params, doseq=True)).geturl()
            
            original_params[param] = ["1 AND 1=2"]
            false_url = parsed_url._replace(query=urlencode(original_params, doseq=True)).geturl()
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/58.0.3029.110 Safari/537.3'
                }
                true_response = requests.get(true_url, verify=False, headers=headers, timeout=10)
                false_response = requests.get(false_url, verify=False, headers=headers, timeout=10)
                
                if true_response.text != false_response.text:
                    vulnerability = {
                        "url": url,
                        "parameter": param,
                        "payload": "1 AND 1=1 / 1 AND 1=2",
                        "test_url": f"{true_url} / {false_url}",
                        "type": "Boolean-based blind SQLi"
                    }
                    print_queue.put(vulnerability)
                    bar()  # Increment progress bar upon finding a vulnerability
            except requests.RequestException as e:
                print_queue.put(f"{Fore.YELLOW}Error during boolean-based test for {url}: {str(e)}{Fore.RESET}")
            finally:
                bar()  # Increment the progress bar even if vulnerability is found
                
            # Time-based blind SQLi
            rate_limiter.acquire()
            time_payload = "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a) AND '1'='1"
            encoded_time_payload = encode_payload(time_payload)
            time_params = params.copy()
            time_params[param] = [encoded_time_payload]
            time_url = parsed_url._replace(query=urlencode(time_params, doseq=True)).geturl()
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/58.0.3029.110 Safari/537.3'
                }
                start_time = time.time()
                response = requests.get(time_url, verify=False, headers=headers, timeout=10)
                end_time = time.time()
                
                if end_time - start_time >= 5:
                    vulnerability = {
                        "url": url,
                        "parameter": param,
                        "payload": time_payload,
                        "test_url": time_url,
                        "type": "Time-based blind SQLi"
                    }
                    print_queue.put(vulnerability)
            except requests.RequestException as e:
                print_queue.put(f"{Fore.YELLOW}Error during time-based test for {url}: {str(e)}{Fore.RESET}")
            finally:
                bar()  # Increment the progress bar for each payload scanned

    def print_worker(print_queue):
        while True:
            item = print_queue.get()
            if item is None:
                break
            if isinstance(item, dict):
                print_vulnerability(item)
            else:
                print(item)
            print_queue.task_done()

    def sqli_scanner(target):
        print_queue = Queue()
        print_thread = threading.Thread(target=print_worker, args=(print_queue,))
        print_thread.start()

        if os.path.isfile(target):
            with open(target, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
        else:
            urls = [target]

        try:
            with open("payloads/sqli.txt", "r") as f:
                payloads = [x.strip() for x in f.readlines()]
        except FileNotFoundError:
            print(f"{Fore.RED}Payload file 'payloads/sqli.txt' not found.{Fore.RESET}")
            return []

        total_payloads = 0
        # Calculate total payloads based on number of URLs and number of payloads per URL
        for url in urls:
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            if params:
                # Error-based payloads
                error_payloads = [
                    "' OR '1'='1",
                    "' OR '1'='1' --",
                    "' UNION SELECT NULL, NULL, NULL --",
                    "1' ORDER BY 1--+",
                    "1' ORDER BY 2--+",
                    "1' ORDER BY 3--+",
                    "1 UNION SELECT NULL, NULL, NULL --",
                ]
                total_payloads += len(params) * len(error_payloads)
                
                # Boolean-based payloads (1 per parameter)
                total_payloads += len(params) * 1
                
                # Time-based payloads (1 per parameter)
                total_payloads += len(params) * 1

        if total_payloads == 0:
            print(f"{Fore.YELLOW}No parameters found in the target URL(s) to perform SQLi scanning.{Fore.RESET}")
            return []

        all_vulnerabilities = []
        # Initialize the rate limiter
        rate_limiter = threading.Semaphore(RATE_LIMIT)

        def release_rate_limiter():
            while True:
                time.sleep(REQUEST_INTERVAL)
                rate_limiter.release()

        # Start a thread to release the semaphore at the defined rate
        rate_thread = threading.Thread(target=release_rate_limiter, daemon=True)
        rate_thread.start()

        with alive_bar(total_payloads, title="Scanning SQL Injection Vulnerabilities") as bar:
            with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                future_to_url = {executor.submit(sqli_scan_url, url, print_queue, bar, rate_limiter): url for url in urls}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        vulnerabilities = future.result()
                        all_vulnerabilities.extend(vulnerabilities)
                    except Exception as exc:
                        print_queue.put(f'{Fore.RED}Error scanning {url}: {exc}{Fore.RESET}')

        print_queue.put(None)
        print_thread.join()

        return all_vulnerabilities

    if __name__ == "__main__":
        vulnerabilities = sqli_scanner(args.sqli_scan)
        if vulnerabilities:
            print(f"\n{Fore.RED}Total SQL Injection vulnerabilities found: {len(vulnerabilities)}{Fore.RESET}")
        else:
            print(f"\n{Fore.GREEN}No SQL Injection vulnerabilities found.{Fore.RESET}")


if args.webserver_scan:
    init(autoreset=True)

    def get_server_info(url, path=''):
        full_url = urljoin(url, path)
        try:
            response = requests.get(full_url, allow_redirects=False, timeout=10)
            return response.headers, response.status_code, response.text
        except requests.RequestException:
            return {}, None, ''

    def analyze_headers(headers):
        server_info = {}
        for header, value in headers.items():
            if header.lower() == 'server':
                server_info['Server'] = value
            elif header.lower() == 'x-powered-by':
                server_info['X-Powered-By'] = value
            elif header.lower() == 'x-aspnet-version':
                server_info['ASP.NET'] = value
            elif header.lower() == 'x-generator':
                server_info['Generator'] = value
        return server_info

    def check_specific_files(url):
        files_to_check = {
            '/favicon.ico': {'Apache': 'Apache', 'Nginx': 'Nginx'},
            '/server-status': {'Apache': 'Apache Status'},
            '/nginx_status': {'Nginx': 'Nginx Status'},
            '/web.config': {'IIS': 'IIS Config'},
            '/phpinfo.php': {'PHP': 'PHP Version'}
        }
        
        results = {}
        for file, signatures in files_to_check.items():
            headers, status, content = get_server_info(url, file)
            if status == 200:
                for server, signature in signatures.items():
                    if signature in content:
                        results[server] = f"Detected via {file}"
        return results

    def detect_web_server(url):
        if not url.startswith('http'):
            url = 'http://' + url

        print(f"Scanning {Fore.GREEN}{url}{Fore.WHITE}...{Style.RESET_ALL}")

        headers, status, content = get_server_info(url)
        
        if status is None:
            print(f"{Fore.RED}Error: Unable to connect to the server{Style.RESET_ALL}")
            return

        server_info = analyze_headers(headers)
        
        if 'Server' not in server_info:
            if 'Set-Cookie' in headers and 'ASPSESSIONID' in headers['Set-Cookie']:
                server_info['Likely'] = 'IIS'
            elif 'Set-Cookie' in headers and 'PHPSESSID' in headers['Set-Cookie']:
                server_info['Likely'] = 'PHP'
        
        file_results = check_specific_files(url)
        server_info.update(file_results)

        if server_info:
            for key, value in server_info.items():
                print(f"{Fore.GREEN}{key}:{Style.RESET_ALL} {Fore.YELLOW}{value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Unable to determine web server{Style.RESET_ALL}")

        if 'CF-RAY' in headers:
            print(f"{Fore.GREEN}Cloudflare detected{Style.RESET_ALL}")
        
        if 'X-Varnish' in headers:
            print(f"{Fore.GREEN}Varnish Cache detected{Style.RESET_ALL}")

    def main():
        detect_web_server(args.webserver_scan)

    if __name__ == "__main__":
        main()

if args.javascript_scan:
    init(autoreset=True)

    def is_valid_url(url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_js_files(url):
        js_files = set()
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find <script> tags with src attribute
            for script in soup.find_all('script', src=True):
                script_url = urljoin(url, script['src'])
                if is_valid_url(script_url):
                    js_files.add(script_url)
            
            # Find JavaScript files in <link> tags
            for link in soup.find_all('link', rel='stylesheet'):
                if 'href' in link.attrs:
                    css_url = urljoin(url, link['href'])
                    if is_valid_url(css_url):
                        css_response = requests.get(css_url, timeout=10)
                        js_urls = re.findall(r'url\([\'"]?(.*?\.js)[\'"]?\)', css_response.text)
                        for js_url in js_urls:
                            full_js_url = urljoin(css_url, js_url)
                            if is_valid_url(full_js_url):
                                js_files.add(full_js_url)
            
            # Find JavaScript files mentioned in inline scripts
            for script in soup.find_all('script'):
                if script.string:
                    js_urls = re.findall(r'[\'"]([^\'"]*\.js)[\'"]', script.string)
                    for js_url in js_urls:
                        full_js_url = urljoin(url, js_url)
                        if is_valid_url(full_js_url):
                            js_files.add(full_js_url)
            
        except requests.RequestException as e:
            print(f"{Fore.RED}Error fetching {url}: {e}{Style.RESET_ALL}")
        
        return js_files

    def analyze_js_file(js_url):
        try:
            response = requests.get(js_url, timeout=10)
            content = response.text
            size = len(content)
            
            # Analysis patterns
            interesting_patterns = {
                'API Keys': r'(?i)(?:api[_-]?key|apikey)["\s:=]+(["\'][a-zA-Z0-9_\-]{20,}["\'])',
                'Passwords': r'(?i)(?:password|passwd|pwd)["\s:=]+(["\'][^"\']{8,}["\'])',
                'Tokens': r'(?i)(?:token|access_token|auth_token)["\s:=]+(["\'][a-zA-Z0-9_\-]{20,}["\'])',
                'Sensitive Functions': r'(?i)(eval|setTimeout|setInterval)\s*\([^)]+\)',
            }
            
            findings = {}
            for name, pattern in interesting_patterns.items():
                matches = re.findall(pattern, content)
                if matches:
                    findings[name] = matches
            
            return js_url, size, findings
        except requests.RequestException as e:
            return js_url, None, f"Error: {e}"

    def main():
        print(f"Scanning {Fore.GREEN}{args.javascript_scan} {Fore.WHITE}for JavaScript files...{Style.RESET_ALL}")
        
        js_files = get_js_files(args.javascript_scan)
        if not js_files:
            print(f"{Fore.YELLOW}No JavaScript files found.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}Found {len(js_files)} JavaScript files. Analyzing...{Style.RESET_ALL}\n")
        
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            results = list(executor.map(analyze_js_file, js_files))
        
        for url, size, findings in results:
            print(f"{Fore.MAGENTA}File: {url}{Style.RESET_ALL}")
            if size is not None:
                print(f"Size: {size} bytes")
                if findings:
                    print("Potential sensitive information:")
                    for name, matches in findings.items():
                        print(f"  - {name}:")
                        for match in matches[:5]:  # Limit to first 5 matches to avoid overwhelming output
                            print(f"    {match}")
                        if len(matches) > 5:
                            print(f"    ... and {len(matches) - 5} more")
                else:
                    print("No potential sensitive information found.")
            else:
                print(f"{Fore.RED}{findings}{Style.RESET_ALL}")
            print()

    if __name__ == "__main__":
        main()

if args.javascript_endpoints:

    init(autoreset=True)

    async def fetch(session, url):
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    pass
                    return None
        except aiohttp.ClientError as e:
            print(f"{Fore.RED}Error fetching {url}: {e}{Style.RESET_ALL}")
        except asyncio.TimeoutError:
            print(f"{Fore.RED}Timeout error fetching {url}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Unexpected error fetching {url}: {e}{Style.RESET_ALL}")
        return None

    def find_endpoints(js_content):
        # This regex pattern looks for common endpoint patterns in JavaScript
        endpoint_pattern = r'(?:"|\'|\`)(/(?:api/)?[\w-]+(?:/[\w-]+)*(?:\.\w+)?)'
        endpoints = set(re.findall(endpoint_pattern, js_content))
        return endpoints

    async def analyze_js_file(session, js_url):
        js_content = await fetch(session, js_url)
        if js_content:
            endpoints = find_endpoints(js_content)
            return js_url, endpoints
        return js_url, set()

    async def process_js_files(file_path, concurrency):
        js_files = {}
        
        try:
            with open(file_path, 'r') as file:
                js_urls = [line.strip() for line in file if line.strip()]

            async with aiohttp.ClientSession() as session:
                semaphore = asyncio.Semaphore(concurrency)
                
                async def bounded_analyze_js_file(js_url):
                    async with semaphore:
                        return await analyze_js_file(session, js_url)
                
                tasks = [bounded_analyze_js_file(js_url) for js_url in js_urls]
                results = await asyncio.gather(*tasks)

                for js_url, endpoints in results:
                    js_files[js_url] = endpoints

        except Exception as e:
            print(f"{Fore.RED}Error processing JS file list: {e}{Style.RESET_ALL}")

        return js_files

    async def main():
        print(f"{Fore.CYAN}Analyzing JavaScript files from {Fore.GREEN}{args.javascript_endpoints}{Style.RESET_ALL}\n")
        js_files = await process_js_files(args.javascript_endpoints, args.concurrency)

        if js_files:
            print(f"\n{Fore.YELLOW}Analyzed {len(js_files)} JavaScript files:{Style.RESET_ALL}")
            for js_url, endpoints in js_files.items():
                print(f"\n{Fore.CYAN}{js_url}{Style.RESET_ALL}")
                if endpoints:
                    print(f"{Fore.GREEN}Endpoints found:{Style.RESET_ALL}")
                    for endpoint in sorted(endpoints):
                        print(f"  {endpoint}")
                else:
                    print(f"{Fore.YELLOW}No endpoints found{Style.RESET_ALL}")

            if args.save:
                try:
                    with open(args.save, 'w') as f:
                        for js_url, endpoints in js_files.items():
                            f.write(f"{js_url}\n")
                            if endpoints:
                                f.write("Endpoints:\n")
                                for endpoint in sorted(endpoints):
                                    f.write(f"  {endpoint}\n")
                            else:
                                f.write("No endpoints found\n")
                            f.write("\n")
                    print(f"\n{Fore.GREEN}Results saved to {args.save}{Style.RESET_ALL}")
                except IOError as e:
                    print(f"{Fore.RED}Error saving results to file: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No JavaScript files were successfully analyzed.{Style.RESET_ALL}")

    if __name__ == "__main__":
        asyncio.run(main()) 

if args.param_miner:
    def generate_random_string(length=10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def detect_reflection(response, payload):
        return payload in response.text or payload in response.headers.values()

    def analyze_response_difference(original_response, modified_response):
        if abs(len(original_response.content) - len(modified_response.content)) > 50:
            return True
        return False

    def brute_force_parameter(url, param, original_response):
        try:
            payload = generate_random_string()
            test_url = f"{url}{'&' if '?' in url else '?'}{param}={payload}"
            response = requests.get(test_url, timeout=5, allow_redirects=False)
            
            if detect_reflection(response, payload):
                print(f"{Fore.GREEN}[+] Reflected parameter found: {param}{Style.RESET_ALL}")
                return param, "reflected"
            
            if analyze_response_difference(original_response, response):
                print(f"{Fore.WHITE}[*] Potential parameter found (response changed): {Fore.YELLOW}{param}{Style.RESET_ALL}")
                return param, "potential"
            
            if response.status_code != original_response.status_code:
                print(f"{Fore.WHITE}[*] Status code changed for parameter: {Fore.CYAN}{param} {Fore.YELLOW}({original_response.status_code} -> {response.status_code}){Style.RESET_ALL}")
                return param, "status_changed"
            
        except requests.RequestException:
            pass
        return None, None

    def scan_common_parameters(url):
        common_params = ['id', 'page', 'search', 'q', 'query', 'file', 'filename', 'path', 'dir']
        found_params = []
        for param in common_params:
            result, _ = brute_force_parameter(url, param, requests.get(url, timeout=5))
            if result:
                found_params.append(result)
        return found_params

    def extract_parameters_from_html(url):
        try:
            response = requests.get(url, timeout=5)
            form_params = re.findall(r'name=["\']([^"\']+)["\']', response.text)
            js_params = re.findall(r'(?:get|post)\s*\(\s*["\'][^"\']*\?([^"\'&]+)=', response.text)
            return list(set(form_params + js_params))
        except requests.RequestException:
            return []

    def main(url, wordlist, threads):
        print(f"{Fore.BLUE}[*] Starting parameter mining on: {url}{Style.RESET_ALL}")
        
        original_response = requests.get(url, timeout=5)
        
        print(f"{Fore.MAGENTA}[*] Scanning for common parameters...{Style.RESET_ALL}")
        common_params = scan_common_parameters(url)
        
        print(f"{Fore.MAGENTA}[*] Extracting parameters from HTML and JavaScript...{Style.RESET_ALL}")
        extracted_params = extract_parameters_from_html(url)
        
        with open(wordlist, 'r') as file:
            wordlist_params = [line.strip() for line in file]
        all_params = list(set(wordlist_params + extracted_params + common_params))
        
        print(f"{Fore.BLUE}[*] Testing {len(all_params)} unique parameters...{Style.RESET_ALL}")
        
        reflected_params = []
        potential_params = []
        status_changed_params = []
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(brute_force_parameter, url, param, original_response) for param in all_params]
            for future in as_completed(futures):
                result, category = future.result()
                if result:
                    if category == "reflected":
                        reflected_params.append(result)
                    elif category == "potential":
                        potential_params.append(result)
                    elif category == "status_changed":
                        status_changed_params.append(result)
        
        print(f"\n{Fore.GREEN}[+] Reflected parameters: {', '.join(reflected_params)}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[*] Potential parameters: {Fore.YELLOW}{', '.join(potential_params)}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[*] Status-changing parameters: {Fore.CYAN}{', '.join(status_changed_params)}{Style.RESET_ALL}")

    if __name__ == "__main__":
        try:
            main(args.param_miner, args.wordlist, args.concurrency)
        except KeyboardInterrupt:
            print(f"{Fore.RED}Scan interrupted by user.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        
if args.custom_headers:
    def print_headers(headers):
        print(f"{Fore.CYAN}Headers:{Style.RESET_ALL}")
        for key, value in headers.items():
            print(f"{Fore.GREEN}{key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")

    def extract_links(content, base_url):
        soup = BeautifulSoup(content, 'html.parser')
        links = [urljoin(base_url, link.get('href')) for link in soup.find_all('a', href=True)]
        return links

    def send_request(url, method='GET', custom_headers=None, data=None, params=None, auth=None, proxies=None, allow_redirects=True, verbose=False):
        try:
            start_time = time.time()
            response = requests.request(
                method=method,
                url=url,
                headers=custom_headers,
                data=data,
                params=params,
                auth=auth,
                proxies=proxies,
                allow_redirects=allow_redirects,
                timeout=10
            )
            end_time = time.time()

            print(f"\n{Fore.MAGENTA}Status Code: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Response Time: {end_time - start_time:.2f} seconds{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Response Size: {len(response.content)} bytes{Style.RESET_ALL}")
            
            print("\n--- Request Details ---")
            print(f"{Fore.CYAN}Method: {method}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}URL: {url}{Style.RESET_ALL}")
            print_headers(response.request.headers)
            
            if data:
                print(f"\n{Fore.CYAN}Request Data:{Style.RESET_ALL}")
                print(json.dumps(data, indent=2))
            
            print("\n--- Response Details ---")
            print_headers(response.headers)
            
            if verbose:
                print(f"\n{Fore.CYAN}Response Content:{Style.RESET_ALL}")
                print(response.text)
            
            links = extract_links(response.text, url)
            print(f"\n{Fore.CYAN}Links found in the response:{Style.RESET_ALL}")
            for link in links:
                print(link)

            return response
        except requests.RequestException as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return None

    def load_headers_from_file(filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def main(initial_url, verbose):
        url = initial_url
        session = requests.Session()
        
        while True:
            print(f"\n{Fore.YELLOW}Current URL: {url}{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Options:{Style.RESET_ALL}")
            print("1. Send GET request with default headers")
            print("2. Send GET request with custom headers")
            print("3. Send POST request")
            print("4. Send request with custom method and headers")
            print("5. Change URL")
            print("6. Load headers from file")
            print("7. Set authentication")
            print("8. Set proxy")
            print("9. Toggle redirect following")
            print("10. Save last response to file")
            print("11. Exit")
            
            choice = input(f"{Fore.CYAN}Enter your choice (1-11): {Style.RESET_ALL}")
            
            if choice == '1':
                send_request(url, verbose=verbose)
            elif choice == '2':
                custom_headers = {}
                print(f"{Fore.YELLOW}Enter custom headers (one per line, format 'Key: Value'). Type 'done' when finished.{Style.RESET_ALL}")
                while True:
                    header = input()
                    if header.lower() == 'done':
                        break
                    key, value = header.split(': ', 1)
                    custom_headers[key] = value
                send_request(url, custom_headers=custom_headers, verbose=verbose)
            elif choice == '3':
                data = input(f"{Fore.CYAN}Enter POST data (JSON format): {Style.RESET_ALL}")
                send_request(url, method='POST', data=json.loads(data), verbose=verbose)
            elif choice == '4':
                method = input(f"{Fore.CYAN}Enter HTTP method: {Style.RESET_ALL}").upper()
                custom_headers = {}
                print(f"{Fore.YELLOW}Enter custom headers (one per line, format 'Key: Value'). Type 'done' when finished.{Style.RESET_ALL}")
                while True:
                    header = input()
                    if header.lower() == 'done':
                        break
                    key, value = header.split(': ', 1)
                    custom_headers[key] = value
                send_request(url, method=method, custom_headers=custom_headers, verbose=verbose)
            elif choice == '5':
                url = input(f"{Fore.CYAN}Enter the new URL to check: {Style.RESET_ALL}")
            elif choice == '6':
                filename = input(f"{Fore.CYAN}Enter the filename to load headers from: {Style.RESET_ALL}")
                custom_headers = load_headers_from_file(filename)
                send_request(url, custom_headers=custom_headers, verbose=verbose)
            elif choice == '7':
                username = input(f"{Fore.CYAN}Enter username: {Style.RESET_ALL}")
                password = input(f"{Fore.CYAN}Enter password: {Style.RESET_ALL}")
                send_request(url, auth=(username, password), verbose=verbose)
            elif choice == '8':
                proxy = input(f"{Fore.CYAN}Enter proxy URL: {Style.RESET_ALL}")
                send_request(url, proxies={'http': proxy, 'https': proxy}, verbose=verbose)
            elif choice == '9':
                allow_redirects = input(f"{Fore.CYAN}Allow redirects? (y/n): {Style.RESET_ALL}").lower() == 'y'
                send_request(url, allow_redirects=allow_redirects, verbose=verbose)
            elif choice == '10':
                filename = input(f"{Fore.CYAN}Enter filename to save response: {Style.RESET_ALL}")
                response = send_request(url, verbose=verbose)
                if response:
                    with open(filename, 'w') as f:
                        json.dump(response.json(), f, indent=2)
                    print(f"{Fore.GREEN}Response saved to {filename}{Style.RESET_ALL}")
            elif choice == '11':
                print(f"{Fore.GREEN}Exiting. Goodbye!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

    if args.custom_headers:
        if args.verbose:
            print(f"{Fore.CYAN}Verbose mode enabled{Style.RESET_ALL}")
        main(args.custom_headers, args.verbose)


if args.openredirect:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    TEST_DOMAIN = "google.com"

    PAYLOADS = [
        f"//{TEST_DOMAIN}",
        f"//www.{TEST_DOMAIN}",
        f"https://{TEST_DOMAIN}",
        f"https://www.{TEST_DOMAIN}",
        f"//{TEST_DOMAIN}/%2f..",
        f"https://{TEST_DOMAIN}/%2f..",
        f"////{TEST_DOMAIN}",
        f"https:////{TEST_DOMAIN}",
        f"/\\/\\{TEST_DOMAIN}",
        f"/.{TEST_DOMAIN}",
        f"///\\;@{TEST_DOMAIN}",
        f"///{TEST_DOMAIN}@{TEST_DOMAIN}",
        f"///{TEST_DOMAIN}%40{TEST_DOMAIN}",
        f"////{TEST_DOMAIN}//",
        f"/https://{TEST_DOMAIN}",
        f"{TEST_DOMAIN}",
    ]

    def test_single_payload(url, payload, original_netloc):
        try:
            full_url = f"{url}{payload}"
            response = requests.get(full_url, allow_redirects=False, verify=False, timeout=5)
            if args.verbose:
                print(f"Testing: {full_url}")
                print(f"Status Code: {response.status_code}")
                print(f"Location: {response.headers.get('Location', 'N/A')}")
            if response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get('Location', '')
                if location:
                    parsed_location = urllib.parse.urlparse(location)
                    # If 'location' is a relative URL, resolve it against the original URL
                    if not parsed_location.netloc:
                        location = urllib.parse.urljoin(full_url, location)
                        parsed_location = urllib.parse.urlparse(location)
                    # Now compare the netloc of the location with the original netloc
                    if parsed_location.netloc and parsed_location.netloc != original_netloc:
                        # Check if the TEST_DOMAIN is in the netloc
                        if TEST_DOMAIN in parsed_location.netloc:
                            print(f"{RED}VULNERABLE: Redirects to {location}{RESET}")
                            return (full_url, location)
            elif response.status_code == 403:
                print(f"{url}: {RED}FORBIDDEN{RESET}")
        except requests.RequestException as e:
            if args.verbose:
                print(f"Error testing {full_url}: {str(e)}")
        return None

    def test_open_redirect(url):
        vulnerable_urls = []
        parsed_original_url = urllib.parse.urlparse(url)
        original_netloc = parsed_original_url.netloc
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            future_to_payload = {
                executor.submit(test_single_payload, url, payload, original_netloc): payload
                for payload in PAYLOADS
            }
            for future in concurrent.futures.as_completed(future_to_payload):
                result = future.result()
                if result:
                    vulnerable_urls.append(result)
        return vulnerable_urls

    def process_url(url):
        print(f"{YELLOW}Testing: {url}{RESET}")
        vulnerabilities = test_open_redirect(url)
        if vulnerabilities:
            print(f"{RED}[VULNERABLE] {url}{RESET}")
            for vuln_url, redirect_url in vulnerabilities:
                print(f"  Payload URL: {vuln_url}")
                print(f"  Redirects to: {redirect_url}")
            print()
        else:
            print(f"{GREEN}[NOT VULNERABLE] {url}{RESET}\n")

    def main():
        if args.openredirect:
            process_url(args.openredirect)

    if __name__ == "__main__":
        main()


if args.automoussystemnumber:
    def get_ip_ranges(asn):
        asn = args.automoussystemnumber
        url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and 'prefixes' in data['data']:
                return asn, [prefix['prefix'] for prefix in data['data']['prefixes']]
            else:
                return asn, []
        except requests.RequestException as e:
            print(f"Error fetching data for {asn}: {e}", file=sys.stderr)
            return asn, []

    def process_asn(asn):
        print(f"Fetching IP ranges for AS{asn}...")
        return get_ip_ranges(asn)

    def main():
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            future_to_asn = {executor.submit(process_asn, asn): asn for asn in args.automoussystemnumber}
            for future in concurrent.futures.as_completed(future_to_asn):
                asn, ip_ranges = future.result()
                results[asn] = ip_ranges

        total_ranges = sum(len(ranges) for ranges in results.values())
        print(f"\nFound a total of {total_ranges} IP ranges across {len(args.automoussystemnumber)} ASNs:")

        if args.save:
            with open(args.save, 'w') as f:
                for asn, ranges in results.items():
                    if ranges:
                        f.write(f"AS{asn}:\n")
                        for range in ranges:
                            f.write(f"{range}\n")
                        f.write("\n")
            print(f"Results saved to {args.save}")
        else:
            for asn, ranges in results.items():
                if ranges:
                    print(f"\nAS{asn}:")
                    for range in ranges:
                        print(range)
    if __name__ == "__main__":
        main()


if args.haveibeenpwned:
    print(f"{Fore.CYAN}HAVE I BEEN PWNED!{Style.RESET_ALL}\n")
    print(f"Checking password: {Fore.GREEN}{args.haveibeenpwned}{Style.RESET_ALL}\n")
    def check_password_pwned(password):
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    print(f"The password {Fore.GREEN}'{password}'{Fore.RESET} has been seen {Fore.RED}{count} times.{Fore.RESET}")
                    return

            print(f"The password {Fore.GREEN}'{password}'{Fore.RESET} has not been found in any breaches.")

        except requests.exceptions.HTTPError as err:
            print(f"Error checking password: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

    if __name__ == "__main__":
        password_to_check = args.haveibeenpwned
        check_password_pwned(password_to_check)

if args.subdomaintakeover:
    COMMON_SERVICES = [
        "GitHub, Inc.", "GitLab Inc.", "Bitbucket", "Heroku, Inc.",
        "Firebase", "Netlify, Inc.", "Surge", "Automattic Inc.",
        "Amazon CloudFront", "Microsoft Azure", "Google LLC"
    ]

    def check_subdomain(subdomain):
        potential_takeover = set()
        url = f"https://{subdomain}"
        try:
            response = requests.get(url)
            if response.status == 404:
                print(f"[Potential Takeover] {subdomain} - 404 Not Found")
                potential_takeover.add(subdomain)
                # Save potential takeovers to a file for further analysis
                with open('potential_takeover.txt', 'w') as f:
                    for sub in potential_takeover:
                        f.write(f"{sub}\n")
            elif response.status == 200:
                print(f"[Active] {subdomain} - 200 OK")
            else:
                print(f"[Other] {subdomain} - Status Code: {response.status}")
        except requests.RequestException:
            pass

    def check_dns(subdomain):
        try:
            answers = dns.resolver.resolve(subdomain, 'CNAME')
            for rdata in answers:
                target = str(rdata.target).rstrip('.')
                print(f"{Fore.MAGENTA}[CNAME] {Fore.CYAN}{subdomain}{Style.RESET_ALL} points to {Fore.GREEN}{target}{Style.RESET_ALL}")
                check_whois(target)  # Check WHOIS for the CNAME target
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass  # No CNAME record found
        except Exception as e:
            print(f"{Fore.RED}[DNS Error] {Fore.CYAN}{subdomain} - {Fore.RED}{e}{Style.RESET_ALL}")

    def check_whois(target):
        vuln_subs = set()
        try:
            w = whois.whois(target)
            org_name = w.org if w.org else "Unknown"
            print(f"{Fore.MAGENTA}[WHOIS] {Fore.CYAN}{target}{Style.RESET_ALL} - Organization: {Fore.GREEN}{org_name}{Style.RESET_ALL}")
            for service in COMMON_SERVICES:
                if service.lower() in org_name.lower():
                    vuln_subs.add(target)
                    print(f"{Fore.YELLOW}[Potential Takeover] {Fore.CYAN}{target} is associated with {Fore.GREEN}{org_name} - Common service{Style.RESET_ALL}")
                    break
            with open(f'{args.save}', 'w') as f:
                for sub in vuln_subs:
                    f.write(f"{sub}\n")
        except Exception as e:
            print(f"{Fore.RED}[WHOIS Error] {Fore.CYAN}{target} - {Fore.RED}{e}{Style.RESET_ALL}")

    def check_subdomain_takeover(subdomain):
        check_dns(subdomain)  
        check_subdomain(subdomain)  

    def load_subdomains(file_path):
        try:
            with open(file_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}[Error] {Fore.CYAN}{file_path} - {Fore.RED}File not found{Style.RESET_ALL}")
            return []

    def main():
        subdomains = load_subdomains(args.subdomaintakeover)

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            executor.map(check_subdomain_takeover, subdomains)

    if __name__ == "__main__":
        main()   



if args.autorecon:
    async def fetch(session, url):
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            print(f"Invalid URL: {url}")
            return None
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        
    async def waybackpy(target):
        waybackurls = scan(f"waybackurls {target} | anew")
        return waybackurls
    
    async def portscan(target):
        if target.startswith("http://") or target.startswith("https://"):
            target = target.replace("http://", "").replace("https://", "")
        if target.startswith("www."):
            target = target[4:]
        if target.startswith("https://www."):
            target = target[8:]
        if target.endswith("/"):
            target = target[:-1]
        ports = scan(f"naabu -host {target} -silent")
        return ports
    
    async def dnsscan(target):
        dnsscan = scan(f"echo {target} | dnsx -silent -recon -j dnsscan.json")
        return dnsscan
    
    async def techdetect(target):
        tech = {}
        try:
            info = builtwith(f"{target}")
            for framework, tech in info.items():
                tech.append(f"{framework}: {tech}")
        except UnicodeDecodeError:
            pass
        return tech
    
    async def ssl_vuln_scan(target):
        TLS_VERSION = []
        TLS_VULN_VERSION = ["TLSv1.0", "TLSv1.1", "SSLv2", "SSLv3"]

        def check_ssl(domain: str, port: int = 443):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        TLS_VERSION.append(ssock.version())
                        return f"TLS Version: {ssock.version()}\nCipher Suite: {ssock.cipher()[0]}\nIssuer: {cert['issuer'][0][0]}\nSubject: {cert['subject'][0][0]}\nValid From: {datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d %H:%M:%S')}\nValid To: {datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%d %H:%M:%S')}"
            except Exception as e:
                print(f"Error checking SSL: {e}")


        def save_ssl_info(domain: str, info: str, port: int = 443):
            if info:
                with open('ssl_info.txt', 'w') as f:
                    f.write(info)

        if "http://" in target or "https://" in target:
            target = target.replace("http://", "").replace("https://", "")
        if "www." in target:
            target = target[4:]
        if "https://www." in target:
            target = target[8:]
        if target.endswith("/"):
            target = target[:-1]

        info = check_ssl(target)
        if TLS_VERSION in TLS_VULN_VERSION:
            print(f"{TLS_VERSION}: VULNERABLE!")
            print(f"Mitigation: Please update your SSL/TLS version to a more secure version.")
        save_ssl_info(target, info)
        return info
    
    async def headers_info(target: str):
        try:
            s = requests.Session()
            r = s.get(target, verify=False, headers=header)
        except Exception as e:
            print(f"Error fetching {target}: {e}")
            return []
        http_headers = []
        for k,v in r.headers.items():
            http_headers.append(f"{k}: {v}")    
        return http_headers
    
    async def server_info(target):
        s = requests.Session()
        r = s.get(target, verify=False, headers=header)
        return r.headers.get("Server")
    
    async def crawl_site(target):
        print(f"{Fore.MAGENTA}Crawling {Fore.CYAN}{target}{Style.RESET_ALL} for links...")
        
        connector = aiohttp.TCPConnector(ssl=False)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            response_text = await fetch(session, target)
            if response_text:
                soup = BeautifulSoup(response_text, 'html.parser')
                links = set() 
                for link in soup.find_all('a', href=True):
                    full_url = link['href']
                    if not full_url.startswith('http'):
                        full_url = urlparse(target)._replace(path=full_url).geturl()
                    parsed_url = urlparse(full_url)
                    if all([parsed_url.scheme, parsed_url.netloc]):
                        links.add(full_url)
                    else:
                        print(f"Invalid link found: {full_url}")
                return links 
        return set() 

    async def extract_js_files(links, target):
        print(f"{Fore.MAGENTA}Extracting JavaScript files from links...{Style.RESET_ALL}")
        js_files = set() 
        target_parsed = urlparse(target)  
        async with aiohttp.ClientSession() as session:
            for link in links:
                try:
                    response = await fetch(session, link)  
                    if response:
                        soup = BeautifulSoup(response, 'html.parser')
                        for script in soup.find_all('script', src=True):
                            js_url = urljoin(link, script['src'])
                            js_parsed = urlparse(js_url)
                            if js_parsed.netloc == target_parsed.netloc:
                                js_files.add(js_url)
                except Exception as e:
                    print(f"Error extracting JS from {link}: {e}")
        return js_files

    def extract_parameters(links):
        print(f"{Fore.MAGENTA}Extracting parameters from links...{Style.RESET_ALL}")
        parameters = {}
        for link in links:
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            if query_params:
                parameters[link] = query_params
        return parameters

    def shodan_search(target, api):
        shodan_api = shodan.Shodan(api)
        print(f"{Fore.MAGENTA}Searching Shodan for {Fore.CYAN}{target}{Style.RESET_ALL}...")
        results = []
        try:
            # Perform the Shodan search
            results = shodan_api.search(target)
            print(f"Found {results['total']} results for {target}.")
            
            # Extract subdomains, port numbers, and services
            extracted_data = []
            for match in results['matches']:
                ip = match['ip_str']
                port = match['port']
                services = match.get('product', 'Unknown')  # Get the service/product name
                extracted_data.append(f"IP: {ip}, Port: {port}, Service: {services}")
            
            return extracted_data
        except Exception as e:
            print(f"Error searching Shodan: {e}")
            return []

    async def main(target):
        print(f"{Fore.MAGENTA}Running autorecon for {Fore.CYAN}{target}{Style.RESET_ALL}\n")
        shodankey = input(f"{Fore.CYAN}Enter your Shodan API key: {Style.RESET_ALL}")
        print("\n")
        with alive_bar(12, title='Running autorecon') as bar:
            site_links = await crawl_site(target)
            print(f"{Fore.MAGENTA}Found {Fore.CYAN}{len(site_links)}{Style.RESET_ALL} links from crawling.")
            with open('site_links.txt', 'w') as f:
                for link in site_links:
                    f.write(f"{link}\n")
            bar()  # Update after crawling site

            all_links = site_links  # Only site links now

            # Extract JavaScript files, passing the 
            js_files = await extract_js_files(all_links, target)
            print(f"{Fore.MAGENTA}Found {Fore.CYAN}{len(js_files)}{Style.RESET_ALL} JavaScript files.")
            with open('js_files.txt', 'w') as f:
                for js_file in js_files:
                    f.write(f"{js_file}\n")
            bar()  # Update after extracting JS files

            #Wayback urls 
            waybackurls = await waybackpy(target)
            with open('waybackurls.txt', 'w') as f:
                f.write(f"{waybackurls}\n")
            
            with open('waybackurls.txt', 'r') as f:
                waybackurls_lines = [line.strip() for line in f if line.strip()]
                print(f"{Fore.MAGENTA}Found {Fore.CYAN}{len(waybackurls_lines)}{Style.RESET_ALL} waybackurls.")
            bar()  # Update after waybackurls

            #Naabu portscan
            ports = await portscan(target)
            with open('ports.txt', 'w') as f:
                f.write(f"{ports}\n")

            with open('ports.txt', 'r') as f:
                ports_lines = [line.strip() for line in f if line.strip()]
                numbers = []
                for port in ports_lines:
                    found_numbers = re.findall(r'[-+]?\d*\.\d+|\d+', port)
                    numbers.extend(found_numbers)     
                print(f"{Fore.MAGENTA}Found {Fore.CYAN}{len(ports_lines)}{Style.RESET_ALL} Open Ports.")
                print(f"{Fore.MAGENTA}Open Ports: {Fore.CYAN}{', '.join(map(str, numbers))}{Style.RESET_ALL}")
            bar()  # Update after ports scan

            #Get headers
            getheaders = await headers_info(target)
            target2 = target.replace("https://", "").replace("http://", "").replace("www.", "")
            with open(f"headers.txt", "w") as f:
                for header in getheaders:
                    f.write(f"{header}\n")
            bar()

            #Server info
            serverinfo = await server_info(target)
            print(f"{Fore.MAGENTA}Server: {Fore.CYAN}{serverinfo}{Style.RESET_ALL}")
            bar()

            #Dnsscan
            dns = await dnsscan(target)
            with open('dnsscan.json', 'w') as f:
                f.write(f"{dns}\n")
            print(f"{Fore.MAGENTA}DNS Scan: {Fore.CYAN}DONE!{Style.RESET_ALL}")
            dns_output = scan(f"python3 dnsparser.py -dns dnsscan.json")
            with open('dns_output.txt', 'w') as f:
                f.write(f"{dns_output}\n")
            bar()  # Update after dnsscan

            #Techdetect
            tech = await techdetect(target)
            print(f"{Fore.MAGENTA}Tech Detect: {Fore.CYAN}{tech}{Style.RESET_ALL}")
            with open('techdetect.txt', 'w') as f:
                for techs in tech:
                    f.write(f"{techs}\n")
            bar()  # Update after techdetect

            parameters = extract_parameters(all_links)
            links_params = set()
            for links in parameters:
                links_params.add(links)
            with open('links_params.txt', 'w') as f:
                for link in links_params:
                    f.write(f"{link}\n")
            bar()  # Update after extracting parameters

            # Print parameters for each link
            for link in links_params:
                print(f"{Fore.MAGENTA}Found {Fore.CYAN}{len(links_params)}{Style.RESET_ALL} Links with Parameters")

            # Perform Shodan search and save results to a file
            shodan_results = shodan_search(target, shodankey)
            with open('shodan_results.txt', 'w') as f:
                for result in shodan_results:
                    f.write(f"{result}\n")
            bar()  # Update after Shodan search

            ssl_scan = await ssl_vuln_scan(target)  
            print(f"{Fore.MAGENTA}TLS/SSL Scan: {Fore.CYAN}ssl_info.txt{Style.RESET_ALL}")
            bar()

            scanner = S3Scanner()
            s3_results = await scanner.scan(target)
            scanner.save_results(target)
            bar()
            
    if __name__ == "__main__":
        target_url = args.autorecon
        asyncio.run(main(target_url))

if args.jwt_scan:
    analyzer = JWTAnalyzer()
    analyzer.analyze_token(args.jwt_scan)
elif args.jwt_modify:
    analyzer = JWTAnalyzer()
    analyzer.modify_token(args.jwt_modify)

async def handle_s3_scan(target):
    print(f"\n{Fore.MAGENTA}Starting S3 bucket scan for {Fore.CYAN}{target}{Style.RESET_ALL}")
    scanner = S3Scanner()
    with alive_bar(1, title='Scanning S3 buckets') as bar:
        results = await scanner.scan(target)
        scanner.save_results(target)
        bar()
    return results

if args.s3_scan:
    asyncio.run(handle_s3_scan(args.s3_scan))

if args.heapdump:
    analyzer = HeapdumpAnalyzer()
    analyzer.analyze(args.heapdump, args.output_dir)

if args.heapdump_scan:
    commands(f"python3 modules/heapdump_scan.py --file {args.heapdump_scan}")