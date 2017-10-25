from __future__ import print_function

import time       #Importing the time library to check the time of code execution
import sys    #Importing the System Library
import os

MAX_ATTEMPTS = 150

#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items


def google_image_scrape(search_keyword, parentDir, num_to_download,
                        savePrefix=""):
    ''' Search for a given keyword in google images and return
    a list of links '''
    t0 = time.time()   #start the timer
    
    #Download Image Links
    items = []
    print("Searching for {}...".format(search_keyword))
    print("Evaluating...")
    search = search_keyword.replace(' ','%20')

    url = 'https://www.google.com/search?q=' + search \
        + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&' \
        + 'tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

    print("URL: {}".format(url))

    raw_html = (download_page(url))
    time.sleep(0.1)
    items = items + (_images_get_all_items(raw_html))
    print("Total Image Links = {}".format(len(items)))
    print()

    t1 = time.time()    #stop the timer
    total_time = t1 - t0   #Calculating the total time required to crawl, find and download all the links of 60,000 images
    print("Total time taken: "+str(total_time)+" Seconds")
    print("Starting Download...")

    ## To save imges to the same directory
    # IN this saving process we are just skipping the URL if there is any error
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
    
    attempts = 0
    successes = 0
    errorCount = 0
    while successes < num_to_download and attempts < MAX_ATTEMPTS:
        # from urllib.request import Request,urlopen
        # from urllib.error import URLError, HTTPError
    
        try:
            req = Request(items[attempts], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req, None, 15)
            if savePrefix == "":
                filePath = os.path.join(parentDir, "{:04d}.jpg".format(successes))
            else:
                filePath = os.path.join(parentDir,
                                        "{}_{:04d}.jpg".format(savePrefix,
                                                               successes))
            output_file = open(filePath, 'wb')
                
            data = response.read()
            output_file.write(data)
            response.close();
    
            print("completed ====> {}".format(successes))
    
            successes += 1
            attempts += 1
    
        except:   #If there is any IOError
    
            errorCount += 1
            print("Error on image {}".format(attempts))
            attempts += 1

    print("\n")
    print("Everything downloaded!")
    print("\n"+str(errorCount)+" ----> total Errors")
