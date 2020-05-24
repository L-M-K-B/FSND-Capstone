# FSND-Capstone
## Table of contents
**[Introduction](#introduction)**<br>
**[Installation](#getting-startet)**<br>
**[Testing](#testing)**<br>
**[Generating tokens for testing](#generating-tokens-for-testing)**<br>
**[API endpoints](#api-endpoints)**<br>
**[Users](#users)**

## Introduction
This is the final project of my fullstack developer nano degree. I used the following technologies:
 
    - Coding in Python 3
    - Relational database architecture (PostgreSQL)
    - Modeling data objects with SQLAlchemy
    - Internet protocols and communication
    - Developing a Flask API
    - Testing Flask applications
    - Authentication and access management with Auth0 and Flask
    - Role-Based Access Control (RBAC)
    - Deploying the application with Heroku

## Getting started
Please install the following dependencies:
### Python 3
Follow the instructions in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
### Other dependencies
In this folder you can find a `requirements.txt` which you can run with the following command:
```
pip3 install -r requirements.txt
```
### Virtual Enviornment
It is recommended to work within a virtual environment. Instructions for setting it up can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
## Running the server !!!!!!!!!!!!!!!!!
First ensure that you are working in the created virtual environment.<br>
To run the server, execute:
```bash
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Sourcing `setup.sh` sets some environment variables used by the app.<br>
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.<br>
Setting the `FLASK_APP` variable to `app.py` directs flask to use the this file to find the application.<br>
You can run this API locally at the default `http://127.0.0.1:5000/`
## Testing
To run the tests, run
```
dropdb capstone-test
createdb capstone-test
python test_app.py
```
## Generating tokens for testing
For using and testing the API bearer tokens are needed for gaining access.<br>
Please follow the instructions below:
1. Enter this [URL](https://fsnd-lmkb-capstone.eu.auth0.com/authorize?audience=capstone&response_type=token&client_id=wdw6Dcq4kfsYVkuv34aMN2yCkZJa7SSG&redirect_uri=https://127.0.0.1:8080/login-results) in order to log in
2. Choose a [user](#users) and log in with the account data provided
3. The URL now shown will provide the token

**Note:** The token will be valid for 2 hours. 

## API endpoints
### GET: /movies
- fetches a dictionary of movies:
    - keys: ids of movies
    - values: string, name of movie
- request arguments: None
- returns a json file:
```
{
    'success': true,
    'movies': 
        {
            1 : 'Hidden Figures'
        }
}
```
### GET: /actresses
- fetches a list of objects containing all actresses
- each actress entry is formatted as a dictionary containing the following keys: 
    - birth_date (datetime)
    - gender (str)
    - id (int)
    - movies (list of movie ids)
    - name (str)
- request arguments: None
- returns a json file:
```
{
    'success': true,
    'actresses': 
        [
            {
                'birth_date': 'Fri, 11 Sep 1970 00:00:00 GMT',
                'gender': 'female',
                'id': 1,
                'movies': [1],
                'name': 'Taraji P Henson'
            }
        ]
}
```
### POST: /actress
- creates a new actress entry
- request arguments: 
    - birth_date (DateTime)
    - gender (str)
    - id (int)
    - movies (list of movie ids)
    - name (str)
- returns a json file:
```
{
    'success': true,
    'created': <actress_id (int)>
}
```
### POST: /movie
- creates a new movie entry
- request arguments: 
    - id (int)
    - title (str)
    - release_date (DateTime)
    - country (str)
- returns a json file:
```
{
    'success': true,
    'created': <movie_id (int)>
}
```
### DELETE: /actress/<actress_id>
- deletes a single actress
- request arguments: 
    - id of actress
- returns a json file:
```
{
    'success': true,
    'deleted': <actress_id (int)>
}
```
### PATCH: /actress/<actress_id>
- modifies an actress entry
- request arguments (changes are not necessarily applied to all arguments): 
    - birth_date (DateTime)
    - gender (str)
    - id (int)
    - movies (list of movie ids)
    - name (str)
- returns a json file:
```
{
    'success': true,
    'actress': 
        [
            {
                'birth_date': 'Fri, 11 Sep 1970 00:00:00 GMT',
                'gender': 'female',
                'id': 1,
                'movies': [1],
                'name': 'Taraji P Henson'
            }
        ]
}
```
## Users
There are two types of users with certain privileges.<br>
For testing their privileges user account data is provided here to gain suitable tokens.
### Casting Assistant
- Can view actors and movies

**Username:** casting-assistant@example.com<br>
**Password:** tesTteSt321

### Executive Producer
- Can view actors and movies
- Add or delete an actor from the database
- Add or delete a movie from the database
- Modify actors or movies

**Username:** executive-producer@example.com<br>
**Password:** TestTestT123
