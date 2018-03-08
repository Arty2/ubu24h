## heracl.es/ubuweb
## 2018-02

import csv, random, time, datetime, re, youtube_dl, wget, os.path
from urllib.parse import unquote

# prints a filesize that makes sense
def sizeof_fmt(num, suffix='B'):
	for unit in [' ',' k',' M',' G',' T',' P',' E',' Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, ' Y', suffix)

# outputs a list of films
with open('./output/ubucurate.csv', 'r', encoding='utf-8') as csvinput:
	films = csv.DictReader(csvinput)
	films = list(films)


n = 1

for film in films:
	print(film)
	filename = './videos/' + str(format(n, '04')) + '_' + film['film_screening'].replace(':', '') + '_' + film['film_filename']
	filename = unquote(filename)
	# see options at https://github.com/rg3/youtube-dl/blob/054b99a33079dcc4755e46aaf588424b4bb12020/youtube_dl/YoutubeDL.py
	ydl_options = {
		'outtmpl': filename,
		}

	if os.path.exists(filename) is False: # try to download if supposed filename doesn’t exist
		with youtube_dl.YoutubeDL(ydl_options) as ydl:
			try: # try to download from Vimeo
				print('DOWNLOADING ' + str(n) + ' FROM VIMEO')
				# youtube-dl won’t download a video if already present
				ydl.download([film['film_vimeo']])
			except: # but if it still fails to download, fetch from Ubu
				print('DOWNLOADING ' + str(n) + ' FROM UBUWEB')
				wget.download(film['film_url'], filename)
	n += 1
