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

from rev_ai import customvocabulariesclient

access_token = "your_access_token"

print("Creating Custom Vocab Client")

client = customvocabulariesclient.RevAiCustomVocabulariesClient(access_token)

print("Succeeded in creating client")

print("Submitting")

custom_vocab = client.submit_custom_vocabularies([{"phrases":["Peace out"]}])

print("Succeeded submission")

print("Getting Custom Vocabs")

result = client.get_custom_vocabularies(custom_vocab["id"])

print(result)