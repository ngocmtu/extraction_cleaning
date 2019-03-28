#!/usr/bin/env python
# Input and output folders are input on command line

import sys
import csv
from os import listdir,rename,path,remove,makedirs

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
		if '2008' in original_name:
			yeardelim = findnth(original_name,'2F',2)
			new_name = original_name[yeardelim+2:]
			rename(path.join('files_to_extract',original_name),path.join('files_to_extract',new_name))
			return new_name
		elif '2009' in original_name:
			new_name = original_name[yeardelim+2:]
			rename(path.join('files_to_extract',original_name),path.join('files_to_extract',new_name))
			return new_name
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
			rename(path.join('files_to_extract',original_name),path.join('files_to_extract',new_name))
			return new_name

# get the input and output destinations from user
input_path = raw_input('Please enter the input folder\n')
output_path = raw_input('Please enter output folder\n')

bear_path = path.join(output_path,'bear_extracted')
bull_path = path.join(output_path,'bull_extracted')
nosen_path = path.join(output_path,'nosen_extracted')

if not path.exists(nosen_path):
	makedirs(nosen_path)
if not path.exists(bull_path):
	makedirs(bull_path)
if not path.exists(bear_path):
	makedirs(bear_path)

# begin extraction of all files in input folder
print('input_path: '+input_path)
# line below throws error; refer to this resource: https://stackoverflow.com/questions/15725273/python-oserror-errno-2-no-such-file-or-directory
files_to_extract = listdir(input_path) # full path to input file
for f in files_to_extract:
	if f == '.keep':
		continue
	# if name already shorten, return the same name
	# if not, rename it to make it shorter
	print('Before '+f)
	f = shorten_name(f)
	print('After '+f)

	# get inputfile name without .csv extension
	input_name = f[0:-4]

	# create name for the new output files
	fwbull = input_name + '_bull.csv'
	fwbear = input_name + '_bear.csv'
	fwnosen = input_name + '_nosen.csv'

	# read file and write to corresponding bull or bear file
	# if no sentiment attached, write to a file that's empty
	with open(path.join(bull_path,fwbull),'w+') as write_bull, open(path.join(bear_path,fwbear), 'w+') as write_bear, open(path.join(nosen_path,fwnosen), 'w+') as write_no_sentiment, open(path.join(input_path,f),'r+') as read_file:
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
		headers = reader.fieldnames
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