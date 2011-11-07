from haliteconfig import HaliteConfig
import random
import os

class PlaylistHandler:
		
	def __init__( self ):
		self.media_paths = None
		self.last_path = None
	
	def get_media_paths( self ):
		if( self.media_paths is None ):
			config 	= HaliteConfig.default_config()
			path_items = config.items( "mediapaths" )
			self.media_paths = []
			for key, path in path_items:
				self.media_paths.append( path )
		return( self.media_paths )
	
	def get_next_file( self ):
		media_paths = self.get_media_paths()
		file_path = self.last_path
		while( file_path == self.last_path ):
			media_path = random.choice( media_paths )
			file_paths = []
			for root, dirs, files in os.walk( media_path ):
				for name in files:
					file_paths.append( os.path.join(root, name) )
			file_path = random.choice( file_paths )
		self.last_path = file_path
		return( file_path )
