import pandas as pd
import numpy as np
import csv
import pprint
import os
import urllib.request
import sys
import codecs

def percConvert(ser): return ser/float(ser[2])
from time import sleep
import time

import io

#with io.open(filename,'r',encoding='utf8') as f:
#    text = f.read()
# process Unicode text
#with io.open(filename,'w',encoding='utf8') as f:
#    f.write(text)

#################################################
#Reference: https://www.healthit.gov/providers-professionals/how-attain-meaningful-use
# Data used: Consumer_Complaints.csv| Converted applicable data to MedicareDecoded.csv
#################################################

#with open("data/Consumer_Complaints.csv", 'r') as csv_file:
#    csv_reader = csv.DictReader(csv_file)

with codecs.open("data/Consumer_Complaints.csv", 'r', encoding="cp1252", errors="surrogateescape") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('data/Posteriors/posterior_Consumer_Complaints.csv', 'w') as posterior_Consumer_Complaints:
        fieldnames=['Company response to consumer', 'Product', 'State', 'Consumer disputed?', 'Timely response?', 'Issue', 'Company']

        csv_writer = csv.DictWriter(posterior_Consumer_Complaints, fieldnames=fieldnames, delimiter=',') 
        
        csv_writer.writeheader()
        
        for line in csv_reader:
        	del line['Date received']
	#        del line['Product']
	        del line['Sub-product']
	#        del line['Issue']
	        del line['Sub-issue']
	        del line['Consumer complaint narrative']
	        del line['Company public response']
	#        del line['Company']
	#        del line['State']
	        del line['ZIP code']
	        del line['Tags']
	        del line['Consumer consent provided?']
	        del line['Submitted via']
	        del line['Date sent to company']
	#        del line['Company response to consumer']
	#        del line['Timely response?']
	#        del line['Consumer disputed?']
	        del line['Complaint ID']
	        csv_writer.writerow(line)


df = pd.read_csv('data/Posteriors/posterior_Consumer_Complaints.csv', low_memory=False)
#print(df)
##################################################
#input("#################### Press Enter to produce and view the revised dictionary generated data... ####################")
df.columns = ['Company_response', 'Product', 'State', 'Consumer_disputed', 'Timely_response', 'Issue', 'Company']
df1 = df
##################################################
df = pd.crosstab([df1.Company], [df1.Company_response], margins=True) 
df2 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Product], [df1.Company_response], margins=True) 
df3 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Consumer_disputed], [df1.Company_response], margins=True) 
df4 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Timely_response], [df1.Company_response], margins=True) 
df5 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Issue], [df1.Company_response], margins=True) 
df6 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Issue, df1.Consumer_disputed], [df1.Company_response], margins=True) 
df7 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Issue, df1.Consumer_disputed, df1.Timely_response], [df1.Company_response], margins=True) 
df8 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Product, df1.Issue, df1.Consumer_disputed, df1.Timely_response], [df1.Company_response], margins=True) 
df9 = df.div(df["All"], axis=0) 
##################################################
df = pd.crosstab([df1.Company, df1.Product, df1.Issue, df1.Consumer_disputed, df1.Timely_response], [df1.Company_response], margins=True) 
df10 = df.div(df["All"], axis=0) 
##################################################
writer = pd.ExcelWriter('data/Posteriors/posteriors_Consumer_Complaints.xlsx', engine='xlsxwriter')

df2.to_excel(writer, sheet_name='Tab 1')
df3.to_excel(writer, sheet_name='Tab 2')
df4.to_excel(writer, sheet_name='Tab 3')
df5.to_excel(writer, sheet_name='Tab 4')
df6.to_excel(writer, sheet_name='Tab 5')
df7.to_excel(writer, sheet_name='Tab 6')
df8.to_excel(writer, sheet_name='Tab 7')
df9.to_excel(writer, sheet_name='Tab 8')
df10.to_excel(writer, sheet_name='Tab 9')
writer.save()

time.sleep( 1 )

CD = pd.read_excel('data/Posteriors/posteriors_Consumer_Complaints.xlsx', sheet_name = 0)
print(CD)
#time.sleep( 1 )

os.remove('data/Posteriors/posterior_Consumer_Complaints.csv')