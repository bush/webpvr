#!/usr/bin/python

import urllib2
import re
import sys, os, errno
import feedparser
from subprocess import call

DEBUG = 1 
TVDIR = "/media/windowsshare/downloads/completed/TV"
FEEDS = [
    #{'type': 'rss', 'show': 'Modern Family', 'encoding': 'XviD', 'signature': 'ettv', 'url': 'http://extratorrent.cc/rss.xml?type=last&cid=632', 'limit': 3},
      {'type': 'html', 'show': 'The Big Bang Theory', 'encoding': 'x264', 'signature': 'LOL', 'url': 'https://thepiratebay.se/search/the%20big%20bang%20theory/0/7/0', 'limit': 3},
      #{'type': 'html', 'show': 'The Big Bang Theory', 'encoding': 'x264', 'signature': 'eztv', 'url': 'http://eztv.it/shows/23/the-big-bang-theory/'},
      ]

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

def add_from_rss_feed(path,url,encoding,signature,limit):
  # Extract the torrent url
  feed = feedparser.parse(url)

  #if feed.bozo:
  #  print "There is something wrong with this feed.  Maybe the site is down ..."
  #  print feed.bozo
  #  return feed.bozo    
  mylimit = 0

  for item in feed["items"]:  

    torrent_url = item['links'][1]['href']
    if re.search(encoding,torrent_url) and re.search(signature,torrent_url) and mylimit < limit:
      mylimit += 1
      add_torrent(path,torrent_url)


def add_from_html_feed(path,url,encoding,signature,limit):
  
  response = urllib2.urlopen(url)
  html = response.read()
  list = re.findall(r'href="(magnet:[^"]*)"',html)
  mylimit = 0
  for item in list:
    if re.search(encoding,item) and re.search(signature,item) and mylimit < limit:
      mylimit += 1
      add_torrent(path,item)

def add_torrent(path,torrent_url):

  # Touch the history file
  history_fn = os.path.join(TVDIR,'history')
  f = open(history_fn, 'a+')

  # Move on if we already downloaded the torrent file
  if torrent_url in f.read():
    if DEBUG:
      print "We already got this one, moving on ..."
    return

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


def get_tv_shows():

  for item in FEEDS:
  
    path = os.path.join(TVDIR,item['show'])

    if item['type'] == "rss":
      if DEBUG:
        print "Processing rss feed ..."
      add_from_rss_feed(path,item['url'],item['encoding'],item['signature'],item['limit'])
    elif item['type'] == "html":
      if DEBUG:
        print "Processing html feed ..."
      add_from_html_feed(path,item['url'],item['encoding'],item['signature'],item['limit'])


# Main
def main():
  get_tv_shows()

if __name__ == "__main__":
    main()
