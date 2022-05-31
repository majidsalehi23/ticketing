# Ticketing App
### Overview
In Telecommunication companies, there is a need for a centralized ticketing system to monitor and manage high volumes of requests and responses. The ticketing system is developed to create, modify, query, and close a ticket. An admin defines different roles for each user. Both customer and vendor can login the same ticketing system to take a set of ticketing actions based on their access level.

### Requirements
- Postgresql version: 4.0 or higher
- Python version: 3.8.x
- Django: 4.0 or higher

### Installation
1. setup a PostgreSQL database
2. setup pgAdmin for managaing the PostgreSQL
3. open the pgAdmin and run the sql scripts in the [initial_data.txt](https://github.com/majidsalehi23/ticketing/tree/main/doc/initial_data.txt) to have the minimum data for testing the app
2. install python and django
3. check the djangoversion:
	python -m django --version
4. change the directory to the TicketingSite folder, where the manage.py locates.
5. run the following command:
	python manage.py runserver
6. use the users' list in the [users.xlsx](https://github.com/majidsalehi23/ticketing/tree/main/doc/users.xlsx) to test the app with different users and different roles.
7. Navigate to the localhost:8000/TicketingApp/login