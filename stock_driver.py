import requests
import datetime
import json
import pandas as pd
import xlsxwriter
import sys
import os
import string

class Stock_Data:
	def __init__(self, stock):
		self.Ticker = stock
		self.data = ""
		self.dates = []
		self.score = []



	#Loads Stock Data
	def load_data(self,data):
		for d in data:
			try:
				date = d.split(",")[0]
				count = d.split(",")[1]

				self.dates.append(date)
				self.score.append(str(count))
				print date + " ==> " + str(count)
			except: pass
	def create_file(self):


		WorkBookName = self.Ticker + "_GoogleTrendsData.xlsx"

		#Pandas writing objects
		self.workbook = xlsxwriter.Workbook(WorkBookName)
		self.worksheet = self.workbook.add_worksheet()
		self.worksheet.set_column('A:A', 20)
		self.worksheet.set_column('B:B', 20)
		row = 0
		col = 0
		i = 0
		while i < len(self.dates):
			self.worksheet.write(row, col, self.dates[i])
			self.worksheet.write(row, col+1,self.score[i])
			i = i+1
			row+=1
		self.workbook.close()



def get_volume_keyword_year(keyword):
	""" use google trends to get volume search for keyword """
	print "[+] getting volume for keyword " + keyword + " for last year"
	url = 'https://trends.google.com/trends/api/explore?hl=fr&tz=-60&req={"comparisonItem":[{"keyword":"'+ keyword +'","geo":"","time":"today+12-m",}],"category":0,"property":""}&tz=-60'
	r = requests.get(url)
	widget = json.loads(r.text.split("'")[1])['widgets'][0]
	token = widget['token']
	time = widget['request']['time']
	url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv?req={"time":"'+ time +'","resolution":"WEEK","locale":"fr","comparisonItem":[{"geo":{},"complexKeywordsRestriction":{"keyword":[{"type":"BROAD","value":"'+keyword+'"}]}}],"requestOptions":{"property":"","backend":"IZG","category":0}}&token='+ token +'&tz=-60'
	r = requests.get(url)

	if r.status_code == 200:
		data = r.text.split("\n")[3:-1]
		for d in data:
			try:
				date = d.split(",")[0]
				count = d.split(",")[1]

				print date + " ==> " + str(count)
			except: pass
		return data
	else: print "[+] error with token"


def get_volume_keyword_month(keyword):
	""" use google trends to get volume search for keyword """
	print "[+] getting volume for keyword " + keyword + " for last month"
	url = 'https://trends.google.com/trends/api/explore?hl=fr&tz=-60&req={"comparisonItem":[{"keyword":"'+ keyword +'","geo":"","time":"today+1-m",}],"category":0,"property":""}&tz=-60'
	r = requests.get(url)
	widget = json.loads(r.text.split("'")[1])['widgets'][0]
	token = widget['token']
	time = widget['request']['time']
	url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv?req={"time":"'+ time +'","resolution":"DAY","locale":"fr","comparisonItem":[{"geo":{},"complexKeywordsRestriction":{"keyword":[{"type":"BROAD","value":"'+keyword+'"}]}}],"requestOptions":{"property":"","backend":"IZG","category":0}}&token='+ token +'&tz=-60'
	r = requests.get(url)
	if r.status_code == 200:
		data = r.text.split("\n")[3:-1]
		for d in data:
			try:
				date = d.split(",")[0]
				count = d.split(",")[1]
				print date + " ==> " + str(count)
			except: pass
	else: print "[+] error with token"


df = pd.read_excel('Tickers.xlsx')
location = os.getcwd()
Tickers = df['TICKER']

#List to hold stock objects
Stock_metadata = []


for Tick in Tickers:
	Output = Stock_Data(Tick)
	Output.load_data(get_volume_keyword_year(Output.Ticker))
	Output.create_file()




#Data.load_data()
