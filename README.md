# Domain Accessibility Checker

This Python tool checks the accessibility of a list of subdomains over HTTP and HTTPS protocols. It performs multi-threaded checks to efficiently handle a large number of domains and outputs the accessible domains to a file.
Features

    Multi-Threaded Processing: Uses ThreadPoolExecutor to perform domain checks concurrently, speeding up the process.
    Protocol Support: Checks both HTTP and HTTPS protocols to determine if a domain is accessible.
    Redirect Handling: Captures and reports redirects for HTTP and HTTPS URLs.
    Error Handling: Provides clear error messages for invalid domains and request issues.
    Output: Writes accessible domains to updomains.txt for easy reference.

# Requirements

    Python 3.x
    requests library

# You can install the requests library using pip:

    pip install requests

How It Works

    Domain Validation: Checks if each domain is in a valid format.
    Accessibility Check: Attempts to access each domain over HTTP and HTTPS.
    Results Formatting: Prints results for each domain, including status codes, redirect information, and final URLs.
    Output File: Saves the accessible domains to updomains.txt.

Usage

Prepare Your Subdomains: List your subdomains in a file named all_subdomains.txt, one per line.
Run the Tool: Execute the script to start checking domains.


    python domain_checker.py

Check Results: Review the updomains.txt file for a list of domains that are accessible over HTTP or HTTPS.

# Example Output
