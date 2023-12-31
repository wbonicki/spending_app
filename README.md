# Application for spending management

## Description

The main goal of the application is to learn and organize my knowledge about software design, the Flask framework, SQLAlchemy, and the Docker Compose tool. __Frontend issues were not addressed as they were not a goal of this project.__ The application is still under a development and new features are planned to be added.

The application is designed for saving and analyzing user spendings.

## 1. Runnning the application on Docker

Download spending-app directory (e.g. using git clone) and execute the following commands:

`cd spending-app/docker-compose`

`sudo docker-compose build`

`sudo docker-compose up -d`

The application will be accessible at localhost:5000. To find the docker container ip address use the command 

`sudo docker logs docker-compose_spending_app_1 -f`


## 2. Running the application locally (for development purposes)

Note: To run the application locally, you need a PostgreSQL instance on Docker and Python 3.10+ installed. 
Execute the commands from the first point. The required libraries are listed in the 'requirements.txt' file (they can be installed with `python3 -m pip install -r requirements.txt`).

Once the postgres instance on Docker is running execute 

`sudo docker inspect docker-compose_app_database_service_1` 

and find the IPAddress value in "Networks" field (e.g. 172.20.0.2). Next edit the
*docker-compose/.env* file and assign found ip address to the SERVICE_NAME field (see the commented line in the .env file).

To run the application execute

`python3 main.py` 

Then, open browser and go to localhost:5001

## 3. Usage of the application

The navigation bar provides three links. The "Add new spending" allows users to add a new spending entry and also provides the ability to add a new category or remove an existing category.

![alt text](https://raw.githubusercontent.com/wbonicki/spending_app/main/screens/adding_new_spending.png)

There are two types of categories: the main category (e.g. food) and the more specific subcategory (e.g. fruits). Users must determine the type of category they are adding.

![alt text](https://raw.githubusercontent.com/wbonicki/spending_app/main/screens/adding_new_category.png)

"Analyze spending" displays all spending the user has added.

![alt text](https://raw.githubusercontent.com/wbonicki/spending_app/main/screens/all_spendings.png).

A spending summary for a selected month can be viewed by choosing a date. It is also possible to view summaries for all months.

![alt text](https://raw.githubusercontent.com/wbonicki/spending_app/main/screens/grouped_spending.png).

## 4. Running tests

Important: database operations are tested on test database which can be built with the *docker-compose.testdb.yml* file with the command

`sudo docker-compose -f docker-compose.testdb.yml up -d`

Go to the spending-app/tests directory. Unittests can be run with the following command.

`python3 -m unittest discover -v`

Note: all unittests except tests related to database operations are run during the docker-compose build process (check the Dockerfile for details).



