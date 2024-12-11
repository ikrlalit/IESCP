
# IESCP V2

The Influencer Engagement & Sponsorship Coordination Platform - V2 is a multi-user web application that allows influencers to explore ad campaigns and sponsors to create new campaigns and ad requests to influencers.

## Technologies Used:
 * Python – Python is the primary programming language used for developing app
 * Flask – Used for backend application and APIs
 * SQLite- Serves as the database for the application
 * VueJS – Used for creating frontend of the application
 * Jinja2 – Used for displaying data dynamically in HTML pages
 * Bootstrap – It is a CSS framework, we used for making pages visually appealing
 * Redis – For caching and backend for celery 
 * Celery and Celery beat – To perform async task and schedule task for automatic execution
 * Mailhog – For setting and demonstrating mailing service on local system
## API Design:
The APIs are designed using Flask-Restful for performing CRUD on User,Influencer Profile, Sponsor Profile, Campaigns, Adrequests, etc We used the flask-jwt-extended package for implementing authentication and authorization on API endpoints. 

## Architecture and Features:
The application follows the standard MVC architecture. The frontend of the application is created using using vuejs 3.  The APIs are created using Python and Flask Restful. Models are the Python classes that map with SQLite database tables using the Flask-SQLAlchemy ORM library.
The features of the application are as follows-
* Signup and Login for influencer, sponsor and Admin
* An admin can view, approve new sponsor accounts, block any suspicious activity, and can monitor the applications statistics 
* A Influencer can view, search new campaign and adrequests from sponsors. They can negotiate on a request and chat with sponsors.
* Sponsors can create, update,read,delete new campaign and adrequests they can chat with influencers.
* We used caching to increase the performance of APIs
* We are using celery to offload backend heavy tasks and celery beat for scheduling mails and remainders 

## Instructions to Run the Application
* Download and extract the project directory
* Change directory to backend inside the project and setup virtual environment
* Use ```python3 -m venv .venv``` to create the virtual environment
* Once created use ```source .venv/bin/activate``` this will activate virutal environment
* Next execute the ```pip install -r requirements.txt``` this will install all the packages required for running the application
* Finally run the app using ```python app.py``` to run the flask server
* Open another terminal and change directory to frontend which is inside the main project folder
* Run ``` npm install``` to install the required packages
* Next run ```npm run serve``` to start the server
* Open another terminal and change directory to backend and then use ``` celery -A app:celery_app worker --loglevel INFO ``` to run the celery worker
* Now run the celery beat with ``` celery -A app:celery_app beat --loglevel INFO ```
* Make sure redis server is installed and running on your local system
* To setup SMTP server on local system you can install and use Mailhog. Use ```~/go/bin/MailHog ```


