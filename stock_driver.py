import requests
import datetime
import json

def generate_graph():
	print "[+] generating graph"

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


def main():
	get_volume_keyword_year("north korea")
	get_volume_keyword_month("north korea")


if __name__ == '__main__': main()
