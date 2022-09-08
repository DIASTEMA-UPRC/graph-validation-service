# Graph Validation Service

## Description
DIASTEMA uses a service to verify the integrity of the Diastema playbook before it is given to the Orchestration Service for execution [[1]](https://github.com/DIASTEMA-UPRC/graph-validation-service/blob/main/README.md#references).

This system receives a JSON graph that mentions in it all the necessary information for the execution of all procedures. This information refers to which jobs should run first before others, what job each one is, various variables, ids, and more.

The purpose od this service is to check whether the graph is valid or not for the execution of the Orchestrator. It does this, by accessing all the jobs and attributes of the playbook, while trying to find missing values, non logical links etc.

## Repository Contents
- graph-validation/docker-image
  - The source code of the Graph Validation Service. It also contains a python virtual environment with all the needed libraries.
- graph-validation/dummy/analyzes
  - Some dummy JSONs that are valid. To check how the service is retarning the OK status.
- graph-validation/dummy/wrong-analyzes/
  - Some dummy JSONs that are not valid. To check how the service is retarning the CONFLICT status.

The repository below, contains a Dockerfile, giving the opportunity to use them with Docker if needed.
- graph-validation/docker-image

## Example of use
In this section, an example of how to use the source code of this repository is shown, using the files from the dummyrepositories.

### Prerequisites
Below is an example of prerequisites:
- Docker
- Windows OS
- Postman

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
graph-validation-image
```
Now you have activated the service in your Machine.

#### Usage
5. Open Postman and execute the following requests:
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

There are many more Dummy JSON bodies that you can use in the following directories:
- graph-validation/dummy/analyzes
- graph-validation/dummy/wrong-analyzes/

## References
- [1] https://diastema.gr/
