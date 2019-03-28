# VoteTweet
This is a twitter bot that posts summaries of Georgia Legislation as they are voted on. Follow @VoteTweet for more information and voting day reminders!

# How it works
This script uses BeautifulSoup to scrape the webpage of the Georgia General Assembly, retreive the links to the bill, summary, and whether it passed or not. 
It returns a list of bill objects with the following data:

	u'SB 99': {'billLink': u'http://www.legis.ga.gov/Legislation/en-US/Display/20192020/SB/99',
	            'houseSponsors': [u'Smith, Vance 133rd'],
	            'senateSponsors': [u'Harper, Tyler 7th',
	                               u'Mullis, Jeff 53rd',
	                               u'Lucas, David 26th',
	                               u'Karinshak, Zahra 48th',
	                               u'Jones, Burt 25th',
	                               u'Brass, Matt 28th'],
	            'status': u'House Vote #230 (PASSAGE)',
	            'summary': u"2019-2020 Regular Session\xa0-\xa0SB\xa099Department of Natural Resources' Online Licensing System; allow applicants to make an anatomical gift; provide",
	            'votesLink': u'http://www.legis.ga.gov/Legislation/en-US/Vote.aspx?VoteID=16869'}

Then it formats that data and blasts out a tweet via Twitter API.

# Requirements
pip install BeautifulSoup
pip install requests