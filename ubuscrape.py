## heracl.es/ubu24h
## 2018-02

import requests, time, subprocess, csv, datetime
from bs4 import BeautifulSoup

# gets the duration of a video file
def get_duration(video):
	try:
		return str(subprocess.check_output(['ffprobe', '-i', video, '-rw_timeout', '4M', '-show_entries', 'format=duration', '-v', 'quiet', '-print_format', 'compact=print_section=0:nokey=1:escape=csv']),'utf-8').strip()
	except:
		return 0

# prints a filesize that makes sense
def sizeof_fmt(num, suffix='B'):
	for unit in [' ',' k',' M',' G',' T',' P',' E',' Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, ' Y', suffix)

# scrapes UbuWeb Films
def ubu_scrape(base = 'http://www.ubu.com/film/', links_number = 10, link_start = 1):
	global film_index
	# Open Ubuweb film page
	directory_page = requests.get(base)
	directory_soup = BeautifulSoup(directory_page.text, 'html.parser')
	# get all links in the second [1] table
	artist_links = directory_soup.findAll('table')[1].findAll('a')

	# Select a subset (or all)
	if links_number is not None:
		links_total = artist_links[link_start:(link_start + links_number)]
	else:
		links_total = artist_links[link_start:]


	artist_link_current = link_start
	film_index = 1;



	# iterate artist links and write to .csv
	with open('ubuscrape.csv','w', newline='', encoding='utf-8') as csvoutput:
		wr = csv.writer(csvoutput, dialect='excel')
		wr.writerow(['film_index','film_creator','film_title','film_duration','film_duration_human','film_filesize','film_filesize_human','film_filename','film_vimeo','film_file','film_page_url'])
		for artist_link in links_total:
			artist_page_url = 'http://www.ubu.com/film/'+ artist_link.get('href')[2:]
			print(str(artist_link_current) +'/' + str(len(links_total)+link_start) + '    http://www.ubu.com/film/'+ artist_link.get('href')[2:] + '    ' + time.ctime())

			# open artist page
			artist_page = requests.get(base + artist_link.get('href')[2:])
			artist_soup = BeautifulSoup(artist_page.text, 'html.parser')
			artist_page.close()

			# go to next of loop if "Error: template", see http://www.ubu.com/film/bataille.html
			if artist_page.text.find('Error: template') is 0:
				print('TEMPLATE ERROR!')
			else:
				# test whether the current page is a film instead of artist
				if artist_soup.find('a', {'id': 'moviename'}):
					print('THIS IS A FILM PAGE!')				
					ubu_film_scrape(artist_soup,wr,artist_page_url)
				else:
					# the following papth precedes film links, very prone to break
					potential_film_page_links = artist_soup.findAll("table")[1].findAll("td", attrs = {"class": "default"})[1].findAll("font")[0].findAll("img")
				
					# loop through artist's films
					for potential_film_page_link in potential_film_page_links:
						a = potential_film_page_link.findNext()
						try:
							potential_film_url = a["href"]
						except KeyError:
							continue
						# do not follow external or upwards links
						# TODO: check if file already exists, use a hash?
						if '../' not in a["href"] and 'http' not in a["href"]: 
							film_page_url = base + a["href"]
							print('   ' + str(film_index) + '/' + str(len(potential_film_page_links)) + ' ' + film_page_url)
							film_page = requests.get(film_page_url)
							film_soup = BeautifulSoup(film_page.text, 'html.parser')
							film_page.close()
							
							if film_soup.find(id='ubucreator'):
								ubu_film_scrape(film_soup,wr,film_page_url)
			
			artist_link_current += 1


def ubu_film_scrape(film_soup,wr,film_page_url):
	global film_index
	# scrape film metadata, if they exist
	film_creator = film_soup.find('span', {'id': 'ubucreator'}).text.strip() if film_soup.find('span', {'id': 'ubucreator'}) else ''
	film_title = film_soup.find('span', {'id': 'ubuwork'}).text.strip() if film_soup.find('span', {'id': 'ubuwork'}) else ''
	film_file = film_soup.find('a', {'id': 'moviename'}).get('href') if film_soup.find('a', {'id': 'moviename'}) else ''
	try:
		film_filesize = requests.get(film_file, stream=True).headers['Content-length']
	except KeyError:
		# if you can't get the filesize, set to 0
		film_filesize = 0
	except requests.exceptions.RequestException as e:
		print(e)
		# if there is no video file, then try the next link
		film_index +=1
		return
	film_filesize_human = sizeof_fmt(int(film_filesize))
	film_duration = int(float(get_duration(film_file)))
	film_duration_human = str(datetime.timedelta(seconds=film_duration))
	film_filename = film_file[film_file.rfind("/")+1:]
	film_vimeo = film_soup.find('iframe').get('src').replace('?transparent=0','') if film_soup.find('iframe') else ''
	# film_filesize.close()
	print('   ' + film_duration_human +' / '+ film_filesize_human)
	
	# film_descr = film_soup.find(id='ubudesc').text

	wr.writerow([film_index,film_creator,film_title,film_duration,film_duration_human,film_filesize,film_filesize_human,film_filename,film_vimeo,film_url,film_page_url])
	film_index +=1
	# sleep for a bit to cutdown on usage
	time.sleep(1)


ubu_scrape(links_number = None, link_start = 620)