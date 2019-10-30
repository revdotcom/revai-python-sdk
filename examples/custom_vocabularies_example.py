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
from rev_ai import customvocabulariesclient
from rev_ai.models import CustomVocabulary

access_token = "your_access_token"

print("Creating Custom Vocab Client")
client = customvocabulariesclient.RevAiCustomVocabulariesClient(access_token)

print("Submitting")
custom_vocabularies_job = client.submit_custom_vocabularies(
    [
        {"phrases": ["Patrick Henry Winston"]},
        CustomVocabulary(["Robert Berwick", "Noam Chomsky"])
    ]
)

job_id = custom_vocabularies_job["id"]

while True:
    custom_vocabularies = client.get_custom_vocabularies(job_id)
    status = custom_vocabularies["status"]

    print("Job Status: {}".format(status))

    if status == "in_progress":
        time.sleep(5)
        continue

    elif status == "failed":
        print("Job Failed : {}".format(custom_vocabularies["failure_detail"]))
        break

    if status == "complete":
        print("SUCCESS: {}".format(custom_vocabularies))
        break
