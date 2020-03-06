# FastApi
The code above performs various CRUD operations with help of [fastapi](https://fastapi.tiangolo.com/) and 
[mongodb](https://docs.mongodb.com/). 

The code above is written using fastapi with help of asynchronous frameworks that provide high-performance network and 
web-servers, database connection libraries, distributed task queues, etc.

## Dependencies & Requirements

The python version used is 3.8+ and runs on [uvicorn](https://www.uvicorn.org/) server. 

To install python 3.8 use the command below.
```bash
 sudo add-apt-repository ppa:deadsnakes/ppa
 sudo apt-get update
 sudo apt-get install python3.8
    
 sudo apt-get install python3.8-venv python3.8-dev

```

You can install uvicorn, fastapi and mongodb using the python package manager 
[pip3](https://pip.pypa.io/en/stable/installing/) and running the requirements.txt file.
```bash
 pip3 intall -r requirements.txt
```
Before running the above command make sure you have a local environment.

## Running the Program

To run the program use the command below
```bash
 uvicorn app:app --reload
```




