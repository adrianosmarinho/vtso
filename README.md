# VTSO

This repository contains the VTSO (Vessel Traffic Service Operator) exercise developed for JosephMark.
You can see the original exercise prompt in the Prompt section further ahead.

## Project Overview

The VTSO project contains a backend API that is part of a system being developed for Vessel Traffic Service Operators (VTSO). The API allows it is users to:

- list all the ships in the system
- list all the harbours in the system
- list all the visits a ship has paid to a harbour
- list all the companies that operate ships
- list all employees (people) in the system
- filter ships by type
- list harbours visited by a particular ship
- list ships currently docked in a particular harbour
- create new company, person, ship, harbour and visit entries
- edit the details of a given ship


## Features

- Project is implemented in Django and Django Rest Framework
- Pipenv for managing dependencies
- Docker support for containerization
- API follows REST principles
- API is protected with DRF Token Authentication
- Endpoint for Swagger Documentation
- Unit tests written in pytest

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Pipenv
- Docker (optional, for containerization)

### Installation

1. Clone the repository:
```sh
    git clone https://github.com/adrianosmarinho/vtso.git
    cd vtso
```

2. Install dependencies:
```sh
    pipenv shell
    pipenv install
```

Note: `pipenv shell` will create and activate a virtual environment.

3. Apply migrations:
```sh
python manage.py migrate
```

4. Ensure the OpenAPI Schema is up to date

```sh
python manage.py spectacular --file schema.yaml
```

5. Run the development server:
```sh
python manage.py runserver
```

Access the web application at `http://localhost:8000`

### Docker Setup

1. Build and Run the Docker Image with Docker Compose

```sh
docker-compose up --build -d
```

The above command will run in detached mode. Access the application at `http://localhost:8001`.

To stop the container run:
    
```sh
docker-compose down
```

## Usage

- If running the system for the first time, you will need to create a super user. You can the create other users while logged in as the super user.
    
```sh
python manage.py createsuperuser
```
- To create other Users, login as a superuser on Django admin (`http://localhost:8001/admin/`)

- You cannot make api requests without a Token. You can create a Token for User using the Django admin site. Or you can make a POST request to /tokens/obtain/ passing the username and password of a User.

- Once you have a Token, any requests to the API must include the Token in the Authorization header. For example:

```sh
curl -X GET http://127.0.0.1:8001/vtso/companies/ -H 'Authorization: Token <your token here>'
```

- For a list of available endpoints, go to `http://127.0.0.1:8001/api/schema/swagger-ui/`.

## Testing
The project contains unit tests for the Views and Models. To run the tests, clone the repository, change to its root directory and run `pytest`.


## Original Prompt
<details>
  <summary>Click here to see the original exercise prompt</summary>
  
### Overview
Your task is to create a backend API part of a system that is being developed for Vessel Traffic Service operators (VTSO). The operators need to be able to find out information about various ships that visit their harbours. Information that needs to be recorded for ships includes the name, tonnage, draft (under max load and dry), type (one of these types only: bulk carrier, fishing, submarine, tanker, cruise ship), beam and length, flag, year built and the operating company. The operating company has a contact person with a local phone number and contact email as well.

Of primary importance to the VTSOs is to be able to record when a ship enters and exits a harbour they manage. They also need to be able to find out what other harbours a particular ship has entered and when. Harbours have a name, a maximum berth depth, a harbour master (which is the person who manages the harbour) and exist in a particular location- which is represented by a city and country (do not worry about using a geographical system or latitude/longitude).

### Tech stack / scope
- Please use Django and Django Rest Framework, and follow RESTful principles where possible
 - https://www.djangoproject.com/
 - https://www.django-rest-framework.org/

- You can use whatever database system you like

- You do not need to use a GIS based database

### Primary Objectives
1. Please create models in django to represent the situation described above
you may find it helpful to create an ER diagram and/or a tech spec first

2. Create django admin pages for all the models you create
you do not need to create anything too complex but use your own judgement on what fields to show

3. Develop REST endpoints that will be used to:
- create a new ship record
- create a new harbour
- record the date and time when a ship enters a harbour
- record the date and time when a ship leaves a harbour
- update the details of an existing ship

4. Develop REST endpoints that will be used to:
- list all the ships in the system, this should include all information about the ship as well as the current age of the ship in years
- list all the harbours in the system, this should include the id, name, and maximum berth depth only
- get the details about a particular harbour, this should include all information about the harbour as well as a list of what ships are currently in the harbour.
- get details about all the harbours a particular ship has visited. This should include the entry/exit date and times as well as the harbour name.

5. Dockerize the application to ensure that it can be easily deployed and run in any environment.

6. Provide a README file that includes clear instructions on how to set up, run, and test (if applicable) the application.

### Bonus objectives
1. Implement a system to allow users to search for ships by name and filter ships by type
- do this for the endpoint developed for objective 4a and if possible 4c.

2. Write unit tests for your code

3. Protect the endpoints with token based authentication

4. Create documentation using OpenAPI (Swagger)

### Submission
Your code should be submitted as a link to a Git repository.

Include a README file with instructions on how to set up and run the project, including steps to build and run the Docker container.

### Presentation
You are required to demonstrate the functionality of your application. Please prepare to showcase your API through a tool like Postman or any other API client. This demonstration should include showcasing the endpoints working- successful requests and how potential errors are handled.

Additionally, demonstrate the functionality within the Django admin page to show how entities are managed and displayed.

You can run the demonstration locally during your presentation.
Your presentation will be in front of developers (along with members of other disciplines) so you will be expected to show your code and answer questions about it.


</details>

## Futher Work
Here are a list of ideas and/or refinements that can be done in the future:
- Replace the DRF Token Authentication with a more robust alternative. Django Rest Framework recommends Django REST Knox.
- Change the modelling in a way that a User is effectively linked to a Company (operator) and therefore only sees data belonging to Ships operated by their Company.
- Replace the sqlite database with Postgres (or any other engine that is appropriate for a production environment).
- Adjust the Dockerfile and docker-compose so the application can be deployed to a production environment.

## Contact

For any inquiries, please contact Adriano S. Marinho at adrianosmarinho@gmail.com.
