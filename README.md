# Project Name
## Social Media Scrapping
In this project we scrap varous plateform data like instgram twitter facebook using python django basically we create a tool that has we scrapp varous social media plateform using tool
### Overview
* The Twitter Scraping project is designed to extract valuable data from Twitter. It provides a robust API that facilitates several functionalities:

***Profile Data Scraping***-
Retrieve detailed information about Twitter profiles using profile names.

***Trending Hashtags Scraping***-
Extract the latest trending hashtags on Twitter to stay updated with current trends.
***Hashtag-based Data Scraping***
Collect tweets and associated data by searching specific hashtags.

***Scraping Using Post-Ids*** -
Fetch information about specific posts using their unique post IDs.

***Scraping Post Comments***-
 Fetch comments associated with specific posts using their unique post IDs.


# Setup Instructions

## Installation

### Python Installation Process
Before proceeding, ensure Python is installed on your system. If not, you can download and install Python from [python.org](https://www.python.org/downloads/).

### Setting up a Virtual Environment
To work with Django, it's recommended to create a virtual environment. Follow the steps outlined in the [Python documentation](https://docs.python.org/3/tutorial/venv.html) or use tools like `virtualenv` or `venv`.

### Installing Django
Once the virtual environment is set up, you can install Django within it. Refer to the [Django documentation](https://docs.djangoproject.com/en/stable/intro/install/) for detailed instructions on installing Django.

## Getting Started

### Clone the Project
```bash
git clone https://github.com/exoticaitsolutions/Twitter-Scrapping
```

## Navigate to the Project Directory

```bash
  cd Twitter-Scrapping
```

# Install Dependencies
### Using requirements.txt
```
pip install -r requirements.txt
```

# Individual Dependencies

**Undetected Chromedriver**
```
pip install undetected-chromedriver
```
***Selenium***
```
pip install selenium
```
***Core Headers***
```
pip install django-cors-headers
```

***Setuptools***
```
python -m pip install --upgrade pip setuptools
```
## Chromedriver
* Ensure that the version of Chromedriver matches the version of Google Chrome installed on your system for proper functionality.

# Run Project
```bash
python manage.py runserver
```

**Unix/MacOS/Linux:**

```bash
python3 manage.py runserver
```


