# EcoImpact Repo
This readme file contains the guide to running backend and frontend server for EcoImpact.
## Backend
The following steps are to be followed to run the program: 
* Navigate to the backend folder
* ### Setup a python virtual environment
    * pip install virtualenv (one time)
    * virtualenv env (one time)
    * [source env/bin/activate] (linux) OR [ env/Scripts/activate] (windows) {everytime for running the project} 
* ### Run Project
    * python manage.py makemigrations
    * python manage.py migrate
    * python manage.py runserver


## Frontend
The following steps are to be followed to run the program: 
* Navigate to the frontend folder
* npm install
* npm run dev (for development server)
* npm run build (for production build)



## Tech Stack
The following tech stack was used to build this application.
* Database: MariaDB
* Backend: Django, Django Rest Framework, Allauth
* Frontend: Vue Js