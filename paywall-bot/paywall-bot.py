#!/usr/bin/env python3

import requests
import praw
import urllib
import os


parseurl = "https://outlineapi.com/parse_article"

def getOutline(url):
	fullurl = "?".join((parseurl, urllib.parse.urlencode({"source_url": url})))
	r = requests.get(fullurl)
	if r.status_code != 200:
		raise Exception("Failed to parse article")
	output = r.json()
	if output["success"] != True:
		raise Exception("Failed to parse article")
	return "https://outline.com/%s" % output["data"]["short_code"]

reddit = praw.Reddit(client_id=os.environ["REDDIT_ID"],
                     client_secret=os.environ["REDDIT_SECRET"],
                     password=os.environ["REDDIT_PASSWORD"],
                     user_agent=os.environ["REDDIT_USER_AGENT"],
                     username=os.environ["REDDIT_USERNAME"])


def main():
	for comment in reddit.inbox.unread():
		print(comment)
		if isinstance(comment, praw.models.Comment):
			try:
				url = comment.submission.url
				outline = getOutline(url)
				comment.reply(outline)
				comment.mark_read()
			except e:
				print(repr(e))
		
if __name__ == "__main__":
	main()