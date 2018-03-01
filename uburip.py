## heracl.es/ubuweb
## 2018-02

import csv, random, time, datetime, re, youtube_dl, wget
from subprocess import call

# prints a filesize that makes sense
def sizeof_fmt(num, suffix='B'):
	for unit in [' ',' k',' M',' G',' T',' P',' E',' Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, ' Y', suffix)

# outputs a list of films
with open('ubucurate.csv', 'r', encoding='utf-8') as csvinput:
	films = csv.DictReader(csvinput)
	films = list(films)



# print('TOTAL FILMS: ' + str(len(films_selected)))
# print('TOTAL DURATION: ' + str(datetime.timedelta(seconds=films_duration_total)))
# print('ESTIMATED TOTAL SIZE: ' + sizeof_fmt(films_size_total))

# uncomment the following to enable download of videos

n = 1
for film in films:
	print(film)
	filename = str(format(n, '03')) + '_' + film['film_filename']
	if film['film_vimeo']:
		print('DOWNLOADING FROM VIMEO')
		command = 'youtube-dl ' + film['film_vimeo'] + ' -o /videos/' + filename
		call(command.split(), shell=False)
	else:
		print('DOWNLOADING FROM UBUWEB')
		wget.download(film['film_url'], 'videos/' + filename)
	n += 1
