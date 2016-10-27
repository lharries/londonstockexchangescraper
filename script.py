#what the client described: 
#take in table, search for the company, return top website result, open fundamentals page, 
#get profit after tax, Earnings per Share - Basic, Total Assets, Total Liabilities, Total Equity 

import requests, os, bs4, webbrowser, sys, csv

#this fixes encoding issue for printing to file
reload(sys)
sys.setdefaultencoding('utf-8')

# open output file
f = open('output.html', 'w')

#empty array which will contain the list of companies
companies = []

#import list of companies into the array companies
def getCompanies():
	with open("companies-list.csv",'rb') as csvfile:
		companiesList = csv.reader(csvfile)
		for row in companiesList:
			companies.append(row[0])



#import file
getCompanies()

#turn the output file into html
print >>f, "<htm><body>"

#searches the website and returns the specific company code
def getCompanyLinkCode(desiredCompany):
	searchUrl = "http://www.londonstockexchange.com/exchange/searchengine/search.html?lang=en&x=0&y=0&q="
	res = requests.get(searchUrl + desiredCompany)
	companyUrl = bs4.BeautifulSoup(res.text, "html.parser")
	table = companyUrl.select('.table_dati')
	firstLine = table[0].select('.odd')

	names = firstLine[0].select('.name')

	companyLinkA =  names[1].select('a')
	companyLinkURL = companyLinkA[0].attrs['href']

	companyLinkURL = companyLinkURL[-34:]
	companyLinkCode = companyLinkURL[:21]
	return companyLinkCode

#uses the company link code to extract the desired rows
#desired rows are farily messily hard code
def getDesiredRowData(companyLinkCode):
	fundamentalsPage = "http://www.londonstockexchange.com/exchange/prices/stocks/summary/fundamentals.html?fourWayKey="
	#webbrowser.open(fundamentalsPage)

	res = requests.get(fundamentalsPage + companyLinkCode)
	companyUrl = bs4.BeautifulSoup(res.text, "html.parser")
	companyTable = companyUrl.select('.table_dati')
	companyRows = []

	for tables in companyTable :
		tableRows = tables.findAll('tr')
		for row in tableRows :
			companyRows.append(row)

	desiredRows = [0,6,15,42,59,71]

	desiredCompanyData = []
	for i in desiredRows:
		desiredCompanyData.append(companyRows[i])
	return desiredCompanyData

#prints the company name followed by the rows
def printDesiredCompanyDataToHTMLFile(desiredCompany,desiredCompanyData) :
	print >>f, "<table>"
	print >>f, "<h1>"+ desiredCompany + "</h1>"
	for i in desiredCompanyData:
		print >>f, i
	print >>f, "</table>"


for desiredCompany in companies:
	try:
		print desiredCompany
		companyLinkCode = getCompanyLinkCode(desiredCompany)
		desiredCompanyData = getDesiredRowData(companyLinkCode) 
		printDesiredCompanyDataToHTMLFile(desiredCompany,desiredCompanyData)
	except (RuntimeError, TypeError, NameError, IndexError):
		print "the above company didn't work"
		print >>f, "<h1>"+ desiredCompany + "did not work" "</h1>"


print >>f, "</body></html>"






