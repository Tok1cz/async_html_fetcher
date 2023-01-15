# asynch_html_fetcher
A simple program that fetches webpages from a list of urls and saves the results as html files.

## Disclaimer:
**The author relinquishes responsibility for all legal consequences that may arise for the users by running this program. Users should and must be aware of the terms of use of the websites they fetch and check, if their activity complies with the website's policies.**
Tested for Windows 11.
Use at own risk.

## Usage:

download the github folder

install the necessary libraries
especially httpx with async support 
('pip install httpx-socks[asyncio]')

Download the [tor client]
(https://www.torproject.org/download/tor/)

Add tor to path
press ```win+r```, type ```cmd``` - ```enter``` (open command line on windows) 
Type ```tor```
wait until >Bootstrapped 100%

run the method ```run_fetch(url_list)``` with a list containing strings of the desired urls


        
        run_fetch(url_list):
        
        Loads the webpages from links and saves them as html
        to ./htmls
        Returns:
        a list of html response objects.

        Variables: 

        links: A list of urls (strings) to fetch

        process_in_parallel: The number of links to 
        fetch and write in parallel - decrease this value if you get frequent SOCKS server failures, 
        increase for more speed

        write_to_files: default: True, if false the http response is only the return value of the
        method, but will not be written to a file.

        A Tor Daemon has to be running (Port 9050).
      
