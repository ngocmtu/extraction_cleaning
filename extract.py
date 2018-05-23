#!/usr/bin/env python

import sys
import csv
import pandas as pd
from os import listdir
from os import rename
from os import path
from os import remove
from os import makedirs

d = sys.argv[1] # input dir

# method to find position of certain characters
def findnth(haystack, needle, n):
	n = n-1
	parts= haystack.split(needle, n+1)
	if len(parts)<=n+1:
		return -1
	return len(haystack)-len(parts[-1])-len(needle)

def shorten_name(original_name, current_dir):
	#find position of year
	#then get year to a var called year
	#if file name's already changed, then do nothing
	yeardelim = findnth(original_name,'2F',1)

	if yeardelim == -1:
		if path.exists(current_dir+'done/'+original_name[0:-4]+'_bull.csv'):
			return 'done'
		else:
			return current_dir+original_name
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
		return new_name

# loop through all files in a directory
# rename them to get rid of all redundant characters
# separate their contents into bull, bear, and no sentiment files
l = listdir(d)
done = d+'done/'
if not path.exists(done):
	makedirs(done)


for fr in l:
	try:
		fr = shorten_name(fr,d)
		if fr == 'done':
			continue

		# put file into a DataFrame for further processing
		df = pd.read_csv(d+fr)

		# get inputfile name without .csv extension
		input_name = fr[0:-4]

		# create name for the new output files
		fwbull = input_name + '_bull.csv'
		fwbear = input_name + '_bear.csv'
		fwnosen = input_name + '_nosen.csv'

		# read file and write to corresponding bull or bear file
		# if no sentiment attached, write to a file that's empty
		with open(path.join(done,fwbull),'w+') as write_bull, open(path.join(done,fwbear), 'w+') as write_bear, open(path.join(done,fwnosen), 'w+') as write_no_sentiment:
			# create csvwriter to write in csv format to output files
			csvwrite_bull = csv.writer(write_bull,dialect='excel')
			csvwrite_bear = csv.writer(write_bear,dialect='excel')
			csvwrite_no_sentiment = csv.writer(write_no_sentiment,dialect='excel')

			# write column names
			# no_sentiment file does not have sentiment so it does not have that column
			csvwrite_bull.writerow(['created_at','tweet', 'sentiment'])
			csvwrite_bear.writerow(['created_at','tweet', 'sentiment'])
			csvwrite_no_sentiment.writerow(['created_at','tweet'])

			# for every row in the original file
			# write to each of the corresponding 3 files
			for i in range(len(df)):
				row = df.loc[i,:]
				sen = row['entities_sentiment_basic']
				tweet = row['object_summary']
				time = row['object_postedTime']
				if sen == 'Bullish':
					csvwrite_bull.writerow([time,tweet,sen])
				elif sen == 'Bearish':
					csvwrite_bear.writerow([time,tweet,sen])
				else:
					csvwrite_no_sentiment.writerow([time,tweet])

		# remove original file after it has served its purpose
		# remove(d+fr)
	except Exception:
		print(Exception)
		print('File responsible for this '+fr)
		pass