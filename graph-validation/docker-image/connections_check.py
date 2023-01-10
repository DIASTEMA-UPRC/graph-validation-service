# Variables for graph validation results
valid = "valid"
invalid = "invalid"
suggested = "suggested"

one_input_jobs = [
    "cleaning",
    "regression",
    "classification",
    "clustering",
    "visualization"
]

# Cleaning check Handler
def connections_handler(playbook):
    # The jobs of the playbook.
    json_jobs = playbook["jobs"]

    for job in json_jobs:
        if job["title"] in one_input_jobs:
            if type(job["from"]) == list:
                return [invalid, "This job can have only one input: "+job["title"]+" ("+str(job["id"])+")"]
            
        if job["title"] == "data-join":
            if type(job["from"]) != list:
                return [invalid, "This job must have two inputs: "+job["title"]+" ("+str(job["id"])+")"]
            if len(job["from"]) != 2:
                return [invalid, "This job must have two inputs: "+job["title"]+" ("+str(job["id"])+")"]

    return [valid, "dummy reason"]