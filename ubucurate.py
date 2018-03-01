## heracl.es/ubu24h
## 2018-02

import csv, random, time, datetime, re, youtube_dl, wget, sys
from subprocess import call

# prints a filesize that makes sense
def sizeof_fmt(num, suffix='B'):
	for unit in [' ',' k',' M',' G',' T',' P',' E',' Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, ' Y', suffix)

# outputs a list of films
with open('./samples/ubuscrape.csv', 'r', encoding='utf-8') as csvinput:
	films = csv.DictReader(csvinput)
	films = list(films)

films_hours = input("Enter the duration in hours (default = 24):") or 24;
films_duration_clip = input("Enter the maximum duration per film in minutes (default = 20):") or 20;
film_film_screening_offset = 60*60*input("Enter the time the screenings start in hours (default = 20):") or 20 # what time do the films screen, in seconds
films_duration_max = 60*60*films_hours # maximum duration in seconds, 24 hours
films_duration_slack = 30; # min and max slack in seconds
films_duration_total = 0
films_size_total = 0
films_selected = []
film_programme = str(films_hours) + ' HOURS OF UBUWEB, BY UBUCURATE.PY\r\n\r\n'
print(film_programme)

film_screening = time.strftime("%H:%M", time.gmtime(films_duration_total + film_film_screening_offset))

# iterate artist links and write to .csv
with open('ubucurate.csv','w', newline='', encoding='utf-8') as csvoutput:
	wr = csv.writer(csvoutput, dialect='excel')
	wr.writerow(['film_screening','film_creator','film_title','film_duration_human','film_filename','film_vimeo','film_url'])

	while True:
		film_random = random.choice(films)
		# print(film_random)
		film_duration = int(film_random['film_duration'])
		if films_duration_total < films_duration_max - films_duration_slack:
			if film_duration > 0 and film_duration < films_duration_clip*60: # limit max duration to 20 minutes
				if films_duration_total+film_duration < films_duration_max + films_duration_slack: # check whether the new total duration is within the given slack
					film_duration_human = time.strftime('%M', time.gmtime(film_duration)).lstrip('0') + '′' if film_duration > 60 else str(film_duration) + '′′'
					output = film_screening + ' | ' + film_random['film_creator']
					output += ' — ' + film_random['film_title'] if film_random['film_title'] else ''
					output += ', '
					output += film_duration_human
					output = re.sub(' +', ' ', output) # remove multiple spaces
					output += '\r\n'
					print(output) # display the selected film

					wr.writerow([film_screening,film_random['film_creator'],film_random['film_title'],film_duration_human,film_random['film_filename'],film_random['film_vimeo'],film_random['film_url']]) # write to CSV

					film_programme += output;

					films_duration_total += film_duration
					film_screening = time.strftime("%H:%M", time.gmtime(films_duration_total + film_film_screening_offset)) # next screening time


					films_size_total += int(film_random['film_filesize'])
					films_selected.append(film_random)
					films.remove(film_random)

		else:
			break

output = '\r\n'
output += 'GENERATED: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '\r\n'
output += 'TOTAL FILMS: ' + str(len(films_selected)) + '\r\n'
output += 'TOTAL DURATION: ' + str(datetime.timedelta(seconds=films_duration_total)) + '\r\n'
output += 'ESTIMATED TOTAL SIZE: ' + sizeof_fmt(films_size_total)

print(output)

film_programme += output;
with open("ubucurate.txt", 'w', newline='', encoding='utf-8') as text_file:
    text_file.write(film_programme)

## uncomment the following to enable download of videos

# n = 1
# for film in films_selected:
# 	filename = str(format(n, '03')) + '_' + film['film_filename']
# 	if film['film_vimeo']:
# 		command = 'youtube-dl ' + film['film_vimeo'] + ' -o /videos/' + filename
# 		call(command.split(), shell=False)
# 	else:
# 		print('NOT IN VIMEO!')
# 		wget.download(film['film_url'], 'videos/' + filename)
# 	n += 1
