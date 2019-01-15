class JobSubmitOptions:
	def __init__(
		self, 
		metadata=None, 
		callback_url=None, 
		skip_diarization=None
	):
		"""
		:param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as a webhook
        """
		self.metadata = "" if metadata == None else metadata
		self.callback_url = callback_url
		self.skip_diarization = False if skip_diarization == None else skip_diarization