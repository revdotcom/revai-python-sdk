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
from rev_ai import apiclient, JobStatus
from rev_ai.models.asynchronous.translation_job_status import TranslationJobStatus
from rev_ai.models.asynchronous.translation_language_options import TranslationLanguageOptions
from rev_ai.models.asynchronous.translation_options import TranslationOptions
from rev_ai.models.asynchronous.translation_model import TranslationModel

# String containing your access token
access_token = "<your_access_token>"

# Create your api client
client = apiclient.RevAiAPIClient(access_token)

# Submitting a job through a local file.
#
# job = client.submit_job_local_file("your_local_file_path",
#                             delete_after_seconds=2592000,
#                             language='en',
#                             translation_config=TranslationOptions(
#                                 target_languages=[
#                                     TranslationLanguageOptions("es", TranslationModel.PREMIUM)
#                                 ]
#                             ))


# Submitting a job with a link to the file you want transcribed and translated
url = "https://www.rev.ai/FTC_Sample_1.mp3"
job = client.submit_job_url(media_url=url,
                            delete_after_seconds=2592000,
                            language='en',
                            translation_config=TranslationOptions(
                                target_languages=[
                                    TranslationLanguageOptions("es", TranslationModel.PREMIUM)
                                ]
                            ))

print("Submitted Job")
print("Job Status : {}".format(job.status))

# Checks if the job has been transcribed and summarized. Please note that this is not the recommended way
# of getting job status in a real application. For recommended methods of getting job status
# please see our documentation on setting a callback url here:
# https://docs.rev.ai/resources/tutorials/get-started-api-webhooks/

while job.status == JobStatus.IN_PROGRESS:
    time.sleep(5)
    # Obtains details of a job in json format
    job = client.get_job_details(job.id)
    print("Job Status : {}".format(job.status))

if job.status == JobStatus.FAILED:
    print("Job Failed : {}".format(job.failure_detail))
    exit()

if job.status == JobStatus.TRANSCRIBED:
    print("Translation Status : {}".format(job.translation.target_languages[0].status))
    # Checks if the job has been summarized. Please note that this is not the recommended way
    # of getting job status in a real application. For recommended methods of getting job status
    # please see our documentation on setting a callback url here:
    # https://docs.rev.ai/resources/tutorials/get-started-api-webhooks/
    while job.translation.target_languages[0].status == TranslationJobStatus.IN_PROGRESS:
        time.sleep(5)
        # Obtains details of a job in json format
        job = client.get_job_details(job.id)
        print("Translation Status : {}".format(job.translation.target_languages[0].status))

if job.translation.target_languages[0].status == TranslationJobStatus.FAILED:
    print("Translation Failed : {}".format(job.translation.target_languages[0].failure))
    exit()

# obtain transcript translation as a string for the job.
transcript_text = client.get_translated_transcript_text(job.id, 'es')
print(transcript_text)

# obtain transcript translation as a json object for the job.
transcript_json = client.get_translated_transcript_json(job.id, 'es')

# obtain transcript translation object for the job.
transcript_obj = client.get_translated_transcript_object(job.id, 'es')

# obtain translated captions for the job.
captions = client.get_translated_captions(job.id, 'es')

# Use the objects however you please

# Once you are done with the job, you can delete it.
# NOTE : This will PERMANENTLY DELETE all data related to a job. Exercise only
# if you're sure you want to delete the job.
# client.delete_job(job.id)
print("Job Submission and Collection Finished.")
