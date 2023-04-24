# Import custom Classes
from MongoDB_Class import MongoDB_Class

# Variables for graph validation results
valid = "valid"
invalid = "invalid"
suggested = "suggested"

# Cleaning check Handler
def feature_handler(playbook):
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

    # Use a dictionary as a storage for each job answer
    jobs_anwers_dict = {}
    joins = {}

    # Assume that it is valid ["result", "reason"]
    feature_validity = [valid, "dummy reason"]
    
    # for each starting job, start the analysis
    print("[INFO] Starting the Depth-First Algorithm.")
    for starting_job_step in starting_jobs:
        job = jobs_dict[starting_job_step]
        # navigate through all the jobs and execute them in the right order
        jobs(starting_job_step, jobs_dict, jobs_anwers_dict, playbook, joins, feature_validity)

    return  feature_validity   # [validity, reason]

# Access jobs by viewing them Depth-first O(N)
def jobs(job_step, jobs_dict, jobs_anwers_dict, playbook, joins, feature_validity):
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
            job_requestor(jobs_dict[job_step], jobs_anwers_dict, playbook, feature_validity)
    else:
        job_requestor(jobs_dict[job_step], jobs_anwers_dict, playbook, feature_validity)

    # Depth-first approach
    next_steps = jobs_dict[job_step]["next"]
    for step in next_steps:
        if(step == 0): # If ther is no next job then do not try to go deeper
            pass
        elif(flagged == True): # If this job is flagged do not try to go deeper
            pass
        else:
            jobs(step, jobs_dict, jobs_anwers_dict, playbook, joins, feature_validity)
            
    return

# Request a job
def job_requestor(job_json, jobs_anwers_dict, playbook, feature_validity):
    # If the features are not right then stop
    if (feature_validity[0] == invalid):
        return

    title = job_json["title"]
    step = job_json["step"]
    from_step = job_json["from"]

    if(title == "dataset"):
        # Initialize dataset
        mongo_obj = MongoDB_Class()
        mongo_record = {"organization": playbook["database-id"], "label": job_json["label"]}
        mongo_doc = mongo_obj.getMongoRecord(mongo_record)
        dataset_comlpex_features = mongo_doc["features"]
        features = []
        for feature in dataset_comlpex_features:
            # features.append(feature["name"]) # Feature update
            features.append(feature)
        jobs_anwers_dict[step] = features
        return
    
    if(title == "function"):
        # Find if features are right
        func_args = job_json["function"]["args"]
        from_steps = from_step
        from_counter = 0
        for func_arg in func_args:
            if "feature" in func_arg:
                # Check if feature given exists
                features = jobs_anwers_dict[from_steps[from_counter]]
                feature = func_arg["feature"]
                if(not (feature in features)):
                    feature_validity[0] = invalid
                    feature_validity[1] = "Feature '"+feature+"' does not exist in the features: "+ str(features)
                    return
                # Update value to check the next one
                from_counter += 1
        # New dataset will be the below
        jobs_anwers_dict[step] = ["result"]
        return
    
    if(title == "data-join"):
        # Find if column given is right
        from_features_1 = jobs_anwers_dict[from_step[0]]
        from_features_2 = jobs_anwers_dict[from_step[1]]
        feature = job_json["column"]

        if(not (feature in from_features_1)):
            feature_validity[0] = invalid
            feature_validity[1] = "Join: Feature '"+feature+"' does not exist in the features: "+ str(from_features_1)
            return
        
        if(not (feature in from_features_2)):
            feature_validity[0] = invalid
            feature_validity[1] = "Join: Feature '"+feature+"' does not exist in the features: "+ str(from_features_2)
            return

        # Build the join features
        join_features = []
        join_features.extend(from_features_1)
        join_features.extend(from_features_2)
        join_features.remove(feature)

        # New dataset will be the below
        jobs_anwers_dict[step] = join_features
        return
    
    if(title == "regression"):
        # Find if column given is right
        from_features = jobs_anwers_dict[from_step]
        feature = job_json["column"]

        if(not (feature in from_features)):
            feature_validity[0] = invalid
            feature_validity[1] = "Regression: Feature '"+feature+"' does not exist in the features: "+ str(from_features)
            return

        # New dataset will be the below
        jobs_anwers_dict[step] = [feature, "prediction"]
        return
    
    if(title == "classification"): 
        # Find if column given is right
        from_features = jobs_anwers_dict[from_step]
        feature = job_json["column"]

        if(not (feature in from_features)):
            feature_validity[0] = invalid
            feature_validity[1] = "Classification: Feature '"+feature+"' does not exist in the features: "+ str(from_features)
            return
        
        # New dataset will be the below
        jobs_anwers_dict[step] = [feature, "prediction"]
        return
    
    if(title == "clustering"): ### This code could have changes in the future

        """
        # Find if column given is right
        from_features = jobs_anwers_dict[from_step]
        feature = job_json["column"]

        if(not (feature in from_features)):
            feature_validity[0] = invalid
            feature_validity[1] = "Clustering: Feature '"+feature+"' does not exist in the features: "+ str(from_features)
            return
        # New dataset will be the below
        """

        # New dataset will be the below
        ### THIS MUST HAVE THE END RESULTS
        from_features = jobs_anwers_dict[from_step]
        from_features.append("prediction")
        jobs_anwers_dict[step] = from_features
        # jobs_anwers_dict[step] = [feature, "prediction"]
        return

    jobs_anwers_dict[step] = jobs_anwers_dict[from_step]
    return