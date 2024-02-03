# CheMondis Coding Challenge
This repository is my proposed solution to the coding challenge I got send by CheMondis.   
The task assignment can be found in [doc/Backend_Coding_Challenge.pdf](doc/Backend_Coding_Challenge.pdf).

### Quickstart
Run the docker-compose setup by calling `docker-compose up`  
After start up you can reach the api under http://localhost/api/v1/  
You can access the Specification at http://localhost/api/schema/  
This includes a swagger-ui at http://localhost/api/schema/swagger-ui/  
as well as a redoc at http://localhost/api/schema/redoc/  

### Overview
This solution is crafted by utilizing the following technologies:
- Django
  - The Challenge called for Django so we obviously need to use it
- Django Rest Framework
  - Speaks for its self
- DRF_spectacular
  - for specification generation and accessibility
- Docker
  - to make the project easily executable
- Docker-compose
  - to easily run the project and its dependencies
- Redis
  - to cache the responses
- Postgres (although technically not needed)
  - we are currently not storing any data in the database but might do later (e.g. city lookup)

### Configuration
Application configuriation (Cache_TTL, etc.) can be found in `src/weatherApi/.env`