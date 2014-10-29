# Queries through YQL and parses data, will mainly focus on yahoo.finance for
# the wealth tool
# TODO
# implement caching to minimise requests
# clean up layout for easy use through the result of the application
# add further requests
# perhaps get the latest data / updated data
# historical information

import urllib
import json
import httplib

# API urls
PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
DATABASE_URL = 'store://datatables.org/alltableswithkeys'
# API Tables (mostly community tables)
YQL_TABLES = {'stocks': 'yahoo.finance.stocks',
              'xchange': 'yahoo.finance.xchange'}  # For currency exchange


def executeYQLQUERY(yql):
        conn = httplib.HTTPConnection('query.yahooapis.com')
        queryString = urllib.urlencode({'q': yql, 'format': 'json',
                                        'env': DATABASE_URL})
        conn.request('GET', PUBLIC_API_URL + '?' + queryString)
        return json.loads(conn.getresponse().read())


class QueryError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
            return repr(self.value)

print executeYQLQUERY("select * from %(xchange)s where pair in (\"EURUSD\",\"GBPUSD\")" % YQL_TABLES)
