# web server for smart bike rental system
The webserver has been build with django and provides a way for users to hire bikes.

## installation

the project has the following dependencies:

- [python](https://www.python.org/)
- [django](https://www.djangoproject.com/)
- [django-rest-framework](https://www.django-rest-framework.org/)
- [djoser](https://github.com/sunscrapers/djoser)

clone this repository

`git clone https://github.com/PenO3-CW2B2/webapp`

rename the `example.settings.py` to `settings.py` and edit the following settings:

- [ALLOWE_HOSTS](https://docs.djangoproject.com/en/2.1/ref/settings/#s-allowed-hosts)
- HOST_PREFIX (see commend)
- [DATABASES](https://docs.djangoproject.com/en/2.1/ref/settings/#s-databases)

You can test the server by running it locally

`python manage.py runserver`

and you should be able to access it on http://127.0.0.1:8000
