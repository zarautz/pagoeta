Pagoeta
=======

[![travis-badge]][travis]
[![coveralls-badge]][coveralls]
[![license-badge]](LICENSE)

`Pagoeta` is the code name of the Open API for the city of [Zarautz](http://www.zarautz.org/), based on
the `Open Data` philosophy. You can access the API at [https://data.zarautz.xyz/](https://data.zarautz.xyz/).

API Usage policy
----------------
Usage of the OpenZarautz API is currently unrestricted. API keys are not used. Please be gentle with our server!
In the future, we may require registration and API keys for heavy use.

All data is made available under the [Open Database License](http://opendatacommons.org/licenses/odbl/1.0/).
Any rights in individual contents of the database are licensed under the
[Database Contents License](http://opendatacommons.org/licenses/dbcl/1.0/).
Whenever external sources are mentioned you should mention them too when you present the data.


For developers
==============

Pagoeta uses [Django](https://www.djangoproject.com/) and the
[Django REST Framework](http://www.django-rest-framework.org/). Feel free to contribute to the project.

Application dependencies
------------------------
The application uses the [pip Package Manager](http://pip.readthedocs.org/en/latest/) to install dependencies.
While in development, you will need to read the dependencies from the following file (includes packages like
`debug_toolbar`):

    $ pip install -r requirements/development.txt

Configuration
-------------
The application looks for the necessary configuration/credentials in a JSON file at the root folder.
This file uses the same names we use as config vars in [Heroku](https://devcenter.heroku.com/articles/config-vars).

For development, just copy `config.json.txt` to `config.json` and fill in the options (only real database information
is strictly necessary).

Once the database configuration is filled in you can generate the necessary tables and load some fixtures using
`manage.py`:

    $ python manage.py migrate

Running the server
------------------
    $ python manage.py runserver

Running spec tests
------------------
    $ python manage.py test pagoeta.apps

Coverage of the tests
---------------------
    $ coverage run --source='pagoeta/apps' manage.py test pagoeta.apps
    $ coverage report -m

Style guide
-----------
Unless otherwise specified, follow
[Django Coding Style](https://docs.djangoproject.com/en/1.8/internals/contributing/writing-code/coding-style/).
Tab size is 4 **spaces**. Maximum line length is 119. Furthermore your code has to validate against pyflakes.
It is recommended to use [flake8](https://pypi.python.org/pypi/flake8) which combines all the checks
(`flake8` is included in the development requirements):

    $ flake8 --max-line-length=119 pagoeta


[travis-badge]: https://travis-ci.org/zarautz/pagoeta.svg?branch=master
[travis]: https://travis-ci.org/zarautz/pagoeta?branch=master
[coveralls-badge]: https://coveralls.io/repos/github/zarautz/pagoeta/badge.svg?branch=master
[coveralls]: https://coveralls.io/r/zarautz/pagoeta?branch=master
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
