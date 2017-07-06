# -*- coding:utf-8 -*-
import auth
import tweepy
import csv
import time,sys,argparse

# CMD args parser
parser = argparse.ArgumentParser(description="Deltete tweet from tweets\' csv.")
parser.add_argument("-v", "--verbose", \
		action="store_true", \
		default=False, \
		help="verbosity output.")
parser.add_argument("--protect-media",action="store_true",default=False ,help="protect media tweets from deleting.")

args = parser.parse_args()
PROTECT_MEDIA = args.protect_media
VERBOSE_MODE = args.verbose

# Method defenition


def searchByDate(csvreader, csvfile):
	point = []
	point_start = None
	while point_start is None:
		point = []
		datestr = input("Date?(YYYY-MM-DD):")
		timestr = input("Time?(hh:mm:ss):")
		query = datestr + " " + timestr + " +0000"
		for row in csvreader:
			if row["timestamp"] == query:
				point.append(row)
		print("result:" + str(len(point)))
		print(point)
		index = input("which one?(0-" + str(len(point)) + " or no to continue):")
		if index.isdigit() and 0 <= int(index) < len(point):
			point_start = point[int(index)]
		csvfile.seek(0)
	return point_start


def try_delete(tweet_id):
	deleted = ""
	result = ""
	try:
		status = api.get_status(tweet_id)
		if PROTECT_MEDIA and hasattr(status, "extended_entities"):
			print("[ \033[33mPROTECTED\033[0m ]", "\r")
			return False
		result = api.destroy_status(tweet_id)
	except tweepy.error.TweepError as e:
		deleted += str(e)
	if result != "":
		deleted += str(result)
		if VERBOSE_MODE:
			print("[ \033[32mSUCCESS\033[0m ]", end="")
			print(deleted, "\r", end="")
		else:
			print("[ \033[32mSUCCESS\033[0m ]", "\r", end="")
		return True
	else:
		print("[ \033[31mFAILED\033[0m ]", end="")
		print(deleted, "\r", end="")
		return False

# Main code

twiauth = auth.TwiAuth()
twiauth.authpass()
api = twiauth.api

filepath = input("Tell me tweet history file. :")
csvfile = open(filepath, "r")
csvreader = csv.DictReader(csvfile)

if csvfile is not None:
	print("successfly loaded.")

print("please setup start tweet.")
src_start = searchByDate(csvreader, csvfile)
print("next, please setup end tweet.")
src_end = searchByDate(csvreader, csvfile)

print("searching...")
# print(src_start)
# print(src_end)

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

print(str(len(delete_list)) + "tweets will be deleted(if it exists and non-protected).")
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
	if VERBOSE_MODE:
		print("status id: " + target)
	print("[" + str(tried) + "]trying...", end="")
	result = try_delete(target)
	if result:
		succeed += 1
	tried += 1

elapsed_time = time.time() - start_time

print(("elapsed_time:{0}".format(elapsed_time)) + "[sec]")
print("tried " + str(tried) + " tweets.")
print("complited " + str(succeed) + " tweets.")
