# ubu24h

Ubu24h is a collection of three scripts, built to be used sequentialy with the purpose to:

1. *ubuscrape.py* — create a database of the films available on Ubuweb
	- IN:
		+ `https://www.ubuweb.com/film` the page to scrape
		+ the creator’s index (starting point, default = 1)
	- OUT: 
		+ `./output/ubuscrape.csv` contains the scraped data
2. *ubucurate.py* — generate an arbitrary selection of films
	- IN:
		+ `./output/ubuscrape.csv` or the provided `./sample/ubucurate.csv`
		+ the duration in hours (default = 24)
		+ the maximum duration per film in minutes (default = 20)
		+ the time the screenings start in hours (default = 20)
	- OUT:
		+ `./output/ubucurate.csv` the selected films
		+ `./output/ubucurate.html` a rich formatted programme of films
3. *uburip.py* — download the films and rename them appropriately
	- IN:
		+ `./output/ubucurate.csv`
	- OUT:
		+ `./videos/` …


## Things that could be improved

### in general

- The efficiency and style of the code.
- The inline comments that explain how it works
- …

### in `ubuscrape.py`
### in `ubucurate.py`
### in `uburip.py`

## Know Issues

- The following pages cause `ubuscrape.py` to halt:
	+ ...
- 

## Licence

MIT, do whatever you want