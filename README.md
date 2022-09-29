# Graph Validation Service

## Description
DIASTEMA uses a service to verify the integrity of the Diastema playbook before it is given to the Orchestration Service for execution [[1]](https://github.com/DIASTEMA-UPRC/graph-validation-service/blob/main/README.md#references).

This system receives a JSON graph that mentions in it all the necessary information for the execution of all procedures. This information refers to which jobs should run first before others, what job each one is, various variables, ids, and more.

The purpose od this service is to check whether the graph is valid or not for the execution of the Orchestrator. It does this, by accessing all the jobs and attributes of the playbook, while trying to find missing values, non logical links etc.

Two interesting functionalities of the above, is the ability to handle dinamicly witch features of the datasets given are corrent to assist the end-users with friendly messages, as well as the ability to know when a dataset is in need, is suggested, or not to have a cleaning job performed using the Data Verifier Service.

## Repository Contents
- graph-validation/docker-image
  - The source code of the Graph Validation Service. It also contains a python virtual environment with all the needed libraries.
- graph-validation/dummy/analyzes
  - Some dummy JSONs that are valid. To check how the service is retarning the OK status.
- graph-validation/dummy/wrong-analyzes/
  - Some dummy JSONs that are not valid. To check how the service is retarning the CONFLICT status.
- graph-validation/dummy/data-verifier/
  - A dummy JSON used as an example of the HTTP call's JSON body for the Data Verifier Service given by the Graph Validation Service.
- graph-validation/dummy-data-verifier/
  - A dummy Data Verifier Service for testing purposes.

The repositories below, contain Dockerfiles, giving the opportunity to use them with Docker if needed.
- graph-validation/docker-image
- graph-validation/dummy-data-verifier/

## Example of use
In this section, an example of how to use the source code of this repository is shown, using the files from the dummyrepositories.

### Prerequisites
Below is an example of prerequisites:
- Docker
- Windows OS
- Postman
- MongoDB

You can execute the functionality with other prerequisites and commands as well!

#### Docker
1. Make sure that you are running Docker on your Machine.

#### Service Startup
2. Clone this repository on your Machine.
3. Go to the directory below using a CMD:
- graph-validation/docker-image/
4. Type the two following commands in the CMD:
```
docker build --tag graph-validation-image .
```
```
docker run -p 127.0.0.1:5000:5000 ^
--name graph-validation-service ^
--restart always ^
-e HOST=0.0.0.0 ^
-e PORT=5000 ^
-e DIASTEMA_KEY=diastema-key ^
-e MONGO_HOST=host.docker.internal ^
-e MONGO_PORT=27017 ^
-e DATABASE=UIDB ^
-e COLLECTION=datasets ^
-e DATA_VERIFIER_HOST=host.docker.internal ^
-e DATA_VERIFIER_PORT=5001 ^
graph-validation-image
```
Now you have activated the service in your Machine.

You should also activate the dummy Service to test the above.
5. Go to the directory below using a CMD:
- graph-validation/dummy-data-verifier/
6. Type the two following commands in the CMD:
```
docker build --tag dummy-data-verifier .
```
```
docker run -p 127.0.0.1:5001:5000 ^
--name dummy-data-verifier-service ^
--restart always ^
-e HOST=0.0.0.0 ^
-e PORT=5000 ^
dummy-data-verifier
```
#### Mongo Dummy Initialization
7. Use another CMD and type the mongo command
```
mongo
```
The command above will let you in the mongo shell.
8. Now initialize two dummy datasets by typing the commands below
```
use UIDB
db.dropDatabase()
use UIDB
db.datasets.insert( { "organization": "metis", "user": "panagiotis", "label": "ships", "features" : [ "ships-1", "ships-2", "ships-3" ] } )
db.datasets.insert( { "organization": "metis", "user": "panagiotis", "label": "boats", "features" : [ "boats-1", "boats-2", "boats-3" ] } )
cls
db.datasets.find()

```

#### Usage
9. Open Postman and execute the following requests:
- Valid Graph:
   - POST
   - URL: http://localhost:5000/validation
   - JSON BODY: The "join-with-classification.json" from the repository named "graph-validation/dummy/analyzes/"
- Not Valid Graph:
   - POST
   - URL: http://localhost:5000/validation
   - JSON BODY: The "no-attribute.json" from the repository named "graph-validation/dummy/wrong-analyzes/"

By executing the above you will get the following with the corresponding meanings:
- Valid Graph: STATUS 200 OK - Your Graph is valid and ready to be used by the Orchestrator.
- Not Valid Graph: STATUS 409 CONFLICT - Your Graph is problematic and you can view the TEXT in the body of your response to fix it.
- Graph Suggestion: STATUS 425 TOO EARLY - Your Graph is not problematic but there is one suggestion given in the TEXT body of the response.

There are many more Dummy JSON bodies that you can use in the following directories:
- graph-validation/dummy/analyzes
- graph-validation/dummy/wrong-analyzes/

#### Usage
If needed, you can change the values in the Docker commands to change hosts, ports, keys as well as the databse and collection used.

## References
- [1] https://diastema.gr/
