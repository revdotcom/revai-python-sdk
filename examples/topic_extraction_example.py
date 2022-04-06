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


import time
from rev_ai import topic_extraction_client


"""String containing your access token"""
access_token = "your_access_token"

"""Submit a job with whatever text you want by changing this input"""
text = "input text"
transcript_json = None

"""Create your api client"""
client = topic_extraction_client.TopicExtractionClient(access_token)

"""If you'd like to submit the transcript of an existing transcription job you can do so by
uncommenting the lines below

async_job_id = "your_job_id"
async_api_client = apiclient.RevAiAPIClient(access_token)
transcript = api_client.get_transcript_object(async_job_id)
transcript_json = transcript
text = None
"""

"""Submitting a job with either text or json. Only one can be provided per submission"""
job = client.submit_job(text=text, json=transcript_json)
print("Submitted Job")

while True:

    """Obtains details of a job in json format"""
    job_details = client.get_job_details(job.id)
    status = job_details.status.name

    print("Job Status : {}".format(status))

    """Checks if the job has been completed. Please note that this is not the recommended way
    of getting job status in a real application. For recommended methods of getting job status
    please see our documentation on callback_urls here:
    https://docs.rev.ai/resources/tutorials/get-started-api-webhooks/
    """
    if status == "IN_PROGRESS":
        time.sleep(2)
        continue

    elif status == "FAILED":
        print("Job Failed : {}".format(job_details.failure_detail))
        break

    if status == "COMPLETED":
        """Getting a list of current topic extraction jobs connected with your account
        The optional parameters limits the length of the list.
        starting_after is a job id which causes the removal of
        all jobs from the list which were created before that job
        """
        list_of_jobs = client.get_list_of_jobs(limit=None, starting_after=None)

        """obtain a list of topics and their scores for the job"""
        result = client.get_result_object(job.id, threshold=None)
        remove_none_elements = lambda dictionary: {
            key: value for key, value in dictionary.items() if value}
        print([{
            'topic': topic.topic_name,
            'score': topic.score,
            'informants': [
                remove_none_elements(informant.__dict__) for informant in topic.informants
            ]
        } for topic in result.topics])

        break
"""Use the objects however you please
Once you are done with the job, you can delete it.
NOTE : This will PERMANENTLY DELETE all data related to a job. Exercise only
if you're sure you want to delete the job.

client.delete_job(job.id)
"""
print("Job Submission and Collection Finished.")
