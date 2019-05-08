import requests 
from bs4 import BeautifulSoup 
import os  
def get_audio_links(url): # searches the HTML page and extracts urls ending with mp3
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, "html.parser") 
    links = soup.findAll('audio') 

    audio_links = [link['src'] for link in links if link['src'].endswith('mp3')] 
    return audio_links 
	
def findNextPage(url): # searches the HTML page and extracts the url of the next page (need to adjust the function based on HTML formatting of each website)
	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html.parser')
	nextpage = soup.findAll('a')	
	nexturl = ""
		
	for next in nextpage:
		if (next.has_attr('class')):
			if (next['class'][0] == "current2"):
				nexturl = nexturl + next['href']
				break
	
	return nexturl	
	
def download_audio(audio_links): # downloads the mp3 files to the directory containing this program file using links from the get_audio_links method
	
		for link in audio_links:
			print("downloading ", link)
			req = requests.get(link, stream=True)
			file_name = link[40:]
			file_name = os.path.join('songs', file_name)
			with open(file_name, 'wb') as f: 
				for chunk in req.iter_content(chunk_size = 1024*1024): 
					if chunk: 
						f.write(chunk) 
		return
	
def crawl_website(): # crawls the website to download music files
	url = "https://www.bensound.com/royalty-free-music"
	i = 1
	
	while not(url is None) :
		audio_links = get_audio_links(url)
		url = findNextPage(url)
		download_audio(audio_links)
		print("page ",i, "done") 
		i = i+1

crawl_website()