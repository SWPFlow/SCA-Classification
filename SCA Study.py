# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 08:10:06 2017

@author: Chris.Cirelli
"""

#   SCA LAWSUIT STUDY

#   Objectives:
#1. Understand the strucrture of each lawsuit to determine if they are uniform. 
#2. See if we can identify and isolate the allegations for each lawsuit. 
#3. See if we can identify and isolate the aspect of the law they are relying on. 
#4. Pass the allegation and law to a dictionary with the keys being the names of the company, statute, allegations. So nested. 


#   Step1: Load Libraries
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import PyPDF2 as pdf
import numpy as np


#   Step2: Import File & Extract Text
File = 'C:\\Users\\Chris.Cirelli\\Desktop\\Python Programing Docs\\DataFiles Misc\\SCA Docs\\201788_f01c_17CV02127.pdf'
File2 = pdf.PdfFileReader(File)
File3 = File2.getPage(0)
Text = File3.extractText()

#   Step3: Pass text to list & tokenize w/ punctuation
x = File2.getNumPages()
List = []

for page in range(0, x):
    content = File2.getPage(page).extractText().split("\n")
    content_tokenized = str(content)
    List.append(content_tokenized)

text_wpunc0 = nltk.word_tokenize(str(List))
text_wpunc = nltk.Text(text_wpunc0)

#   Step4: Tokenize text with without punctuation
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
text_nopunc = tokenizer.tokenize(str(List)) #use this set for when the word reference does not work well withou the punctuation. 
text_nltk = nltk.Text(text_nopunc)

#string = 'STRING'
#print(string.lower())


#   Step5: Identify Ticker Symbol

symbol_loc = text_nltk.index('symbol') + 1
ticker_location = text_nltk[symbol_loc]
ticker = ''.join([c for c in ticker_location if c.isupper()])

#   Identify Court

Court_location = text_nltk.index('DISTRICT')
Court_upper = Court_location + 7
Court_raw = text_nltk[Court_location:Court_upper]

List_court = []
for x in Court_raw:
    if x != 'DISTRICT':
        if x != 'FOR':
            if x != 'COURT':
                if x != 'THE':
                    if x != 'OF':
                        List_court.append(x)
court = List_court

#   Step7: Identify Defendant

location_inc = text_wpunc.index('Inc.') + 1
low_inc = location_inc - 4
defendant_location = text_wpunc[low_inc:location_inc]

List_defendant = []
for x in defendant_location:
    if x != ',':
        List_defendant.append(x)
defendant = List_defendant


#   Identify Plaintiff

location_plaintiff = text_nltk.index('hereby')
high = location_plaintiff + (-1)
low = location_plaintiff - 3
plaintiff = text_nltk[low:high]

#   Define Type of Lawsuit

Type = {
        'IPO': ['Initial Public Offering', 'Offering', 'IPO', '1933', 'Prospectus'], 
        '10B5': ['1934'],
        'M&A': ['Merger', 'Acquisition', 'Transaction', 'Proxy'], 
        'Bankruptcy':['Chapter 11', 'Bankruptcy', 'Restructure', 'Restructuring', 'Chapter 7'],
        'NonUS': ['Foreign', 'Non-US', 'Non US'], 
        '10B5': ['10B5',  '10B-5', 'material', 'misrepresentation', 'misrep']
        }

List_details = []
for x in Type:
    for y in Type[x]:
        count = text_nltk.count(y)
        List_details.append([x, y, count])

Df1 = pd.DataFrame(List_details)
#print(Df1)

#   Alaternative - Use Dictionary to aggregate values by key.  Then if the reader wants they can use Df to view sub values. 

List_characteristics = []
for x in Type:
    for y in Type[x]:
        count = text_nltk.count(y)
        List_characteristics.append([x, count])

Dict_keys = dict(List_characteristics)
#print(Dict_keys)


#   Identify Sections of Securities Law

list_section = []
currentIndex = 0
for x in text_nltk:
  if x == 'Section':
    list_section.append(currentIndex)
  currentIndex += 1

list_securitieslaws = []
for x in list_section:
    y = text_nltk[x:x+6]
    list_securitieslaws.append(y)
#print(list_securitieslaws)


######   OUTPUT ###########################


D = {'Defendant: ': [defendant], 'Ticker: ': [ticker], 'Plaintiff:' : [plaintiff], 'Court: ': [court]}
Df = pd.DataFrame(D)
print(Df)
print(Dict_keys)
print(list_securitieslaws)
        











       
        


