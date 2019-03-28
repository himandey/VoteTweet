from bs4 import BeautifulSoup
import requests
from pprint import pprint

# get the list of votes page
voteReq = requests.get('http://www.legis.ga.gov/Legislation/en-US/VoteList.aspx?Chamber=2')
req = requests.get('http://www.legis.ga.gov/Legislation/en-US/Display/20192020/HB/290')

# parse
soup = BeautifulSoup(voteReq.content, 'html.parser')

# get all the divs in that stupid fucking "table" with no classes or ids
divs1 = soup.find_all('div', attrs={'style':'width:100%; background-color:#EEEFCE;'})
divs2 = soup.find_all('div', attrs={'style':'width:100%; background-color:#FFFFFF;'})
divs = divs1 + divs2

# filter for only the votes that passed or were adopted
divs = [list(div.children) for div in divs if 'ADOPT' in str(div) or 'PASSAGE' in str(div)]

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

# build bill data parse the actual vote page for relevant information
bills = {}

for link in voteLinks:
	billReq = requests.get(link)
	soup = BeautifulSoup(billReq.content, 'html.parser')

	linkDivs = soup.find_all('div', attrs={'class':'ggah1'})
	statusDivs = soup.find_all('div', attrs={'class':'ggah2'})
	
	# get hrefs
	# build data structure of bill, whether it passed, and the link to the bill summary
	for linky in linkDivs:
		aLink = list(linky.findChildren("a" , recursive=False))
		#pprint(aLink)
		if aLink != []:
			bills.update({aLink[0].get_text():{'billLink':'http://www.legis.ga.gov' + aLink[0]['href'],'votesLink':link}})
			for status in statusDivs:
				if status.get_text().lower() != '' and status.get_text().lower() != []:
					bills[aLink[0].get_text()].update({'status':status.get_text()})

# get each sublinks actual bill summary
for bill,nye in bills.iteritems():
	theScience = requests.get(nye.get('billLink'))
	soup = BeautifulSoup(theScience.content, 'html.parser')

	divs = soup.find_all('div', attrs={'class':'ggah1'})
	links = soup.find_all('a')

	senator = [palpalink.get_text() for palpalink in links if 'http://www.senate.ga.gov/senators' in str(palpalink)]

	bills[bill]['senatorSponsor'] = senator
	pprint(bills)



pprint(bills)