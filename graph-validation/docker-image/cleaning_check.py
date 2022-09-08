# Jobs that need cleaned datasets
jobs_with_cleaning = [
    "classification",
    "regression",
    "clustering",
    "function"
]

# Jobs that need dirty datasets
jobs_with_no_cleaning = [
    "data-join"
]

""" Global Variables """
not_cleaned = "not_cleaned"
cleaned = "cleaned"

# Not ready yet
def cleaning_handler(playbook):
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

    # Assume that it is valid
    valid_cleaning = [True]
    
    # for each starting job, start the analysis
    print("[INFO] Starting the Depth-First Algorithm.")
    for starting_job_step in starting_jobs:
        job = jobs_dict[starting_job_step]
        # navigate through all the jobs and execute them in the right order
        jobs(starting_job_step, jobs_dict, jobs_anwers_dict, playbook, joins, valid_cleaning)

    return  valid_cleaning[0]   # True/False

# Access jobs by viewing them Depth-first O(N)
def jobs(job_step, jobs_dict, jobs_anwers_dict, playbook, joins, valid_cleaning):
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
            job_requestor(jobs_dict[job_step], jobs_anwers_dict, playbook, valid_cleaning)
    else:
        job_requestor(jobs_dict[job_step], jobs_anwers_dict, playbook, valid_cleaning)

    # Depth-first approach
    next_steps = jobs_dict[job_step]["next"]
    for step in next_steps:
        if(step == 0): # If ther is no next job then do not try to go deeper
            pass
        elif(flagged == True): # If this job is flagged do not try to go deeper
            pass
        else:
            jobs(step, jobs_dict, jobs_anwers_dict, playbook, joins, valid_cleaning)
            
    return

# Request a job
def job_requestor(job_json, jobs_anwers_dict, playbook, valid_cleaning):
    title = job_json["title"]
    step = job_json["step"]
    from_step = job_json["from"]

    # If this is a starting job, then the Dataset is not cleaned.
    if(from_step == 0):
        jobs_anwers_dict[step] = not_cleaned
        return
    
    # If this is a cleaning job, then the Dataset is now cleaned.
    if(title == "cleaning"):
        jobs_anwers_dict[step] = cleaned
        return
    
    # Cleaned --> Cleaned/Not Cleaned (If function)
    if(title in jobs_with_cleaning):
        # If it is not cleaned then valid_cleaning = False
        if(title == "function"):
            for f_step in from_step:
                if(jobs_anwers_dict[f_step] == not_cleaned):
                    jobs_anwers_dict[step] = jobs_anwers_dict[f_step]
                    valid_cleaning[0] = False
                    return
            # If the above are ok then mark as not cleaned
            jobs_anwers_dict[step] = not_cleaned
        else:
            if(jobs_anwers_dict[from_step] == not_cleaned):
                jobs_anwers_dict[step] = jobs_anwers_dict[from_step]
                valid_cleaning[0] = False
                return
            # If the above are ok then mark as cleaned
            jobs_anwers_dict[step] = cleaned
        return
    
    # Not cleaned --> Not cleaned
    if(title in jobs_with_no_cleaning):
        for f_step in from_step:
            if(jobs_anwers_dict[f_step] == cleaned):
                jobs_anwers_dict[step] = jobs_anwers_dict[f_step]
                valid_cleaning[0] = False
                return
        # If the above are ok then mark as not cleaned
        jobs_anwers_dict[step] = not_cleaned
        return
    
    # If nothing from the above then keep the last state
    jobs_anwers_dict[step] = jobs_anwers_dict[from_step]
    return