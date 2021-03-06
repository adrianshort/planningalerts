"""
Lichfield District council has no nice search page, but it does have a page
which has the applications received in the last 7 days, so we'll use this,
ignoring the date passed in.

"""

import urllib2
import urlparse
import re

import datetime

import BeautifulSoup

from PlanningUtils import PlanningApplication, \
    PlanningAuthorityResults, \
    getPostcodeFromText

date_format = "%d/%m/%Y"

date_received_re = re.compile("(\d\d?)[a-z]{2} ([a-zA-Z]*) (\d{4})")

class LichfieldParser:
    def __init__(self, *args):

        self.authority_name = "Lichfield District Council"
        self.authority_short_name = "Lichfield"
        self.base_url = "http://www.lichfielddc.gov.uk/site/scripts/planning_list.php"

        self._results = PlanningAuthorityResults(self.authority_name, self.authority_short_name)


    def getResultsByDayMonthYear(self, day, month, year):
        response = urllib2.urlopen(self.base_url)
        soup = BeautifulSoup.BeautifulSoup(response.read())

        trs = soup.find("table", {"class": "planningtable"}).tbody.findAll("tr")

        for tr in trs:
            application = PlanningApplication()

            tds = tr.findAll("td")

            application.council_reference = tds[0].a.string.strip()
            application.info_url = urlparse.urljoin(self.base_url, tds[0].a['href'])
            application.address = ' '.join(tds[1].contents[1].strip().split()[1:])
            application.postcode = getPostcodeFromText(application.address)


            # We're going to need to download the info page in order to get 
            # the comment link, the date received, and the description.

            info_response = urllib2.urlopen(application.info_url)
            info_soup = BeautifulSoup.BeautifulSoup(info_response.read())

            application.description = info_soup.find(text="Proposal").findNext(text=True).strip()
            date_received_str = info_soup.find(text="Date Application Valid").findNext(text=True).split(",")[1].strip()

            # This is a nasty botch, but the easiest way I can see to get a date out of this is to make another string and use strptime
            better_date_str = "%s %s %s" %date_received_re.match(date_received_str).groups()
            application.date_received = datetime.datetime.strptime(better_date_str, "%d %B %Y").date()
            application.comment_url = info_soup.find("a", title="Comment on this planning application.")['href']

            self._results.addApplication(application)

        return self._results

    def getResults(self, day, month, year):
        return self.getResultsByDayMonthYear(int(day), int(month), int(year)).displayXML()

if __name__ == '__main__':
    parser = LichfieldParser()
    print parser.getResults(20,11,2008)
