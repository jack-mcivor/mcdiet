# The McDiet
Constrained integer optimisation of McDonalds meals

# Develop
Install locally and run some quick tests:
```
python setup.py develop
python setup.py test
```
(Alternatively may install using `pip install -e .` and/or test with pytest directly using `pytest`)

# Usage
See the `example_diets.py` script for example usage

# Requirements
Building the problem and solving it requires [PuLP](https://github.com/coin-or/pulp), which comes with a preconfigured MIP solver called [CBC](https://projects.coin-or.org/Cbc). These should be automatically installed by setuptools when installing the package.

# Data
Price data is scraped from [Uber Eats](https://www.ubereats.com/en-NZ/wellington/food-delivery/mcdonalds-bunny-street/JLKY-yejQb-dK3ZK_hT_YA/), nutritional information is scraped from [McDonalds](https://mcdonalds.co.nz/menu), and the two manually merged. The resulting data is stored as static json files in the `/assets` directory. Note that the data hasn't been updated since 2017-12 and is due for a freshen up!

# Roadmap
* [x] constrain nutrition, minimise price
* [ ] constrain price, maximise nutrition (or 'health')
* [ ] input validation
* [ ] allergens
* [ ] fractional solutions?