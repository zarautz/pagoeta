OpenZarautz API
===============

[![travis-badge]][travis]
[![coveralls-badge]][coveralls]
[![license-badge]](LICENSE)

`Pagoeta` is the code name of the open API for the city of [Zarautz](http://www.zarautz.org/).
You can access the API at [https://pagoeta.herokuapp.com/](https://pagoeta.herokuapp.com/).

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

Pagoeta uses [Api Star](https://github.com/encode/apistar). Feel free to contribute to the project.

Application dependencies
------------------------
The application uses [Pipenv](https://docs.pipenv.org/#install-pipenv-today) to manage application dependencies.
While in development, you will need to install all dependencies (includes packages like `flake8`):

    $ pipenv install --dev
    $ pipenv shell

Running the server
------------------
    $ python runserver.py

Running unit tests
------------------
    $ python -m unittest pagoeta.tests

Coverage of the tests
---------------------
    $ coverage run --source=pagoeta -m unittest discover
    $ coverage report -m

Style guide
-----------
Unless otherwise specified, follow
[Django Coding Style](https://docs.djangoproject.com/en/1.11/internals/contributing/writing-code/coding-style/).
Tab size is 4 **spaces**. Maximum line length is 120. All changes should include tests and pass `flake8`.


[travis-badge]: https://travis-ci.org/zarautz/pagoeta.svg?branch=master
[travis]: https://travis-ci.org/zarautz/pagoeta?branch=master
[coveralls-badge]: https://coveralls.io/repos/github/zarautz/pagoeta/badge.svg?branch=master
[coveralls]: https://coveralls.io/r/zarautz/pagoeta?branch=master
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
