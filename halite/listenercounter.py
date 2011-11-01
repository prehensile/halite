import os
from haliteconfig import HaliteConfig

config 			= HaliteConfig.default_config()
COUNT_FILE 		= config.get("listenercounter","countfile")

class ListenerCounter:
	
	def __init__( self ):
		self.listener_count = 0
		if( os.path.isfile(COUNT_FILE) ):
			fh = open( COUNT_FILE )
			self.listener_count = int( fh.read() )
			fh.close()
	
	def write_count( self ):
		fh = open( COUNT_FILE, "w" )
		fh.write( "%d" % self.listener_count )
		fh.close()
	
	def increment_count( self ):
		self.listener_count += 1;
		self.write_count()
		return( self.listener_count )
	
	def decrement_count( self ):
		self.listener_count -= 1;
		if( self.listener_count < 1 ):
			self.listener_count = 0 # clamp to 0
		self.write_count()
		return( self.listener_count )
