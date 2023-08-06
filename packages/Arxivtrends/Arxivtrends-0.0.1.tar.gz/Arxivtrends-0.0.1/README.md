# arXivTrends

An arXiv scraper to retrieve records from given research areas in mathematics and
detect some trends in hyper-specialization and rate increase of scientific
production in those fields.

## Install
Use the package manager [pip](https://pip.pypa.io/en/stable/) (or ```pip3``` for python3):

```bash
$ pip install arxivtrends
```

Alternatively, download the source and use ```setup.py```:

```bash
$ python setup.py install
```

To update the module using ```pip```:

```bash
$ pip install arxivtrends --upgrade
```

## Examples
Let's import ```arxivtrends``` and create a scraper to fetch all preprints in
Fourier analysis (for other fields see below):

```python
import arxivtrends
scraper = arxivtrends.Scraper(macro_field='Elliptic PDE')
```

The instantiation of the class ```Scraper``` with the parameter ```macro_field```
set to 'Elliptic PDE' returns a dictionary-like
object containing all the information (authors, title, submission date, etc.)
about the arXiv preprints whose [Mathematics Subject Classification (MSC)](https://cran.r-project.org/web/classifications/MSC-2010.html) falls under the category Partial differential
equations of elliptic type.

Once ```scraper``` is built, we can start the parsing process and extract the
information we want for each preprint: submission date, list of authors and
number of pages.

```python
output_df = scraper.scrape()
```

While ```scrape()``` is running, it prints its status:

```python
Total number of papers scraped: 100
Total number of papers scraped: 200
...
```

Finally the extracted information is saved both into the pandas DataFrame ```output_df```
and into a ```.csv``` file. The latter option may be useful in case of overnight
running and kernel shutdown after a certain time of inactivity, as the parsing
process may last up to a few hours (see the script ```arxivtrends.py```).

Once the parsing is complete, we can call the data visualization methods (see the
  script ```graphics.py```) and see what the data can tell us. For example, the
  below call to the method ```plot_N_authors_papers()``` shows the number of
  uploaded arXiv preprints with at least 3 authors, year by year:

```python
plot_N_authors_papers(output_df, 3)
```
![picture](PDE.png)

For a complete walkthrough of the package, see the ```.ipynb``` file.

## Research Areas
Currently available option for the parameter ```macro_field```:
```Fourier Analysis``` (MSC codes: 42A05 - 42C40), ```Abstract Fourier Analysis``` (MSC codes: 43A05 - 43A90), ```Elliptic PDE``` (MSC codes: 35J05 - 35J85), ```Fluid Mechanics PDE``` (MSC codes: 76A02 - 76S05).


## License
[MIT](https://choosealicense.com/licenses/mit/)
