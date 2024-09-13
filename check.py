import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import re

art = '''

                                                ⠀⠀⡶⠛⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡶⠚⢶⡀⠀
                                                ⢰⠛⠃⠀⢠⣏⠀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣤⣤⣄⣀⡀⠀⠀⠀⣸⠇⠀⠈⠙⣧
                                                ⠸⣦⣤⣄⠀⠙⢷⣤⣶⠟⠛⢉⣁⣤⣤⣤⣤⣀⣉⠙⠻⢷⣤⡾⠋⢀⣤⣤⣴⠏
                                                ⠀⠀⠀⠈⠳⣤⡾⠋⣀⣴⣿⣿⠿⠿⠟⠛⠿⠿⣿⣿⣶⣄⠙⢿⣦⠟⠁⠀⠀⠀
                                                ⠀⠀⠀⢀⣾⠟⢀⣾⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣷⡄⠹⣷⡀⠀⠀⠀
                                                ⠀⠀⠀⣾⡏⢠⣿⣿⡯⠤⠤⠤⠒⠒⠒⠒⠒⠒⠒⠤⠤⠽⣿⣿⡆⠹⣷⡀⠀⠀
                                                ⠀⠀⢸⣟⣠⡿⠿⠟⠒⣒⣒⣉⣉⣉⣉⣉⣉⣉⣉⣉⣒⣒⡛⠻⠿⢤⣹⣇⠀⠀
                                                ⠀⠀⣾⡭⢤⣤⣠⡞⠉⠁⢀⣀⣀⠀⠀⠀⠀⢀⣀⣀⠀⠈⢹⣦⣤⡤⠴⣿⠀⠀
                                                ⠀⠀⣿⡇⢸⣿⣿⣇⠀⣼⣿⣿⣿⣷⠀⠀⣼⣿⣿⣿⣷⠀⢸⣿⣿⡇⠀⣿⠀⠀
                                                ⠀⠀⢻⡇⠸⣿⣿⣿⡄⢿⣿⣿⣿⡿⠀⠀⢿⣿⣿⣿⡿⢀⣿⣿⣿⡇⢸⣿⠀⠀
                                                ⠀⠀⠸⣿⡀⢿⣿⣿⣿⣆⠉⠛⠋⠀⢴⣶⠀⠉⠛⠉⣠⣿⣿⣿⡿⠀⣾⠇⠀⠀
                                                ⠀⠀⠀⢻⣷⡈⢻⣿⣿⣿⣿⣶⣤⣀⣈⣁⣀⡤⣴⣿⣿⣿⣿⡿⠁⣼⠏⠀⠀⠀
                                                ⠀⠀⠀⢀⣽⣷⣄⠙⢿⣿⣿⡟⢲⠧⡦⠼⠤⢷⢺⣿⣿⡿⠋⣠⣾⢿⣄⠀⠀⠀
                                                ⣰⠟⠛⠛⠁⣨⡿⢷⣤⣈⠙⢿⡙⠒⠓⠒⠒⠚⡹⠛⢁⣤⣾⠿⣧⡀⠙⠋⠙⣆
                                                ⠹⣤⡀⠀⠐⡏⠀⠀⠉⠛⠿⣶⣿⣶⣤⣤⣤⣾⣷⠾⠟⠋⠀⠀⢸⡇⠀⢠⣤⠟
                                                ⠀⠀⠳⢤⠾⠃⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠘⠷⠤⠾⠁⠀


 ░▒▓██████▓▒░       ░▒▓███████▓▒░       ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓███████▓▒░       ░▒▓████████▓▒░      ░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░                    ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░                    ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓██████▓▒░           ░▒▓████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░                            
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░                            
 ░▒▓██████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░         ░▒▓█▓▒░     
                                                                                                                                
                                                                                                                                
'''

print(art)

def is_valid_domain(domain):
    """Check if the domain is in a valid format and doesn't contain consecutive dots."""
    # Regex pattern for valid domain format (no consecutive dots allowed)
    pattern = r'^[a-zA-Z0-9]+([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]+([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$'

    # Check if domain has consecutive dots
    if '..' in domain:
        return False
    
    # Check against the regex pattern
    return bool(re.match(pattern, domain))


def check_accessibility(domain):
    """Check if the domain is accessible via HTTP and HTTPS."""
    statuses = {}
    protocols = ['http', 'https']

    if not is_valid_domain(domain):
        # Return an error if the domain is invalid
        error_message = 'Invalid domain'
        return domain, {
            'http': {'status_code': None, 'error': error_message},
            'https': {'status_code': None, 'error': error_message}
        }

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
            status_code = response.status_code
            final_url = response.url
            status_message = f"{status_code} {response.reason}"

            if final_url != url:
                redirect_info = f"--------> Redirect to: {final_url}"
            else:
                redirect_info = ""

            statuses[protocol] = {
                'status_code': status_code,
                'status_message': status_message,
                'redirect_info': redirect_info,
                'final_url': final_url
            }
        except RequestException as e:
            statuses[protocol] = {'status_code': None, 'error': str(e)}

    return domain, statuses

def format_output(domain, http_status, https_status):
    """Format and print the output for accessible URLs."""
    print(f"🔍 Checking : {domain}")
    urls = []

    if http_status['status_code'] == 200:
        http_url = f"http://{domain}"
        final_http_url = http_status.get('final_url', http_url)
        redirect_info = http_status.get('redirect_info', '')
        print(f"Accessible via HTTP: {final_http_url} {redirect_info}")
        print(f"Code: {http_status['status_code']} {http_status['status_message']}")
        urls.append(final_http_url)

    if https_status['status_code'] == 200:
        https_url = f"https://{domain}"
        final_https_url = https_status.get('final_url', https_url)
        print(f"Accessible via HTTPS: {final_https_url}")
        print(f"Code: {https_status['status_code']} {https_status['status_message']}")
        urls.append(final_https_url)

    return urls

def main():
    """Main function to check domains and write accessible ones to a file."""
    accessible_domains = set()  # Use a set to avoid duplicates

    # Read subdomains from file
    with open('all_subdomains.txt', 'r') as file:
        subdomains = [line.strip() for line in file if line.strip()]

    # Number of threads to use
    num_threads = 10  # Adjust as needed

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Map futures to subdomains
        future_to_domain = {executor.submit(check_accessibility, subdomain): subdomain for subdomain in subdomains}

        for future in as_completed(future_to_domain):
            domain, statuses = future.result()
            http_status = statuses.get('http', {'status_code': None})
            https_status = statuses.get('https', {'status_code': None})

            # Determine if either protocol is accessible
            urls = format_output(domain, http_status, https_status)
            if urls:
                accessible_domains.update(urls)  # Add URLs to the set

    # Write unique, sorted domains to a file
    with open('updomains.txt', 'w') as file:
        for url in sorted(accessible_domains):
            file.write(f"{url}\n")

if __name__ == "__main__":
    main()
