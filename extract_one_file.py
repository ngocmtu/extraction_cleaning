#!/usr/bin/env python

import sys
import csv
import pandas as pd
from os import listdir,rename,path,remove,makedirs

f = sys.argv[1] # full path to input file

# method to find position of certain characters
def findnth(haystack, needle, n):
	n = n-1
	parts = haystack.split(needle, n+1)
	if len(parts)<=n+1:
		return -1
	return len(haystack)-len(parts[-1])-len(needle)

def shorten_name(original_name):
	#find position of year
	#then get year to a var called year
	#if file name's already changed, then do nothing
	path_name, original_name = path.split(original_name)
	yeardelim = findnth(original_name,'2F',1)

	if yeardelim == -1:
		return path.join(path_name,original_name)
	else:
		year = original_name[yeardelim+2:yeardelim+6]
		print('Year '+year)

		# get positions of month in name
		# usually between the last two '_' characters out of three '_' characters
		# if there's only two, count the length of name after the last '_'
		# if 17, get the first number after '_' as month
		# if 18, get the two numbers after '_' as month
		firstdelim = findnth(original_name,'_',2)
		seconddelim = findnth(original_name,'_',3)

		if seconddelim == -1:
			if len(original_name[firstdelim:-1]) == 17:
				month = original_name[firstdelim+1]
			else:
				month = original_name[firstdelim+1:firstdelim+3]
		else:
			month = original_name[firstdelim+1:seconddelim]

		new_name = year+'_'+month+'_'+original_name[-5]+'.csv'
		rename(current_dir+original_name,current_dir+new_name)
		return path.join(path_name,new_name)

# if name already shorten, return the same name
# if not, rename it to make it shorter
print('Before '+f)
fr = shorten_name(f)
print('After '+fr)

# put file into a DataFrame for further processing
df = pd.read_csv(fr)

# get inputfile name without .csv extension
input_name = f[0:-4]

# create name for the new output files
fwbull = input_name + '_bull.csv'
fwbear = input_name + '_bear.csv'
fwnosen = input_name + '_nosen.csv'

# print('Information about column name')
# created_at_column = raw_input('Created at datetime column name\n')
# tweet_column = raw_input('Tweet body column name\n')
# sentiment_column = raw_input('Sentiment column name\n')

# read file and write to corresponding bull or bear file
# if no sentiment attached, write to a file that's empty
with open(fwbull,'w+') as write_bull, open(fwbear, 'w+') as write_bear, open(fwnosen, 'w+') as write_no_sentiment, open(f,'r+') as read_file:
	# create csvwriter to write in csv format to output files
	csvwrite_bull = csv.writer(write_bull,dialect='excel')
	csvwrite_bear = csv.writer(write_bear,dialect='excel')
	csvwrite_no_sentiment = csv.writer(write_no_sentiment,dialect='excel')
	reader = csv.DictReader(read_file)

	# write column names
	# no_sentiment file does not have sentiment so it does not have that column
	csvwrite_bull.writerow(['created_at','tweet', 'sentiment'])
	csvwrite_bear.writerow(['created_at','tweet', 'sentiment'])
	csvwrite_no_sentiment.writerow(['created_at','tweet'])

	# get header info
	# files before 2011 has different header names
	headers = reader.
	if 'object_summary' in headers:
		tweet_column = 'object_summary'
	else:
		tweet_column = 'body'
	if 'entities_sentiment' in headers:
		sentiment_column = 'entities_sentiment'
	else:
		sentiment_column = 'entities_sentiment_basic'
	created_at_column = 'object_postedTime'

	current_tweet = ''

	for line in reader:
		tweet = line[tweet_column]

		if current_tweet != tweet or current_tweet == '':
			current_tweet = tweet
			sentiment = line[sentiment_column]
			created_at = line[created_at_column]

			if sentiment == 'Bullish':
				csvwrite_bull.writerow([created_at,tweet,sentiment])
			elif sentiment == 'Bearish':
				csvwrite_bear.writerow([created_at,tweet,sentiment])
			else:
				csvwrite_no_sentiment.writerow([created_at,tweet])
		else:
			continue

	print('Done')