import sys
import os
from ConfigParser import SafeConfigParser

class HaliteConfig:
	
	config = None
	
	@staticmethod
	def default_config():
		if( HaliteConfig.config is None ):
			# change this if needs be
			path = os.path.realpath(__file__)
			path = os.path.dirname( path )
			configpath = os.path.join( path, "etc/halite.config" )
			config = SafeConfigParser()
			config.read( configpath ) 
			HaliteConfig.config = config
		return HaliteConfig.config