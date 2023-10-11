# Student Score Tracking System

The Student Score Tracking System is a web application developed using Python (Bottle), Ember.js, and MySQL. It allows users to track student scores across different subjects and quarters. The application is Dockerized, enabling easy deployment and scaling.


## Features

- Track student scores in various subjects and quarters.
- Create and manage student records.
- Display data with interactive charts.
- Dockerized for easy deployment.
- RESTful API for integration with other systems.

## Implemented Features

At the moment following aspects of the task have been completed:
- App is dockerized
- Back end api for the front-end
- DB connection
- on initial app start DB is populated with data from .csv file
- frontend server
- communication between front-end and back-end
- front-end endpoints: 
  - http://localhost:4200
  - http://localhost:4200/students
  - http://localhost:4200/student/1

Following things to be accomplished
- required charts for student's scores
- form to add scores/students
- styles for the frontend

## Installation

To run the project locally follow these steps:

   ```shell
    git clone https://github.com/Valentine-VL/students_scores_test_app.git
   
    cd softimpact_task
   
    docker-compose up --build -d
```
After build is complete you will be able to see the project on http://localhost:4200
