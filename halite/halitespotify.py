import spytify
import time
from halitelogging import Logger
from haliteconfig import HaliteConfig

SP_SIGNAL_TRACK_START = 1
SP_SIGNAL_TRACK_TICK = 2
SP_SIGNAL_TRACK_END = 3

config 				= HaliteConfig.default_config()
SP_USERNAME			= config.get("spotify","username")
SP_PASSWORD			= config.get("spotify","password")

class URLHandlerSpotify():
	
	def __init__( self ):
		Logger.log_message( "URLHandlerSpotify: New Spytify instance" )
		self.sp_instance = spytify.Spytify( SP_USERNAME, SP_PASSWORD, callback=self.spytify_callback )
		self.playing = False
		self.router = None
	
	def handles_url( self, url ):
		return( "spotify" in url )
	
	def spytify_callback( self, signal, payload ):
		if( signal == SP_SIGNAL_TRACK_END ):
			self.playing = False
	
	def play_track( self, track ):
		Logger.log_message( "URLHandlerSpotify:\t\tplay track: %s " % track )
		# self.router = HaliteRouter( "hw:0,1,0", "hw:0,0,7" )
		self.sp_instance.play( track )
		self.playing = True;
		while self.playing:
			time.sleep( 1 )
		self.on_track_end()
	
	def on_track_end( self ):
		self.playing = False
		self.sp_instance.stop()
		# self.router.end_routing()
		# self.router = None
		time.sleep( 2 )
	
	def play_album( self, album ):
		track = random.choice( album.tracks )
		self.play_track( track )
	
	def handle_spotify_url( self, url ):
		Logger.log_message( "URLHandlerSpotify: handle Spotify url: %s" % url )
		result = self.sp_instance.lookup( url )
		Logger.log_message( "URLHandlerSpotify:\tresult: %s" % result )
		if isinstance( result, spytify.Track ):
			self.play_track( result )
		elif isinstance( result, spytify.Artist ):
			album = random.choice( result.albums )
			self.play_album( album )
		elif isinstance( result, spytify.Album ):
			self.play_album( result )
	
	def handle_url( self, url ):
		if( url[:7] == "spotify" ):
			# spotify url
			self.handle_spotify_url( url )
		elif( "http://" in url ):
			# http url, translate it
			url = url[url.find("/",7):].replace( "/", ":" )
			self.handle_spotify_url( "spotify%s" % url )
			