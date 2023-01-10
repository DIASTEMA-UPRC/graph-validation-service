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

# Handle the playbook
def access_handler(playbook):
    # The jobs of the playbook.
    json_jobs = playbook["jobs"]

    # handle jobs as a dictionary - O(N)
    jobs_dict = {}
    for job in json_jobs:
        jobs_dict[job["step"]] = job
    
    # Find starting jobs - O(N)
    starting_jobs = []
    for job_step, job in jobs_dict.items():
        # print(job_step, '->', job)
        if job["from"] == 0:
            starting_jobs.append(job_step)
    #print(starting_jobs)
    
    print("[INFO] Starting Jobs Found.")

    # Use a dictionary as a storage for each job answer
    jobs_anwers_dict = {}
    joins = {}
    
    # for each starting job, start the analysis
    print("[INFO] Starting the Depth-First Algorithm.")
    for starting_job_step in starting_jobs:
        job = jobs_dict[starting_job_step]
        # navigate through all the jobs and execute them in the right order
        jobs(starting_job_step, jobs_dict, jobs_anwers_dict, playbook, joins)
    
    return len(jobs_anwers_dict)

# Access jobs by viewing them Depth-first O(N)
def jobs(job_step, jobs_dict, jobs_anwers_dict, playbook, joins):
    # If this function never found before then add it in functions dictionary
    flagged = False
    if(type(jobs_dict[job_step]["from"]) == list and not(job_step in joins)):
        joins[job_step] = 1
    elif(type(jobs_dict[job_step]["from"]) == list and (job_step in joins)):
        joins[job_step] += 1
    
    if(type(jobs_dict[job_step]["from"]) == list):
        if(joins[job_step] < len(jobs_dict[job_step]["from"])):
            flagged = True
        else:
            job_requestor(jobs_dict[job_step], jobs_anwers_dict, playbook)
    else:
        job_requestor(jobs_dict[job_step], jobs_anwers_dict, playbook)

    # Depth-first approach
    next_steps = jobs_dict[job_step]["next"]
    for step in next_steps:
        if(step == 0): # If ther is no next job then do not try to go deeper
            pass
        elif(flagged == True): # If this job is flagged do not try to go deeper
            pass
        else:
            jobs(step, jobs_dict, jobs_anwers_dict, playbook, joins)
            
    return

# Request a job
def job_requestor(job_json, jobs_anwers_dict, playbook):
    title = job_json["title"]
    step = job_json["step"]

    if(title in existing_jobs):
        jobs_anwers_dict[step] = "done"

    return