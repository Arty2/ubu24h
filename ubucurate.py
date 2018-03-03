## heracl.es/ubu24h
## 2018-02

import csv, random, time, datetime, re, youtube_dl, wget, sys, smartypants, os
from subprocess import call

# prints a filesize that makes sense
def sizeof_fmt(num, suffix='B'):
	for unit in [' ',' k',' M',' G',' T',' P',' E',' Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, ' Y', suffix)

# outputs a list of films
if os.path.exists('./output/ubuscrape.csv'):
    inputfile = './output/ubuscrape.csv'
else:
    inputfile = './samples/ubuscrape.csv'
with open(inputfile, 'r', encoding='utf-8') as csvinput:
	films = csv.DictReader(csvinput)
	films = list(films)

films_hours = int(input("Enter the duration in hours (default = 24):") or 24);
films_duration_clip = int(input("Enter the maximum duration per film in minutes (default = 20):") or 20);
film_screening_offset = int(input("Enter the time the screenings start in hours (default = 20):") or 20)*60*60 # what time do the films screen, in seconds
film_screening_days = 1 # counter, do not modify
films_duration_max = 60*60*films_hours # maximum duration in seconds, 24 hours
films_duration_slack = 30; # min and max slack in seconds
films_duration_total = 0
films_size_total = 0
films_selected = []
film_programme = str(films_hours) + ' HOURS OF UBUWEB, BY UBUCURATE.PY<br><br>\r\n'
print(film_programme)

film_screening = time.strftime("%H:%M", time.gmtime(films_duration_total + film_screening_offset))

# iterate artist links and write to .csv

with open('./output/ubucurate.csv','w', newline='', encoding='utf-8') as csvoutput:
	wr = csv.writer(csvoutput, dialect='excel')
	wr.writerow(['film_screening','film_creator','film_title','film_duration_human','film_filename','film_vimeo','film_url'])

	while True:
		film_random = random.choice(films)
		# print(film_random)
		film_duration = int(film_random['film_duration'])
		if films_duration_total < films_duration_max - films_duration_slack:
			if film_duration > 0 and film_duration < films_duration_clip*60: # limit max duration to 20 minutes
				if films_duration_total+film_duration < films_duration_max + films_duration_slack: # check whether the new total duration is within the given slack
					# film_duration_human = time.strftime('%M', time.gmtime(film_duration)).lstrip('0') + '′' if film_duration > 60 else str(film_duration) + '′′'
					film_duration_human = time.strftime('%M', time.gmtime(film_duration)).lstrip('0') + '′' if film_duration > 60 else str(film_duration) + '″'
					output = film_screening + ' | '
					if film_random['film_creator']:
						output += film_random['film_creator']
					else:
						output += '<mark>Creator Missing</mark>'
					if film_random['film_title']:
						output += ' — <em>' + film_random['film_title'] + '</em>, '
					else: # iif title doesn’t exist, then use the filename
						output += ' — <mark><em>' + film_random['film_filename']\
						.replace('-', ' ')\
						.replace('_', ' ')\
						.replace('.iphone', '')\
						.replace('.mp4', '')\
						.replace('.m4v', '')\
						.replace('.avi', '')\
						.replace('.mov', '')\
						 + '</em></mark>, '
					
					output += film_duration_human
					output = re.sub(' +', ' ', output) # remove multiple spaces
					output += '<br>\r\n'
					output = smartypants.smartypants(output) # improve quotes and other typographical characters
					print(output) # display the selected film

					wr.writerow([film_screening,film_random['film_creator'],film_random['film_title'],film_duration_human,film_random['film_filename'],film_random['film_vimeo'],film_random['film_url']]) # write to CSV


					films_duration_total += film_duration
					film_screening = time.strftime("%H:%M", time.gmtime(films_duration_total + film_screening_offset)) # next screening time
					if int(time.strftime("%d", time.gmtime(films_duration_total + film_screening_offset))) > film_screening_days: # add an extra breakline where the day ends
						film_screening_days += 1
						output += '<br>\r\n<mark>DAY ' + str(film_screening_days)  +'</mark><br>\r\n'

					film_programme += output;
					films_size_total += int(film_random['film_filesize'])
					films_selected.append(film_random)
					films.remove(film_random)

		else:
			break

output = '<br>\r\n'
output += 'GENERATED: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '<br>\r\n'
output += 'TOTAL FILMS: ' + str(len(films_selected)) + '<br>\r\n'
output += 'TOTAL DURATION: ' + str(datetime.timedelta(seconds=films_duration_total)) + '<br>\r\n'
output += 'ESTIMATED TOTAL SIZE: ' + sizeof_fmt(films_size_total)

print(output)

film_programme += output;
with open('./output/ubucurate.html', 'w', newline='', encoding='utf-8-sig') as text_file:
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
