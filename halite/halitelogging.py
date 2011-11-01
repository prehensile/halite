from datetime import datetime
import subprocess
from haliteconfig import HaliteConfig

config 				= HaliteConfig.default_config()
LOGFILE				= config.get("logging","logfile")
PRINT_MESSAGES 		= True

class Logger():
	
	loghandle = None
	
	@staticmethod
	def log_line( msg ):
		now = datetime.now()
		return( "%s: %s\n" % (now, msg) )
	
	@staticmethod
	def log_message( msg ):
		
		if( not Logger.loghandle ):
			Logger.loghandle = open( LOGFILE, "a" )
			Logger.loghandle.write( Logger.log_line( "Logger opened logfile" ) )
		Logger.loghandle.write( Logger.log_line( msg ) )
		Logger.loghandle.flush()
		
		if( PRINT_MESSAGES ):
			print msg
		
	@staticmethod
	def end_logging():
		if( Logger.loghandle is not None ):
			Logger.loghandle.close()