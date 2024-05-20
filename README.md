# Twitter Scrapping Rest APIs

To run this project, you will need to add the following environment variables to your .env file
`API_KEY` : http://127.0.0.1:8000/api
Database Details

## Run Locally

Clone the project

```bash
  git clone https://github.com/exoticaitsolutions/Twitter-Scrapping
```

Go to the project directory

```bash
  cd ssapi
```

Create Virtual Environment

Windows:

```bash
py -m venv env
```

Unix/MacOS/Linux:

```bash
sudo python3 -m venv env
```

Then you have to activate the environment, by typing this command:

Windows:

```bash
env\Scripts\activate.bat
```

Unix/MacOS/LLinux:

```bash
source env/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```python manage.py runserver

Then After make a make migrate using the following commandpython manage.py runserver

Windows:

```bash
python manage.py makemigrations api
```

Unix/MacOS/Linux:

```bash
python3 manage.py makemigrations
```

Then run the migrate command to create the tables in the database

Windows:

```bash
python manage.py migrate

```

Unix/MacOS/LInux:

```bash
python3 manage.py migrate
```

Start the server

**Windows:**

```bash
python manage.py runserver

```

**Unix/MacOS/LLinux:**

```bash
python3 manage.py runserver
```

