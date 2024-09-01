import requests
from requests.exceptions import RequestException
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def check_accessibility(domain):
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
