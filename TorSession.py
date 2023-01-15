import string
import random
import httpx
from httpx_socks import AsyncProxyTransport
import traceback


userAgents = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)","Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/5")

chars = tuple(string.ascii_letters) + tuple(range(10))

async def get_tor_session():
    """ Creating and returning a new Tor Session
    with an individual IP. 
    Is closing in Except block sufficient??
    """
    try:
        
        userAgent = random.choice(userAgents)
        header = {'User-Agent': userAgent}
        pwlst = random.choices(chars,k=random.randint(8,20))
        pw = "".join(str(x) for x in pwlst)

        # Tor uses the 9050 port as the default socks port
        creds = str(random.randint(10000,0x7fffffff)) + ":" + pw
        
        torport = 9050
        
        transport = AsyncProxyTransport.from_url("socks5://{}@localhost:{}".format(creds,torport))
        client = httpx.AsyncClient(transport=transport)
        client.headers = header
        return client 
        
    except Exception as e:
        await client.aclose() 
        
        traceback.print_exc()



    
