"""Copyright 2019 REV

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from rev_ai import apiclient, streamingclient
from rev_ai.models import MediaConfig
import json
import time

access_token = "your_access_token"

#Create your api client
client = apiclient.RevAiAPIClient(access_token)

#Submitting a job through a local file. The optional parameters are shown below.
job = client.submit_job_local_file("your_local_file_path",
                                   metadata=None,
                                   callback_url=None,
                                   skip_diarization=False,
                                   custom_vocabularies=None)

#Submitting a job with a link to the file you want transcribed
# job = client.submit_job_url("your_local_file_path",
#                             metadata=None,
#                             allback_url=None,
#                             skip_diarization=False,
#                             custom_vocabularies=None)

while True:
    #obtains details of a job in json format
    job_details = client.get_job_details(job.id)
    details_dict = json.loads(job_details)
    status = details_dict["status"]
    #Checks if the job has been transcribed
    if status == "in_progress":
        time.sleep(5)
        continue
    elif status == "failure":
        #Do something if the job failed
        break
    break

#If you want to check the current jobs connected with your account
#The optional parameters limits limits the length of the list. Starting_after
#
list_of_jobs = client.get_list_of_jobs(limits=None, starting_after=None)


#obtain transcript text as a string for the job.id.
transcript_text = client.get_transcript_text(job.id)

#obtain transcript text as a json object for the job.id.
transcript_json = client.get_transcript_json(job.id)

#obtain transcript object for the job.id.
transcript_obj = client.get_transcript_object(job.id)

#obtain captions for the job.id.
captions = client.get_captions(job.id)

#Now that we are done with the job, we can delete it.
#NOTE : This will PERMANENTLY DELETE all data related to a job. Exercise only
#if sure you want to delete the job.
client.delete_job(job.id)
