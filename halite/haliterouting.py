import subprocess

class HaliteRouter():
	
	def __init__( self, device_from=None, device_to=None):
		self.sox_process = None
		if( device_from is not None and device_to is not None ):
			self.begin_routing( device_from, device_to )
	
	def begin_routing( self, device_from, device_to ):
		self.sox_process = subprocess.Popen( ["sox","-2","-c","2","-t", "alsa", device_from, "-t", "alsa", device_to ] )
		
	def end_routing( self ):
		if( self.sox_process is not None ):
			self.sox_process.terminate()
			self.sox_process = None
			