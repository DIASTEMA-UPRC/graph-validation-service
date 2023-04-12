# Import Libraries
import os

# Import custom Functions for jobs
from accessibility_check import access_handler
from cleaning_check import cleaning_handler
from features_check import feature_handler
from connections_check import connections_handler

# Diastema Token Environment Variable
DIASTEMA_KEY = os.getenv("DIASTEMA_KEY", "diastema-key")

# Attributes that the playbook must have
needed_attributes = [
        "diastema-token",
        "analysis-id",
        "database-id",
        "jobs",
        "metadata"
    ]

# All the existing jobs for Diastema
existing_jobs = [
        "dataset",
        "cleaning",
        "data-join",
        "classification",
        "regression",
        "clustering",
        "visualization",
        "function",
        "data-sink"
    ]

# Jobs that are allowed to start the playbook
allowed_starting_jobs = [
    "dataset",
    "function"
]

# Jobs that are allowed to end the playbook
allowed_ending_jobs = [
    "data-sink",
    "visualization"
]

# Variables for graph validation results
valid = "valid"
invalid = "invalid"
suggested = "suggested"

def playbook_check(playbook):
    # Check if there is a playbook
    if playbook is None:
        print("[ERROR] No Diastema playbook given!")
        return (invalid, "No Diastema playbook given!")
    
    # Check if the needed_attributes exist only one time in the playbook
    for attribute in needed_attributes:
        if not (attribute in playbook):
            error = "Missing attribute: "+attribute
            print("[ERROR]", error)
            return (invalid, error)

    # Check if the "diastema-token" is correct
    if playbook["diastema-token"] != DIASTEMA_KEY:
        print("[ERROR] Invalid Diastema Token!")
        return (invalid, "Invalid Diastema Token!")
    
    # Check if all the jobs exist in the playbook
    jobs = playbook["jobs"]
    for job in jobs:
        if not (job["title"] in existing_jobs):
            error = "Wrong job title: "+job["title"]+" ("+str(job["id"])+")"
            print("[ERROR]", error)
            return (invalid, error)
    
    # Ckeck if there is at least one starting job
    noStart = True
    for job in jobs:
        if not (type(job["from"]) == list):
            if job["from"] == 0:
                noStart = False
    if noStart:
        error = "There is no starting jobs."
        print("[ERROR]", error)
        return (invalid, error)
    
    # Check if starting jobs are allowed to start the playbook
    for job in jobs:
        if not (type(job["from"]) == list):
            if job["from"] == 0:
                if not (job["title"] in allowed_starting_jobs):
                    error = "Job not valid as a starting job: "+job["title"]+" ("+str(job["id"])+")"
                    print("[ERROR]", error)
                    return (invalid, error)

    # Ckeck if there is at least one ending job
    noEnd = True
    for job in jobs:
        if job["next"] == [0]:
            noEnd = False
    if noEnd:
        error = "There is no ending jobs."
        print("[ERROR]", error)
        return (invalid, error)

    # Check if ending jobs are allowed to end the playbook
    for job in jobs:
        if job["next"] == [0]:
            if not (job["title"] in allowed_ending_jobs):
                error = "Job not valid as an ending job: "+job["title"]+" ("+str(job["id"])+")"
                print("[ERROR]", error)
                return (invalid, error)
    
    # Check if the graph is connected in the right way
    nodes_found = access_handler(playbook)
    if nodes_found != len(jobs):
        error = "There are some jobs that are not accessible!"
        print("[ERROR]", error)
        return (invalid, error)
    
    # Check all the outputs and inputs of the nodes
    connection_validation = connections_handler(playbook)
    if(connection_validation[0] == invalid):
        error = connection_validation[1]
        print("[ERROR]", error)
        return (invalid, error)

    # Use MongoDB to find if the features are making sence
    feature_validation = feature_handler(playbook)
    if(feature_validation[0] == invalid):
        error = feature_validation[1]
        print("[ERROR]", error)
        return (invalid, error)

    

    # Check for cleaning issues
    # not clean --> Join --> not clean
    # clean --> Reg, Class, Clus --> X (clean)
    # clean --> Function --> not clean
    cleaning_validation = cleaning_handler(playbook)
    
    if(cleaning_validation[0] == invalid):
        error = cleaning_validation[1]
        print("[ERROR]", error)
        return (invalid, error)

    if(cleaning_validation[0] == suggested):
        error = cleaning_validation[1]
        print("[SUGGESTION]", error)
        return (suggested, error)

    print("[INFO]", "Valid playbook")
    return (valid, "Valid playbook")
