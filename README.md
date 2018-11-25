# web server for smart bike rental system
The webserver has been build with django and provides a way for users to hire bikes.

## installation

the project has the following dependencies:

- [python](https://www.python.org/)
- [django](https://www.djangoproject.com/)
- [django-rest-framework](https://www.django-rest-framework.org/)
- [django-rest-framework-jwt](https://pypi.org/project/djangorestframework-jwt/)
- [djoser](https://github.com/sunscrapers/djoser)
- [pynmea2](https://github.com/sunscrapers/pynmea2)

clone this repository

`git clone https://github.com/PenO3-CW2B2/webapp`

rename the `example.settings.py` to `settings.py` and edit the following settings:

- [ALLOWE_HOSTS](https://docs.djangoproject.com/en/2.1/ref/settings/#s-allowed-hosts)
- HOST_PREFIX (see commend)
- [DATABASES](https://docs.djangoproject.com/en/2.1/ref/settings/#s-databases)
- [DEFAULT_FROM_EMAIL](https://docs.djangoproject.com/en/2.1/ref/settings/#s-default-from-email)

create the migrations for the bikes

`python manage.py makemigrations bikes`

apply the migrations to the database

`python manage.py migrate`

You can test the server by running it locally

`python manage.py runserver`

and you should be able to access it on http://127.0.0.1:8000

for installation on [an ulyssis server](https://ulyssis.org/hosting/) with (Fast)CGI see [this](https://docs.ulyssis.org/Using_(Fast)CGI_for_non-PHP_websites#Example:_Django).

Note: When using an appache server you should add `CGIPassAuth On` to the htaccess file.
Otherwise the custom header `Authorization` will not be passed to django.
