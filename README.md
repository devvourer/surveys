# surveys
Api for surveys


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/devvourer/surveys.git
$ cd surveys
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd main
```
Create `.env` file and write configs
```sh
SECRET_KEY=(your secret key)
```
Than in console enter:
```sh
(env)$ python manage.py runserver
```
# API documentation
`http://127.0.0.1:8000/`.
