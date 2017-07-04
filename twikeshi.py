#-*- coding:utf-8 -*-
import auth
import tweepy
import csv
import time,sys

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

def try_delete(tweet_id):
	deleted = ""
	result = ""
	try:
		result = api.destroy_status(status_id)
	except tweepy.error.TweepError as e:
		deleted += str(e)
	if result != "":
		deleted += str(result)
		print("[ \033[32mSUCCESS\033[0m ]", "\r", end="")
		#if len(sys.argv) >= 2 and sys.argv[1] == "-v": print(deleted, "\r", end="")
		return True
	else:
		print("[ \033[31mFAILED\033[0m ]", end="")
		print(deleted, "\r", end="")
		return False

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

print("searching...")
print(src_start)
print(src_end)

delete_switch = False
delete_list = []
for row in csvreader:
	if row == src_end:
		delete_switch = True
	if delete_switch:
		status_id = row["tweet_id"]
		delete_list.append(status_id)
	if row == src_start:
		delete_switch = False

confirm = input("ok?(y or n)")
if confirm != "y":
	exit(0)
print("closing csv file...", end="")
csvfile.close()
print("[ \033[32mOK\033[0m ]")

start_time = time.time()

tried = 0
succeed = 0
for target in delete_list:
	print("["+str(tried)+"]trying...", end="")
	succeed += 1 if try_delete(target) else 0
	tried += 1

elapsed_time = time.time() - start_time

print(("elapsed_time:{0}".format(elapsed_time)) + "[sec]")
print("tried "+str(tried)+" tweets.")
print("complited "+str(succeed)+" tweets.")

