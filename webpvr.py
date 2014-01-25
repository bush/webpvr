import urllib2
import re

def main():
 
  # TODO: Add all failure paths

  response = urllib2.urlopen('http://extratorrent.cc/rss.xml?type=last&cid=632')
  html = response.read()
  
  
  # Find the first line that matches the type and ID we're looking for 
  for line in html.splitlines():
    if re.search('XviD',line) and re.search('ettv',line):
      match = re.search('<enclosure url="([^"]*)"',line)
      torrenturl = match.groups()[0]
      break

  # Save the torrent
  print torrenturl
  match = re.search('\/([^\/]*\.torrent)',torrenturl)
  if match:
    fn = match.groups()[0]
    print fn
  exit
  response = urllib2.urlopen(torrenturl)
  html = response.read()
  f = open(fn,'w')
  f.write(html)
  f.close
 # print html

  # Check if the torrent alread exists, add it if it does not
  

  # Clean up torrents that are a few days old 


 

if __name__ == "__main__":
    main()
