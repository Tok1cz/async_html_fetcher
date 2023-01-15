#%%
import traceback
from datetime import date
import asyncio
from python_socks._errors import ProxyError
import os
import TorSession

# Set the current working directory to dir of the script
# This is important for saving the files
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Error_Tracker:
    errors = {}


async def get_pages(links:list,main_session, write_to_files:bool) -> list:
    """Asynchronously gathering and writing the pages from the link list to 
    html file (if write_to_files=True),
    returns list of html response objects (also None possible)
    needs a list of links and a Tor Session"""

    async def get_page(link:str,main_session) -> object:
        """Asynchronously executing an HTTP GET Request to a given link
        needs a Tor Session,
        returns a HTTP Response or None"""
        try:
            resp = await main_session.get(link,timeout=7)
        #Add proxy connection timeout exception handling here!

        except ProxyError as e:
            traceback.print_exc()
            msg = f"Proxy Error, Could not load {link}"
            print(msg)
            Error_Tracker.errors[link] = [e.with_traceback,msg]
            return None
        except Exception as e:
            traceback.print_exc()
            msg = f"Could not load {link}"
            print(msg)
            Error_Tracker.errors[link] = [e.with_traceback,msg]
            return None
        return resp

    responses=[]

    for link in links:
        resp = await get_page(link,main_session)
        responses.append(resp)


        #writing files
        if write_to_files:
            link_string = link
            # make the link writeable as filename
            replace_list = ["/",".","_","-",",","%","?","=",":",";","\\","&"]
            for to_replace in replace_list:
                link_string = link_string.replace(to_replace,"_")
            # avoid long strings
            # Shortening the url name to 60 symbols
            if len(link_string)>60:
                link_string = link_string[0:60]
            #write an empty file if no resp
            if resp == None:
                with open(rf"./htmls/empty_{link_string}_{date.today()}.html", "wb") as f:
                    f.write(b"<No data found>")
            #write response here
            else:
                try:
                    with open(rf"./htmls/{link_string}_{date.today()}.html", "wb") as f:
                        f.write(resp.content)
                    print(f"file {link_string}_{date.today()}.html written.")
                except IOError as e:
                    msg = f"Problem when writing files for {link}"
                    print(msg)
                    Error_Tracker.errors[link] =e.with_traceback,msg

    return responses
    



async def fetch(links:list, n_chunks:int, write_to_files:bool) -> list:
    """Internal function intialized by run_fetch
    Chunks the link list into even chunks (if not possible the last
    chunk will be smaller), than the elements of each chunk are
    processed in parallel"""


    def _chunks(lst:list, n:int):
        """Yield successive n-sized chunks from lst.
        Credit to Ned Batchelder from Stackoverflow"""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    
    # Chunk the list to sub lists of determined size - 4 works well for me

    chunked_link_list = _chunks(links,n_chunks)

    main_session = await TorSession.get_tor_session() 
    # Problem: 
    # If there are many requests to the same site, the site will block the current session
    # It is possible to create a new seesion for each chunk or even url, 
    # then the sessions have to be initialized in get_pages() or get_page
    try:
        responses = await asyncio.gather(*[get_pages(sub_link_list, main_session, write_to_files) for sub_link_list in chunked_link_list]) 

    except ProxyError as e:
        
        msg = f"Proxy Error: elements from {chunked_link_list} have not been fetched!!"
        print(msg)
        Error_Tracker.errors[str(chunked_link_list)] = e.with_traceback(),msg
        return  None
    finally:
        await main_session.aclose()
    
    return responses
    


def run_fetch(links:list,process_in_parallel=4, write_to_files=True) -> list:
        """NOTE 
        Loads the webpages from links and saves them as html
        to ./htmls
        Returns:
        a list of html response objects.

        Variables: 

        links: A list of links to fetch

        process_in_parallel: The number of links to 
        fetch and write in parallel - decrease this value if you get frequent SOCKS server failures, 
        increase for more speed

        write_to_files

        A Tor Daemon has to be running (Port 9050).
        """
    # If write_file = True Files are written in get_page
    # because the I/O work should happen inside the async loop

    # Create and start the eventloop
    fetch_loop = asyncio.get_event_loop()
    
    responses = fetch_loop.run_until_complete(fetch(links, process_in_parallel, write_to_files))
    responses_flat = []
    for list in responses:
        for sub_list in list:
            responses_flat.append(sub_list)
    # Log errors into txt file
    with open(rf"./error logs/error_log_{date.today()}.txt","w") as f:
        f.write(str(Error_Tracker.errors))

    return responses_flat