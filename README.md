# Hacktoberfest
This project is a fresh Django project. It should work like any other ticketing system. This is the same project I mentioned in my hacktoberfest video https://youtu.be/a7eTy9lPeJ4

# RTask
RTask is a ticketing system written in python on top of Django.
## Running (simplified)

1. Clone the repo, if you haven't already, and `cd` to it
`git clone https://github.com/RTask/RTask.git`
`cd RTask/`

2. Install dependencies.
`python3 -m pip install -r requirements.txt`

3. Run app
`python3 rtask/manage.py runserver`

# Some django basics
*    Creating a new Django project
*    Inside it create a Django app
*    The main project folder will contain the app, a folder with the same name as the project,  and a __manage.py__ file
*    The main important files that are edited are: __views.py__, __urls.py__, __settings.py__, and __HTML__ file
*    __views.py__ file deals with the backend part i.e loading the model/operation/calculation, obtaining the values of the features used for determining the output.
*    __urls.py__ file deals with URLs i.e. linking both __views.py__ and __HTML__ files together
*    In __settings.py__ we must add the Django app name we used and the template under there respective places.
*    __HTML__ file describes the UI of the webpage we hosted.
*    The inputs entered by the user is then transferred to the __views.py__ file and the outcome is brought from there.
