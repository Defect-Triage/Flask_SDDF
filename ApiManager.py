import requests
import json
import selenium
from selenium import webdriver
import pickle
from datetime import datetime


def authenticate():
    """Authenticates the application and generates a Sessionid that will later be needed for requests"""
    with open('config.txt', 'rb') as f:
        d = pickle.load(f)
    timestamp = d['time']

    currenttime = datetime.now()
    delta = currenttime-timestamp
    delta_in_s = int(delta.total_seconds())

    if delta_in_s > 23400:  # 23400 seconds = approx. 6.5 hours (session is valid for 7 hours)


        url = "https://session-manager-prod.starc.i.mercedes-benz.com/auth"     # set url for the request
        # set the payload
        payload = json.dumps({
            "application_id": "e0aa617c-3b46-47c9-873e-9d37443fa7e0",
            "application_token": "NzhjYWZlNjEtMDliNS00M2Q2LThiYTYtOGI0YmRhY2YzNjdi",
            "client_type": "fat,web"
        })
        # set the headers
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # make the request
        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
        # print(response.headers['Location'])
        auth_url = response.headers.get('location')
        # start web browser
        browser = selenium.webdriver.Edge()

        # get source code
        # browser.get("https://session-manager-prod.starc.i.mercedes-benz.com/confirmed")
        browser.get(auth_url)

        waiting = True

        while waiting:

            # check that user has provided pingID successfully
            if "confirmed" in browser.current_url:
                waiting = False

        # get complete page source as html
        pageSoure = browser.page_source

        # extract the SessionId from the page source html
        sessionid = pageSoure[39:-16]
        # get current timestamp for later comparison
        if sessionid:
            time = datetime.now()
            # print(sessionId)
            # open config file to save session and timestamp
            d = {'sessionid': sessionid, 'time': time}
            with open('config.txt', 'wb') as f:
                pickle.dump(d, f)

        # close web browser
        browser.close()
    else:
        sessionid = d['sessionid']  #take the old sessionid if it is still valid

    return sessionid


def getdatabyquery(sessionid, pagesize, page, querystring):
    """makes a get request to the starc api based on a CBQL query like in the reports menu on starc
    :param sessionid: str
    id needed to signal the api that the call is authenticated
    :param pagesize: str
    sets the size of the amount of defects that os wanted
    :param page: str
    sets the page number that is wanted
    :param querystring: str
    includes the cbql query
    :return: requests.response
    returns the response that comes back from the starc API
    """
    # define the look of the request url
    url = "https://session-manager-prod.starc.i.mercedes-benz.com/starc/v3/items/query?baselineId=&page=" + page + "&pageSize=" + pagesize + "&queryString=" + querystring
    # no payload
    payload = {}
    # define headers
    headers = {
        'Accept': 'application/json',
        'STARC_SESSION': sessionid
    }
    # send request
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

