import requests
import json
import os
import sys
import time

endpt_search = "https://api.scryfall.com/cards/search"

delay = 0

def search_params(order, query):
    p = {}
    p["order"] = order
    p["q"] = "++e:" + query
    return p

def download_card(card, path, nameformat, quality, skip):
    downloaded = 0
    
    name = card["name"]
    multiface = "card_faces" in card

    if multiface:
        for face in card["card_faces"]:
            downloaded = downloaded + \
                         download_card(face, path, nameformat, quality, skip)
        return downloaded

    filename = nameformat % name
    filepath = os.path.join(path, filename + ".jpg")

    if not os.path.exists(filepath) or not skip:
        image_uris = card["image_uris"]
        r = requests.request("GET", image_uris[quality])
        img = open(filepath, "wb")
        img.write(r.content)
        img.close()
        print name + " downloaded..."
        return downloaded + 1
    else:
        print "Skipping " + name + "..."
        return downloaded
    

def sleep_millis(millis):
    time.sleep(millis / 1000.0)

def run(setabbr, nameformat, quality, skip, limit):
    outpath = os.path.relpath(setabbr)
    checklimit = limit > 0

    r = requests.request("GET", endpt_search, params=search_params("set", setabbr))
    if not r.ok:
        print "There was a problem getting cards. Is the set name correct?"
        return

    try:
        if not os.path.exists(outpath):
            os.makedirs(outpath)
    except OSError as ose:
        print ose
        return
    except IOError as ioe:
        print ioe
        return
    
    has_more = True
    next_page = None

    iterations = 0
    downloaded = 0

    while has_more:
        if next_page:
            r = requests.request("GET", next_page)

        if not r.ok:
            print "A request failed. Stopping download."
            return
        
        result_page = r.json()

        for card in result_page["data"]:
            downloaded += download_card(card, outpath, nameformat, quality, skip)
            if checklimit and downloaded >= limit:
                print "The set download limit of " + str(limit) + \
                      " was reached. Stopping download."
                return
        
        has_more = result_page["has_more"]
        if has_more:
            next_page = result_page["next_page"]

        iterations += 1
        print "--- End of page " + str(iterations) + " ---"
        #sleep_millis(delay)

    print "{} card(s) downloaded.".format(downloaded)
    print "Done."
