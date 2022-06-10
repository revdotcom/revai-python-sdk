"""Copyright 2022 REV

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

from rev_ai import apiclient
from rev_ai.models.customer_url_data import CustomerUrlData
from rev_ai.models import RevAIBaseUrl

# String containing your access token
access_token = "<your_access_token>"

# String containing the Rev AI base URL, this value should correspond to the same RevAI
# deployment as your access token
revai_base_url = RevAIBaseUrl.US.return_value

# Create your api client
client = apiclient.RevAiAPIClient(access_token, revai_base_url)

# Create config objects containing the url and auth headers for each option
# These options replace media_url and callback_url and should not be used alongside them
source_url = "https://www.rev.ai/FTC_Sample_1.mp3"
source_auth_headers = {"Authorization": "Bearer <token>"}
callback_url = "https://www.example.com/callback"
callback_auth_headers = {"Authorization": "Bearer <token>"}

# Submitting a job with the authentication header options
job = client.submit_job_url(
    source_config=CustomerUrlData(url=source_url, auth_headers=source_auth_headers),
    notification_config=CustomerUrlData(url=callback_url, auth_headers=callback_auth_headers))

print("Submitted Job")
