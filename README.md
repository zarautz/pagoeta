Style guide
----------
Follow [Google Python Style Guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html). Tab size is 4 **spaces**.


Application dependencies
------------------------
The application uses the [pip Package Manager](http://pip.readthedocs.org/en/latest/) to install dependencies.
Depending on the environment, you will need to read from a different file (the development file includes packages
like `debug_toolbar`):

    $ pip install -r requirements/development.txt
    $ pip install -r requirements/production.txt


Configuration
-------------
The application looks for the necessary configuration/credentials in a JSON file at the root folder.
This file mimics the credentials file that will be automatically generated at a
[cloudControl](https://www.cloudcontrol.com/dev-center/quickstart) deployment.

For development, just copy `creds.json.txt` to `creds.json` and fill in the options.

Once the database configuration is filled in you can generate the necessary tables using `manage.py`:

    $ python manage.py migrate


Running the server
------------------
    $ python manage.py runserver


QA
--
Run Django spec tests:

    $ python manage.py test

TODO: readme QA development code coverage


Static files
------------

    $ python manage.py collectstatic
