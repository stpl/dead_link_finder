from url_opener import URLOpener
from html_doc import HTMLDoc
from urlparse import urlparse


class Crawler():
  def __init__(self,url):
    self.host_name = urlparse(url).hostname
    self.visited_urls = []
    self.dead_urls = []
    self.crawl(url)


  def get_dead_urls(self):
    return self.dead_urls

  def crawl(self, url):
    if self.is_visited(url):return
    if self.is_external_url(url):return
    self.visited_urls.append(url)
    url_opener = URLOpener(url)
    if url_opener.is_valid():
      html_content = url_opener.get_content()
      html_doc = HTMLDoc(html_content)
      links = html_doc.get_links()
      if not links: return
      for link in links: 
       if link:
         new_url = self.get_url(link, url)
         self.crawl(new_url)
      return
    else:
      print url
      self.dead_urls.append(url)

  def is_external_url(self, link):
    return True if (self.host_name != urlparse(link).hostname) else False    

  def is_visited(self, url):
    return True if url in self.visited_urls else False    

  def get_url(self, link, current_url):
    url = self.make_absolute_url(link, current_url) if self.is_relative_URL(link) else link
    return url
  def is_relative_URL(self, link):
    if link.startswith("http") or link.startswith("https") or link.startswith("www"):
      return False
    return True

  def make_absolute_url(self, link, current_url):
    if link.startswith("/"):
      parse_result = urlparse(current_url)
      base_url  = parse_result.scheme+"://"+parse_result.hostname
    else:
      base_url = current_url.rsplit('/',1)[0]      

    return base_url + link
