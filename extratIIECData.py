# -*- coding: utf-8 -*-

import sys
import nltk
import json
from BeautifulSoup import BeautifulSoup
import re
# Load in output from blogs_and_nlp__get_feed.py

iiecweb = "http://iebc.or.ke/index.php/home/regional-offices"

#need this to mimic a real web browser
from urllib import FancyURLopener

class MyOpener(FancyURLopener): version = 'My new User-Agent'

MyOpener.version

class MyOpener(FancyURLopener): version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

myopener = MyOpener()
conn = myopener.open(iiecweb)
rawData = conn.read()
conn.close()

iiecSoup = BeautifulSoup(rawData)

#get infor about each constituency
rec3 = [sublink for link in iiecSoup.findAll("div", id = 'accordion_sp1_id88') for sublink in link.findAll("div", "sp-accordion-inner")]
iiecRegions = [sublink.getText() for link in iiecSoup.findAll("div", id = 'accordion_sp1_id88') for sublink in link.findAll("div", "toggler")]
#get text for emails
email = [[tag.getText() for tag in region.findAll('a', href = re.compile(r'.*mailto*'))] for region in rec3]

#getLinks for Constituences
const2 = [[tag.attrMap['href'] for tag in region.findAll('a', href = re.compile(r'.*index*'))] for region in rec3]
const1 = [tag.getText() for tag in region.findAll('a', href = re.compile(r'.*index*')) for region in rec3]

#parse text about employe
text = [region.findAll(text=True) for region in rec3]
text2= ["\n".join(values).lower().strip().split("\n") for values in text]
text2 = ["\n".join(values).split("constituencies")[0].strip() for values in text2]
text2 = [values.split("\n") for values in text2]

#Jank non-pythonic code
names =["NA"] * 17
regions = ["NA"] * 17
mobs = ["NA"] * 17
emails = ["NA"] * 17
fax = ["NA"] * 17
for i, s in enumerate(text2):
	for j,k in enumerate(text2[i]):
		print(i,j)
		if j == 0:
			if re.search(r'region', text2[i][j]):
				regions[i] = text2[i][j]
				print(text2[i][j])
				text2[i].pop(j)
		if re.search(r'person:', text2[i][j]):
			names[i] = re.split(r'person:', text2[i][j])[1]
			text2[i].pop(j)
		if re.search(r'mob:|tel:|tel.', text2[i][j]):
			mobs[i] = re.split(r'mob:|tel:|tel.', text2[i][j])[1]
			text2[i].pop(j)
		if re.search(r'fax:|fax.', text2[i][j]):
			fax[i] = re.split(r'fax:|fax.', text2[i][j])[1]
			text2[i].pop(j)
		if re.search(r'[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})', text2[i][j]):
			emails[i] = text2[i][j]
			text2[i].pop(j)

bio = [values[-1] for values in text2]
address = ["\n".join(values[0:-2]) for values in text2]


fields=[iiecRegions, names, mobs, emails, fax, address, bio]
fields= zip(*fields)

sys.path.append("/Volumes/Optibay-1TB/Python/scrapingCode/")
from  unicodeEncoder import UnicodeWriter

heading = "region", "name", "phone", "email", "fax", "addres", "bio"
			
import csv
outputFile = open('/Volumes/Optibay-1TB/Python/scrapingCode/regionalIIEC2012V2.csv','wb')
writer = UnicodeWriter(outputFile, delimiter = ",")
writer.writerow(heading)
for record in fields:
	print(record)
	writer.writerow(record)	
	

const3  = ["http://iebc.or.ke" + values for items in const2 for values in items]

myopener = MyOpener()

rawConstData =[]

import time
import random

for i,j in enumerate(const3):
	conn = myopener.open(const3[i])
	rawConstData.append(conn.read())
	print(rawData[i])
	time.sleep(random.randrange(1,10))
	conn.close()

import pickle
pickle.dump(rawConstData, open( "/Volumes/Optibay-1TB/Python/scrapingCode/constituency2012V2.p", "wb" ) )

soupCD = [BeautifulSoup(page) for page in rawConstData]

soupCD[1].findAll("h1","rt-article-title")

soupCD[1].getText()

outputFile.close()