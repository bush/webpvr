#!/usr/bin/python

import urllib2
import re
import sys, os, errno
import feedparser
from subprocess import call

DEBUG = 0 

# Unused, replaced with the feedparser module
def get_torrent_url(feedurl):
  response = urllib2.urlopen(feedurl)
  html = response.read()
  
  # Find the first line that matches the type and ID we're looking for 
  for line in html.splitlines():
    if re.search('XviD',line) and re.search('ettv',line):
      match = re.search('<enclosure url="([^"]*)"',line)
      torrenturl = match.groups()[0]
      break

  # Pull to torrent url out of the feed
  match = re.search('\/([^\/]*\.torrent)',torrenturl) 
  if match:
    torrentfn = match.groups()[0]
    return torrentfn
  else:
    return "none"

# Unused
def download_torrent(url):
  response = urllib2.urlopen(torrent_url)
  html = response.read()
  full_torrent_fn = os.path.join(path,'lastest.torrent')
  f = open(os.path.join(path,full_torrent_fn),'w')
  f.write(html)
  f.close


def read_rss_feed(url,encoding,signature):
  # Extract the torrent url
  feed = feedparser.parse(url)

  #if feed.bozo:
  #  print "There is something wrong with this feed.  Maybe the site is down ..."
  #  print feed.bozo
  #  return feed.bozo    

  for item in feed["items"]:  

    torrent_url = item['links'][1]['href']

    if re.search(encoding,torrent_url) and re.search(signature,torrent_url):
      if DEBUG:
        print "Found torrent: %s" % torrent_url
      return torrent_url 

  return "none" 

def read_html_feed(url,encoding,signature):
  
  response = urllib2.urlopen(url)
  html = response.read()
  list = re.findall(r'href="(magnet:[^"]*)"',html)
  for item in list:
    if re.search(encoding,item) and re.search(signature,item):
      return item
  return "none"

def main():
 
  # TODO: Add all failure paths
  TVDIR = "/media/windowsshare/downloads/completed/TV"
  FEEDS = [
      {'type': 'rss', 'show': 'Modern Family', 'encoding': 'XviD', 'signature': 'ettv', 'url': 'http://extratorrent.cc/rss.xml?type=last&cid=632'},
      {'type': 'html', 'show': 'The Big Bang Theory', 'encoding': 'x264', 'signature': 'LOL', 'url': 'https://thepiratebay.se/search/the%20big%20bang%20theory/0/7/0'},
      #{'type': 'html', 'show': 'The Big Bang Theory', 'encoding': 'x264', 'signature': 'eztv', 'url': 'http://eztv.it/shows/23/the-big-bang-theory/'},
      ]

  for feed_entry in FEEDS:
  
    torrent_url = "none"

    if feed_entry['type'] == "rss":
      if DEBUG:
        print "Processing rss feed ..."
      torrent_url = read_rss_feed(feed_entry['url'],feed_entry['encoding'],feed_entry['signature'])
    elif feed_entry['type'] == "html":
      if DEBUG:
        print "Processing html feed ..."
      torrent_url = read_html_feed(feed_entry['url'],feed_entry['encoding'],feed_entry['signature'])

    if torrent_url == "none":
      if DEBUG:
        print "No matching torrent found"
      continue

    # Create the torrent directory if it does not exist
    path = os.path.join(TVDIR,feed_entry['show'])
    try:
      os.makedirs(path)
    except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST and os.path.isdir(path):
        pass
      else: raise
    
    # Touch the history file
    history_fn = os.path.join(TVDIR,'history')
    f = open(history_fn, 'a+')

    # Move on if we already downloaded the torrent file
    if torrent_url in f.read():
      if DEBUG:
        print "We already got this one, moving on ..."
      continue

    cmd = ['transmission-remote','-w',path,'-a',torrent_url]

    try:
      devnull = open('/dev/null', 'w')
      if DEBUG:
        print "Adding torrent %s" % torrent_url
      retcode = call(cmd,stdout=devnull, stderr=devnull)
      f.write("%s\n" % torrent_url)
      f.close
      devnull.close
    except OSError, msg:
      quit("Could not execute the above command: %s\n" % cmd)

  

if __name__ == "__main__":
    main()
