# Constructive Geometries - Python library

[![Documentation Status](https://readthedocs.org/projects/constructive-geometries/badge/?version=latest)](http://constructive-geometries.readthedocs.io/?badge=latest) [![Build Status](https://travis-ci.org/cmutel/constructive_geometries.svg?branch=master)](https://travis-ci.org/cmutel/constructive_geometries) [![Coverage Status](https://coveralls.io/repos/github/cmutel/constructive_geometries/badge.svg?branch=master)](https://coveralls.io/github/cmutel/constructive_geometries?branch=master)

Simple tools to define world locations from a set of topological faces and set algebra. For example, one could define a "rest of the world" which started from all countries, but excluded every country who name started with the letter "a".

[Documentation](http://constructive-geometries.readthedocs.io/?badge=latest) and [usage example](https://github.com/cmutel/constructive_geometries/blob/master/examples/Geomatching.ipynb).

Builds on top of [constructive geometries](https://github.com/cmutel/constructive_geometries).

Basic installation needs [wrapt](http://wrapt.readthedocs.io/en/latest/) and [country_converter](https://github.com/konstantinstadler/country_converter); GIS functions need [shapely](https://github.com/Toblerity/Shapely), and [fiona](https://github.com/Toblerity/Fiona).
