## heracl.es/ubuweb
## 2018-01-20

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
with open('ubuscrape_sample.csv', 'r', encoding='utf-8') as csvfile:
	films = csv.DictReader(csvfile)
	films = list(films)

films_duration_max = 60*60*24
films_duration_total = 0
films_size_total = 0
films_selected = []
# what time do the films screen, in seconds
film_film_screening_offset = 60*60*20

film_screening = time.strftime("%H:%M", time.gmtime(films_duration_total + film_film_screening_offset))

while True:
	film_random = random.choice(films)
	# print(film_random)
	film_duration = int(film_random['film_duration'])
	if films_duration_total+film_duration < films_duration_max:
		if film_duration > 0 and film_duration < 20*60:
			output = film_screening + ' | ' + film_random['film_creator']
			output += ' — ' + film_random['film_title'] if film_random['film_title'] else ''
			output += ', '
			output += time.strftime('%M', time.gmtime(film_duration)).lstrip('0') + '′' if film_duration > 60 else str(film_duration) + '′′'
			# remove multiple spaces
			output = re.sub(' +', ' ', output)
			print(output)

			film_screening = time.strftime("%H:%M", time.gmtime(films_duration_total + film_film_screening_offset))


			films_duration_total += film_duration
			films_size_total += int(film_random['film_filesize'])
			films_selected.append(film_random)
			films.remove(film_random)
	else:
		break

print('TOTAL FILMS: ' + str(len(films_selected)))
print('TOTAL DURATION: ' + str(datetime.timedelta(seconds=films_duration_total)))
print('ESTIMATED TOTAL SIZE: ' + sizeof_fmt(films_size_total))

## uncomment the following to enable download of videos

# n = 1
# for film in films_selected:
# 	filename = str(format(n, '03')) + '_' + film['film_filename']
# 	if film['film_vimeo']:
# 		command = 'youtube-dl ' + film['film_vimeo'] + ' -o /videos/' + filename
# 		call(command.split(), shell=False)
# 	else:
# 		print('NOT IN VIMEO!')
# 		wget.download(film['film_file'], 'videos/' + filename)
# 	n += 1
