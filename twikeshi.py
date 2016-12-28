#-*- coding:utf-8 -*-
import auth
import tweepy
import csv

def searchByDate(csvreader,csvfile):
	point = []
	point_start = None
	while point_start == None:
		point = []
		datestr = input("Date?(YYYY-MM-DD):")
		timestr = input("Time?(hh:mm:ss):")
		query = datestr+" "+timestr+" +0000"
		for row in csvreader:
			if row["timestamp"] == query:
				point.append(row)
		print("result:"+str(len(point)))
		print(point)
		index = input("which one?(0-"+str(len(point))+" or no to continue):")
		if index.isdigit() and 0 <= int(index) < len(point):
			point_start = point[int(index)]
		csvfile.seek(0)
	return point_start


twiauth = auth.TwiAuth()
twiauth.authpass()
api = twiauth.api

filepath = input("Tell me tweet history file. :")
csvfile = open(filepath,"r")
csvreader = csv.DictReader(csvfile)

if csvfile != None:
	print("successfly loaded.")

print("please setup start tweet.")
src_start = searchByDate(csvreader,csvfile)
print("next, please setup end tweet.")
src_end = searchByDate(csvreader,csvfile)

print(src_start)
print(src_end)
confirm = input("ok?(y or n)")
if confirm != "y":
	exit(0)
