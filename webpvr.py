import urllib2
import re
import os, errno

def main():
 
  # TODO: Add all failure paths
  tvdir = "/media/windowsshare/downloads/completed/TV"
  show = "Modern Family"

  response = urllib2.urlopen('http://extratorrent.cc/rss.xml?type=last&cid=632')
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
  else:
    sys.exit("We didn't find any matching torrents.")

  response = urllib2.urlopen(torrenturl)
  html = response.read()
  f = open(torrentfn,'w')
  f.write(html)
  f.close

  path = os.path.join(tvdir,os.path.join(show,'torrents'))
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

if __name__ == "__main__":
    main()
