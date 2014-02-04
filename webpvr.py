#!/usr/bin/python

import urllib2
import re
import sys, os, errno
import feedparser
from subprocess import call

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




def main():
 
  # TODO: Add all failure paths
  TVDIR = "/media/windowsshare/downloads/completed/TV"
  FEEDS = [
      {'site': 'extratorrent', 'show': 'Modern Family', 'encoding': 'XviD', 'signature': 'ettv', 'url': 'http://extratorrent.cc/rss.xml?type=last&cid=632'},
      {'site': 'extratorrent', 'show': 'The Big Bang Theory', 'encoding': 'XviD', 'signature': 'ettv', 'url': 'http://extratorrent.cc/rss.xml?cid=583&type=last'},
      ]

  for feed_entry in FEEDS:
  
    # Extract the torrent url
    feed = feedparser.parse(feed_entry['url'])

    #print feed
    #if feed.bozo:
    #  print "There is something wrong with this feed.  Maybe the site is down ..."
    #  continue

    for item in feed["items"]:  

      torrent_url = item['links'][1]['href']
      
      if re.search(feed_entry['encoding'],torrent_url) and re.search(feed_entry['signature'],torrent_url):
         break

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
    open(history_fn, 'a').close()

    # Move on if we already downloaded the torrent file
    if torrent_url in open(history_fn).read():
      print "We already got this one, moving on ..."
      continue

    cmd = ['transmission-remote','-w',path,'-a',torrent_url]

    try:
      devnull = open('/dev/null', 'w')
      retcode = call(cmd,stdout=devnull, stderr=devnull)
      devnull.close
    except OSError, msg:
      quit("Could not execute the above command: %s\n" % cmd)

    f = open(history_fn,'w')
    f.write(torrent_url)
    f.close
  

if __name__ == "__main__":
    main()
