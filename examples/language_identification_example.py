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
from rev_ai import language_identification_client, apiclient


# String containing your access token
access_token = "028Rd-PdaRGCV8JOFKSFmawQShU0vI88nTBH0qCNwkayoQyGBEWMnjyvssEzsdnGi9NGgZUyN4P-NBSTykFySUSVL_nUo"

# Create your api client
client = language_identification_client.LanguageIdentificationClient(access_token)

# Submitting a job with a link to the file you want to identify the language of
# Change url to your url
url = "https://www.rev.ai/FTC_Sample_1.mp3"
job = client.submit_job_url(url,
                            metadata=None,
                            callback_url=None,
                            delete_after_seconds=None)

print("Submitted Job")

while True:
    # Obtains details of a job in json format
    job_details = client.get_job_details(job.id)
    status = job_details.status.name

    print("Job Status : {}".format(status))

    # Checks if the job has been completed. Please note that this is not the recommended way
    # of getting job status in a real application. For recommended methods of getting job status
    # please see our documentation on callback_urls here:
    # https://docs.rev.ai/resources/tutorials/get-started-api-webhooks/
    if status == "IN_PROGRESS":
        time.sleep(2)
        continue

    elif status == "FAILED":
        print("Job Failed : {}".format(job_details.failure_detail))
        break

    if status == "COMPLETED":
        # Getting a list of current language identification jobs connected with your account
        # The optional parameters limits the length of the list.
        # starting_after is a job id which causes the removal of
        # all jobs from the list which were created before that job
        list_of_jobs = client.get_list_of_jobs(limit=None, starting_after=None)

        # obtain the most probable language spoken and a list of other possible languages and their confidence scores
        result = client.get_result_object(job.id)
        print(result.top_language)
        print([{
            'language': language_confidence.language,
            'confidence': language_confidence.confidence
        } for language_confidence in result.language_confidences])

        break

# Use the objects however you please
# Once you are done with the job, you can delete it.
# NOTE : This will PERMANENTLY DELETE all data related to a job. Exercise only
# if you're sure you want to delete the job.
#
# client.delete_job(job.id)

print("Job Submission and Collection Finished.")
