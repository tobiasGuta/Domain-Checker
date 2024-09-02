import requests
from requests.exceptions import RequestException
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import re


def is_valid_domain(domain):
    """Check if the domain is a valid format."""
    return bool(re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain))

def check_accessibility(domain):
    statuses = {}
    protocols = ['http', 'https']

    if not is_valid_domain(domain):
        # Skip invalid domains
        return domain, {'http': {'status_code': None, 'error': 'Invalid domain'}, 'https': {'status_code': None, 'error': 'Invalid domain'}}

    for protocol in protocols:
        url = f'{protocol}://{domain}'
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError(f"Invalid URL: {url}")
        except ValueError as e:
            statuses[protocol] = {'status_code': None, 'error': str(e)}
            continue

        try:
            response = requests.get(url, timeout=10, allow_redirects=True)
            statuses[protocol] = {
                'status_code': response.status_code,
                'url': response.url,
                'headers': dict(response.headers)
            }
        except RequestException as e:
            statuses[protocol] = {'status_code': None, 'error': str(e)}

    return domain, statuses

def format_output(domain, http_status, https_status):
    http_msg = (f"HTTP: {http_status['status_code']} {http_status['url']}"
                if http_status['status_code'] else "HTTP: Down")
    https_msg = (f"HTTPS: {https_status['status_code']} {https_status['url']}"
                 if https_status['status_code'] else "HTTPS: Down")
    
    print("\n" + "="*50)
    print(f"Domain: {domain}")
    print(http_msg)
    print(https_msg)
    print("="*50)

def main():
    accessible_domains = []
    subdomains = []

    # Read subdomains from file
    with open('all_subdomains.txt', 'r') as file:
        subdomains = [line.strip() for line in file if line.strip()]

    # Define the number of threads to use
    num_threads = 10  # Adjust as needed

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_domain = {executor.submit(check_accessibility, subdomain): subdomain for subdomain in subdomains}

        for future in as_completed(future_to_domain):
            domain, statuses = future.result()
            http_status = statuses.get('http', {'status_code': None})
            https_status = statuses.get('https', {'status_code': None})

            # Determine if either protocol is accessible
            if http_status['status_code'] == 200 or https_status['status_code'] == 200:
                accessible_domains.append(domain)
                format_output(domain, http_status, https_status)

    # Write accessible domains to a file
    with open('updomains.txt', 'w') as file:
        for domain in accessible_domains:
            file.write(f"{domain}\n")

if __name__ == "__main__":
    main()
