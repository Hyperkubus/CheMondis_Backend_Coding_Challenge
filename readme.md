# CheMondis Coding Challenge
This repository is my proposed solution to the coding challenge I got send by CheMondis.   
The task assignment can be found [here](doc/Backend%20Coding%20Challenge.pdf).

This solution is crafted by utilizing the Django Rest Framework.

### Quickstart
run the docker-compose setup by calling
```
docker-compose up
```
After start up you should reach the api under http://localhost:80/  
Currently there is just one request endpoint: `/weather/<cityname>/`  
Where `<cityname>` can be substituted for the desired city (e.g.: Cologne)  