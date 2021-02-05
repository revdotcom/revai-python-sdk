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
from rev_ai import apiclient
from rev_ai.models import CustomVocabulary

# String containing your access token
access_token = "your_access_token"

# Create your api client
client = apiclient.RevAiAPIClient(access_token)

# Construct CustomVocabulary objects using our premade class for ease
mit_professors = CustomVocabulary(
    ["Robert Berwick", "Noam Chomsky", "Evelina Fedorenko"]
)
# Or manually construct CustomVocabulary as such
other_scientists = {"phrases": ["Albert Einstein"]}
# Important: place custom vocabularies in a list before passing them into
# either of client.submit_job_local_file() or client.submit_job_url()
custom_vocabularies = [mit_professors, other_scientists]

# Submitting a job through a local file. The optional parameters
# are shown below.
#
# job = client.submit_job_local_file("your_local_file_path",
#                                    metadata=None,
#                                    callback_url=None,
#                                    skip_diarization=False,
#                                    custom_vocabularies=None,
#                                    filter_profanity=False,
#                                    remove_disfluencies=False,
#                                    delete_after_seconds=None,
#                                    language=None,
#                                    custom_vocabulary_id=None)



# Submitting a job with a link to the file you want transcribed
# Change url to your url, custom_vocabularies is optional like above
url = "https://www.rev.ai/FTC_Sample_1.mp3"
job = client.submit_job_url(url,
                            metadata=None,
                            callback_url=None,
                            skip_diarization=False,
                            custom_vocabularies=custom_vocabularies,
                            filter_profanity=False,
                            remove_disfluencies=False,
                            delete_after_seconds=None,
                            language=None,
                            custom_vocabulary_id=None)

print("Submitted Job")

while True:

    # Obtains details of a job in json format
    job_details = client.get_job_details(job.id)
    status = job_details.status.name

    print("Job Status : {}".format(status))

    # Checks if the job has been transcribed
    if status == "IN_PROGRESS":
        time.sleep(5)
        continue

    elif status == "FAILED":
        print("Job Failed : {}".format(job_details.failure_detail))
        break

    if status == "TRANSCRIBED":
        # Getting a list of current jobs connected with your account
        # The optional parameters limits the length of the list.
        # starting_after is a job id which causes the removal of
        # all jobs from the list which were created before that job
        list_of_jobs = client.get_list_of_jobs(limit=None, starting_after=None)

        # obtain transcript text as a string for the job.
        transcript_text = client.get_transcript_text(job.id)
        print(transcript_text)

        # obtain transcript text as a json object for the job.
        transcript_json = client.get_transcript_json(job.id)

        # obtain transcript object for the job.
        transcript_obj = client.get_transcript_object(job.id)

        # obtain captions for the job.
        captions = client.get_captions(job.id)

        break

# Use the objects however you please

# Once you are done with the job, you can delete it.
# NOTE : This will PERMANENTLY DELETE all data related to a job. Exercise only
# if you're sure you want to delete the job.
# client.delete_job(job.id)
print("Job Submission and Collection Finished.")
