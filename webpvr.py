#!/usr/bin/python

import urllib2
import re
import sys, os, errno
import feedparser

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

def main():
 
  # TODO: Add all failure paths
  TVDIR = "/media/windowsshare/downloads/completed/TV"
  FEEDS = [
      {'site': 'extratorrent', 'show': 'Modern Family', 'encoding': 'XviD', 'signature': 'ettv', 'url': 'http://extratorrent.cc/rss.xml?type=last&cid=632'},
      ]

  for feed_entry in FEEDS:
  
    # Extract the torrent url
    feed = feedparser.parse(feed_entry['url'])
    for item in feed["items"]:  

      torrent_url = item['links'][1]['href']
      
      if re.search(feed_entry['encoding'],torrent_url) and re.search(feed_entry['signature'],torrent_url):
         break

    torrent_fn = torrent_url.split('/')[-1] 

    # Create the torrent directory if it does not exist
    path = os.path.join(TVDIR,os.path.join(feed_entry['show'],'torrents'))
    try:
      os.makedirs(path)
    except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST and os.path.isdir(path):
        pass
      else: raise
    
    # Move on if we already downloaded the torrent file
    if os.path.isfile(os.path.join(path,torrent_fn))
      print "We already got this one, moving on ..."
      continue

    # Download the torrent
    response = urllib2.urlopen(torrenturl)
    html = response.read()
    f = open(os.path.join(path,torrentfn),'w')
    f.write(html)
    f.close

   # Add the torrent
   cmd = 'transmission-remote -a %s' % os.path.join(path,torrentfn)
   print cmd
   #os.system(cmd) 

if __name__ == "__main__":
    main()
