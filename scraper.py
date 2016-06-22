#importing libraries

from bs4 import BeautifulSoup
import urllib2
import lxml
import csv
import re

#taken from StackOverFlow: http://stackoverflow.com/questions/31137552/unicodeencodeerror-ascii-codec-cant-encode-character-at-special-name
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

majOpinionFile = open("testFile.txt", "w")
docketNumbersNotAccessed = open("test-cases-not-accessed.txt", "w")

TAG_RE = re.compile(r'<[^>]+>')

#code taken from Stack Overflow: http://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def remove_tags(text):
    return TAG_RE.sub('', text)


#from stackoverflow: https://gist.github.com/dehowell/884204
def file_exists(location):
    request = urllib2.Request(location)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except urllib2.HTTPError:
        return False

docketNumber = ""
#url = 'http://caselaw.findlaw.com/us-supreme-court/'
opinionWriter = '105'

ifStatementAccessed = False 

num = 0

with open('testFileCourtCases.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		temp = (row['majOpinWriter'])
		temp = temp.__str__()
		#print "I'm at the first part of the loop"
		if temp == opinionWriter:
			#tempTwo = (row['docket'])
		    docketNumber = (row['docket']).__str__()
		    url = 'http://caselaw.findlaw.com/us-supreme-court/'
		    url += docketNumber
		    url += '.html'
		    ifStatementAccessed = True
		    #print "I'm here"
		    if file_exists(url) != True:
		    	num = num+1
		    	print docketNumber
		    	print num.__str__()
		    	docketNumbersNotAccessed.write(docketNumber)
		    	docketNumbersNotAccessed.write(" , Name of case: ")
		    	docketNumbersNotAccessed.write(row['caseName'])
		    	docketNumbersNotAccessed.write(" , Year: ")
		    	docketNumbersNotAccessed.write(row['term'])
		    	docketNumbersNotAccessed.write(" , Number: ")
		    	docketNumbersNotAccessed.write(num.__str__())
		    	docketNumbersNotAccessed.write("\n")
		else: 
			ifStatementAccessed = False
			#break;

		#if ifStatementAccessed == True and file_exists(url) == False:
			#docketNumbersNotAccessed.write(docketNumber)

		if ifStatementAccessed == True and file_exists(url) == True and docketNumber != '06-1195':
			print(url)


			page = urllib2.urlopen(url)



			soup = BeautifulSoup(page.read(), "lxml")

			print soup.find("a", {"name":"opinion1"})

			print soup.find("p", string="It is so ordered.")
			print soup.find("p", string="Affirmed.")
			print soup.find("p", string="Reversed.")

			tag = soup.find("a",{"name": "opinion1"})

			print tag

			tempTag = tag.__str__()

			if tempTag == 'None':
				print "trying to change tag"
				tag = soup.find("p", string="Opinion of the Court")

			print tag

			tempTag = tag.__str__()

			stringToLookFor = "No. "
			stringToLookFor += docketNumber

			if tempTag == 'None':
				print "trying to change tag again"
				tag = soup.find("p", string=stringToLookFor)
			print tag 


			stopOne = soup.find("p", string="It is so ordered.")
			stopTwo = soup.find("p", string="Affirmed.")
			stopThree = soup.find("p", string="Reversed.")

			#you will probably have to delete this one
			#this didn't work--fix for Scalia
			#if stopOne.__str__() == 'None':
			#	print "trying to change stopOne"
			#	stopOne = soup.find("em", string=".")

			#will need to run tests on this to make sure it usually does not capture the dissents and concurrences

			if stopOne.__str__() == 'None':
				print "trying to change stopOne"
				stopOne = soup.find("p", string="Nos. 14-46, 14-47, and 14-49")

			if stopOne.__str__() == 'None':
				print "trying to change stopOne"
				stopOne = soup.find("h2", string="FOOTNOTES")

			print stopOne
			print stopTwo
			print stopThree


			for majOpinion in tag.next_siblings:
				if (majOpinion == stopOne or majOpinion == stopTwo or majOpinion == stopThree):
					break
				#print majOpinion.encode()
				#stuff = remove_tags(majOpinion.__str__())
				stuff = remove_tags(majOpinion.encode())
				majOpinionFile.write(stuff)


