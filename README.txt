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


## Things to improve

### … in general

- The efficiency and style of the code.
- The inline comments that explain how it works
- …

### … in *ubuscrape.py*

- Strip HTML comments to include hidden Creators as well.

### … in *ubucurate.py*


### … in *uburip.py*

- Display progress of download, current index and running time.
- Warn and request confirmation if files exist in /videos/
- Continue from the last file existing, or prompt for index.


## Known Issues

- The following pages cause *ubuscrape.py* to halt:
	+ ...
- Several videos cannot be probed for duration (or it times out), therefore are returned with 0 duration and ignored by *ubucurate.py*.
- Some Creator (see Artist) and Film names cannot be scraped, because if inconsistent HTML.


## Licence

Copyright (c) 2017 Heracles Papatheodorou, https://heracl.es

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.