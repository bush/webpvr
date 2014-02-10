#!/usr/bin/python

import urllib, urllib2
from bs4 import BeautifulSoup
import re
import sys, os, errno
import feedparser
from subprocess import call

DEBUG = 1 
TVDIR = "/media/windowsshare/downloads/completed/TV"
MOVIEDIR = "/media/windowsshare/downloads/completed/Movies"
FEEDS = [
    #{'type': 'rss', 'show': 'Modern Family', 'encoding': 'XviD', 'signature': 'ettv', 'url': 'http://extratorrent.cc/rss.xml?type=last&cid=632', 'limit': 3},
      {'type': 'html', 'show': 'The Big Bang Theory', 'encoding': 'x264', 'signature': 'LOL', 'url': 'https://thepiratebay.se/search/the%20big%20bang%20theory/0/7/0', 'limit': 3},
      {'type': 'html', 'show': 'Modern Family', 'encoding': 'x264', 'signature': 'eztv', 'url': 'https://thepiratebay.se/search/modern%20family/0/7/0', 'limit': 3},
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


def add_from_piratebay_most_seeded(movie):
  url = r'http://thepiratebay.se/search/'
  movie_url = movie.replace(' ','%20')
  url = url+movie_url+'/0/7/0'
  
  response = urllib2.urlopen(url)
  html = response.read()
  list = re.findall(r'href="(magnet:[^"]*)"',html)
  path = os.path.join(MOVIEDIR,movie)
  add_torrent(path,list[0])


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

def get_movie_list():
  user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
  url = 'http://www.rottentomatoes.com/dvd/top-rentals/'
  headers = { 'User-Agent' : user_agent }
  data = urllib.urlencode({})
  req = urllib2.Request(url, data, headers)
  response = urllib2.urlopen(req)
  html = response.read()
  #html = open('table').read() 
  soup = BeautifulSoup(html)
  table = soup.find("table", attrs={"class":"center movie_list rt_table"}) 

  # The first tr contains the field names.
  headings = [th.get_text() for th in table.find("tr").find_all("th")]

  datasets = []
  for row in table.find_all("tr")[1:]:
    dataset = dict(zip(headings, (td.get_text().strip() for td in row.find_all("td"))))
    datasets.append(dataset)

  # Touch the history file
  movies_fn = os.path.join(TVDIR,'movies')

  f = open(movies_fn, 'a+')
  movies = []
  lines = f.read()

  for row in datasets:
  
    movie = row['Title']
    score = int(row['T-Meter'].strip('%'))

    if score > 80:
      #print "|%s|" % row['Title']
      #print "|%s|" % score 
      # Move on if we already downloaded the torrent file

      if movie in lines:
        if DEBUG:
          print "We already downloaded %s" % movie
        continue

      movies.append(movie)
      f.write("%s\n" % movie)

  f.close
  return movies

def get_movies():
  movies = get_movie_list()
  for movie in movies:
    add_from_piratebay_most_seeded(movie)

# Main
def main():
  get_tv_shows()
  get_movies()

if __name__ == "__main__":
    main()
