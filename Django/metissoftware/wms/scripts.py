
import urllib.request as urlrequest
import urllib.parse as urlparse
import json
import datetime
__author__ = 'Calum'


def query_api(yql_query):
    BASE_URL = "https://query.yahooapis.com/v1/public/yql?"
    CALLBACK = "http://www.metissoftware.co.uk"
    ENV = "store://datatables.org/alltableswithkeys"
    yql_url = BASE_URL + urlparse.urlencode({'q':yql_query, 'env': ENV})  + "&format=json"

    result = urlrequest.urlopen(yql_url).read()
    response = json.loads(result.decode('utf8'))
    return response
