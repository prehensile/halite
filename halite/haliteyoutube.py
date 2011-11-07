import subprocess
from halitewrappers import MPlayerWrapper
from halitelogging import Logger
from haliteconfig import HaliteConfig

config 			= HaliteConfig.default_config()
YOUTUBEDL_PATH	= config.get("youtube","youtubedl_path")

class URLHandlerYouTube():
	
	def handle_url( self, url ):
		
		Logger.log_message( "URLHandlerYouTube: handle YouTube url: %s" % url )
		
		youtube_process = subprocess.Popen( [ YOUTUBEDL_PATH, '--stdout', url ], stdout=subprocess.PIPE );
		
		mplayer_wrapper = MPlayerWrapper()
		mplayer_wrapper.play_pipe( youtube_process.stdout )
		
		youtube_process.terminate()
		
	
	def handles_url( self, url ):
		return( "youtu" in url )