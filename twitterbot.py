from bs4 import BeautifulSoup
import requests
from pprint import pprint

# python requirements: pip install BeautifulSoup
#					   pip install requests

# get the list of votes page
voteReq = requests.get('http://www.legis.ga.gov/Legislation/en-US/VoteList.aspx?Chamber=2')

# parse
soup = BeautifulSoup(voteReq.content, 'html.parser')

# get all the divs in that stupid fucking "table" with no classes or ids
divs1 = soup.find_all('div', attrs={'style':'width:100%; background-color:#EEEFCE;'})
divs2 = soup.find_all('div', attrs={'style':'width:100%; background-color:#FFFFFF;'})
divs = divs1 + divs2
print "Found all voting record divs"

# filter for only the votes that passed or were adopted
divs = [list(div.children) for div in divs if 'ADOPT' in str(div) or 'PASSAGE' in str(div)]

# get latest divs date and filter
latest_date = str(divs[-1][1].get_text());
divs = [div for div in divs if latest_date in str(div)]

# grab links for each
links = []
for div in divs:
	#pprint(div)
	# try to get the spans first a child, if it fails move on
	for span in div:
		#pprint(span)
		try:
			theAlmightyAlphaLink = span.findChildren("a" , recursive=False)
			if theAlmightyAlphaLink != []:
				links.append(theAlmightyAlphaLink)
		except:
			continue

# get the final link to the page
voteLinks = ['http://www.legis.ga.gov'+link[0]['href'] for link in links if '/Legislation/en-US/Vote' in str(link)]
print "Scraped all bill votes links"
# build bill data parse the actual vote page for relevant information
bills = {}

for link in voteLinks:
	billReq = requests.get(link)
	soup = BeautifulSoup(billReq.content, 'html.parser')

	linkDivs = soup.find_all('div', attrs={'class':'ggah1'})
	statusDivs = soup.find_all('div', attrs={'class':'ggah2'})

	try:
		yayDiv = soup.select('span.voteheader.voteY')[0]
		nayDiv = soup.select('span.voteheader.voteN')[0]
		yayNums = int(yayDiv.get_text().split(':')[1])
		nayNums = int(nayDiv.get_text().split(':')[1])
	except:
		continue

	print "YAYNUMS",yayNums
	print "NAYNUMS",nayNums
	# get hrefs
	# build data structure of bill, whether it passed, and the link to the bill summary
	for linky in linkDivs:
		aLink = list(linky.findChildren("a" , recursive=False))
		#pprint(aLink)
		if aLink != []:
			billTitle = aLink[0].get_text()
			passed = None
			if yayNums > nayNums:
				passed = True
			else:
				passed = False
			bills.update({billTitle:{'billLink':'http://www.legis.ga.gov' + aLink[0]['href'],'votesLink':link,'yays':yayNums,'nays':nayNums,'passed':passed}})
			for status in statusDivs:
				if status.get_text().lower() != '' and status.get_text().lower() != []:
					bills[billTitle].update({'status':status.get_text()})

print "Found all bill links and statuses"

# get each sublinks actual bill summary
for bill,nye in bills.iteritems():
	theScience = requests.get(nye.get('billLink'))
	soup = BeautifulSoup(theScience.content, 'html.parser')

	summaryDiv = soup.find_all('div', attrs={'class':'ggah1'})[0].get_text()
	links = soup.find_all('a')

	#scrape all sponsors and grab the summaryu (ggah1)
	try:
		senators = [palpalink.get_text() for palpalink in links if 'senate.ga.gov/senators' in str(palpalink)]
		houseReps = [hugh.get_text() for hugh in links if 'house.ga.gov/representatives' in str(hugh)]
	except Exception as e:
		print "here's what exploded:", pprint(e)

	bills[bill]['senateSponsors'] = senators
	bills[bill]['houseSponsors'] = houseReps
	bills[bill]['summary'] = summaryDiv 
	#pprint(bills)

print "Found all bill summaries and sponsors"

pprint(bills)