=======
History
=======

0.0.0 (2018-09-28)
------------------

* Initial alpha release

2.1.0
------------------

* Revamped official release

2.1.1
------------------

* File upload bug fixes

2.2.1
------------------

* Better Documentation

2.2.2
------------------

* Fix pypi readme formatting

2.3.0
------------------

* Add get_list_of_jobs

2.4.0
------------------

* Add support for custom vocabularies

2.5.0
------------------

* Add examples
* Improve error handling
* Add streaming client

2.6.0
------------------

* Support skip_punctuation
* Support .vtt captions output
* Support speaker channel jobs

2.6.1
------------------

* Add metadata to streaming client

2.7.0
------------------

* Add custom vocabularies to streaming client

2.7.1
------------------

* Use v1 of the streaming api
* Add custom vocabulary to async example
* Add filter_profanity to async and streaming clients, examples, and documentation
* Add remove_disfluencies to async client

2.11.0
------------------

* Add language selection option for multi-lingual ASR jobs to async client

2.12.0
------------------

* Add custom_vocabulary_id to async client

2.13.0
------------------
* Add detailed_partials to streaming client
* Switch to Github Actions for automated testing

2.14.0
------------------
* Add transcriber to async client
* Add verbatim, rush, segments_to_transcribe, test_mode to async client for human transcription
* Add start_ts and transcriber to streaming client

2.15.0
------------------
* Add topic extraction client
* Add speaker_names to async client for human transcription

2.16.0
------------------
* Add sentiment analysis client
* Add source_config and notification_config job options to support customer provided urls with authentication headers
* Deprecate media_url option, replace with source_config
* Deprecate callback_url option, replace with notification_config

2.17.0
------------------
* Add language to the streaming client

2.18.0
------------------
* Add atmospherics and speaker_count support
* Deprecated support for Python versions up to 3.8

2.19.0
------------------
* Add async translation and summarization
