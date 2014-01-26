import urllib2
import re
import sys, os, errno

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
  tvdir = "/media/windowsshare/downloads/completed/TV"
  show = "Modern Family"
  feeds = [
      {'site': 'extratorrent', 'show': 'Modern Family', 'encoding': 'XviD', 'signature': 'ettv', 'url': 'http://extratorrent.cc/rss.xml?type=last&cid=632'},
      ]

  for feed in feeds:

    # Extract the torrent url from the feed
    torrent_fn = get_torrent_url(feed['url'])
        
    # Check if we have this torrent already



  sys.exit()



  path = os.path.join(tvdir,os.path.join(show,'torrents'))
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

  # Check if we already have the torrent


  response = urllib2.urlopen(torrenturl)
  html = response.read()
  f = open(os.path.join(path,torrentfn),'w')
  f.write(html)
  f.close

if __name__ == "__main__":
    main()
