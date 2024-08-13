import requests
from requests.exceptions import RequestException
import time

def check_accessibility(domain):
    """
    Checks the accessibility of a domain for both HTTP and HTTPS protocols.

    Args:
        domain (str): The domain to check.

    Returns:
        dict: A dictionary with the status of HTTP and HTTPS requests.
    """
    statuses = {}
    protocols = ['http', 'https']

    for protocol in protocols:
        url = f'{protocol}://{domain}'
        try:
            response = requests.get(url, timeout=10, allow_redirects=True)  # Follow redirects
            statuses[protocol] = {
                'status_code': response.status_code,
                'url': response.url,  # Final URL after redirects
                'headers': dict(response.headers)  # Capture response headers
            }
        except RequestException as e:
            statuses[protocol] = {'status_code': None, 'error': str(e)}

    return statuses

def format_output(domain, http_status, https_status):
    """
    Formats the output for a single domain in a readable box format.

    Args:
        domain (str): The domain being checked.
        http_status (dict): The status information for HTTP.
        https_status (dict): The status information for HTTPS.
    """
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
    """
    Reads a list of subdomains from a file, checks their accessibility, and writes accessible domains to a file.
    """
    accessible_domains = []

    # Read subdomains from file
    with open('subdomain.txt', 'r') as file:
        subdomains = file.readlines()

    # Define the delay between requests (in seconds)
    delay_between_requests = 10  # Adjust as needed

    for subdomain in subdomains:
        subdomain = subdomain.strip() 

        if not subdomain:  # Skip empty lines
            continue

        # Check accessibility of the subdomain
        statuses = check_accessibility(subdomain)
        http_status = statuses.get('http', {'status_code': None})
        https_status = statuses.get('https', {'status_code': None})

        # Determine if either protocol is accessible
        if http_status['status_code'] == 200 or https_status['status_code'] == 200:
            accessible_domains.append(subdomain)
            format_output(subdomain, http_status, https_status)

        # Wait before making the next request
        time.sleep(delay_between_requests)

    # Write accessible domains to a file
    with open('updomains.txt', 'w') as file:
        for domain in accessible_domains:
            file.write(f"{domain}\n")

if __name__ == "__main__":
    main()
