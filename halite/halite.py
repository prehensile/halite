#!/usr/bin/env python

import plistlib
import random
import os
import re
from halitespotify import URLHandlerSpotify
from haliteyoutube import URLHandlerYouTube
from halitewrappers import MPlayerWrapper
from halitelogging import Logger
from haliteconfig import HaliteConfig
import subprocess
import sys
import listenercounter

config 			= HaliteConfig.default_config()
PIDFILE 		= config.get("halite","pidfile")
COMMANDFILE 	= config.get("halite","commandfile")
MEDIA_ROOT 		= config.get("halite","media_root")


class FileHandler():

	def handled_extensions( self ):
		return []

	def handle_file( self, filepath ):
		self.filepath = filepath

	
class FileHandlerURL():
	
	def __init__( self ):
		self.handlers = [ 	URLHandlerYouTube(),
							URLHandlerSpotify()	];
	
	def handled_extensions( self ):
		return[ ".webloc", ".txt", ".url" ]
	
	def handle_url( self, url ):
		handled = False
		# find a handler for the url
		for url_handler in self.handlers:
			# if we find one..
			if( url_handler.handles_url( url ) ):
				# process the url
				url_handler.handle_url( url )
				# exit the loop
				handled = True
				break;
		return( handled )
	
	def handle_file( self, filepath ):
		
		# get a url
		fh = open( filepath )
		fstring = fh.read()
		if( "plist" in fstring ):
			# file is a .webloc plist
			pl = plistlib.readPlist( filepath )
			self.handle_url( pl["URL"] )
		else:
			# step through lines, trying to handle each one
			lines = fstring.splitlines()
			for line in lines:
			    if( self.handle_url( line ) ):
			    	break
			    
		
		fh.close()	    
				
				
class FileHandlerMediaFile():
	
	def handled_extensions( self ):
		return[ ".mp3", ".mp4", ".m4a" ]
	
	def handle_file( self, filepath ):
		Logger.log_message( "-> handle file: %s" % filepath )
		mplayer_wrapper = MPlayerWrapper()
		mplayer_wrapper.play_file( filepath )
		
		
def start():
	
	
	
	if( os.path.isfile(PIDFILE) ):
		Logger.log_message( "There is already an instance of Halite running." )
		exit()
	else:
		fh = open( PIDFILE, "w" )
		fh.write( "%d" % os.getpid() )
		fh.close()
	
	Logger.log_message( "Halite start, pid is %d" % os.getpid() )
	
	file_handlers	= [ 	FileHandlerMediaFile(),
							FileHandlerURL() ]
	running = True
	while running:
		# get a new file
		files = os.listdir( MEDIA_ROOT )
		file = random.choice( files )
		(path, ext) = os.path.splitext(file)
		
		# play it
		handled = False
		for file_handler in file_handlers:
			handled_extensions = file_handler.handled_extensions()
			for handled_extension in handled_extensions:
				if( handled_extension == ext ):
					file_handler.handle_file( os.path.join( MEDIA_ROOT, file ) )
					handled = True
				if( handled ):
					break
			if( handled ):
					break
		
		# check contol file
		if( os.path.isfile(COMMANDFILE) ):
			Logger.log_message( "Halite: has a commandfile" )
			fh = open( COMMANDFILE )
			command = fh.read()
			fh.close()
			Logger.log_message( "-> command is %s" % command )
			if( command == "stop" ):
				running = False
				os.remove( COMMANDFILE )
	
	Logger.log_message( "Halite: end main loop" )
	os.remove(PIDFILE)


def write_command( command ):
	fh = open(COMMANDFILE, "w")
	fh.write( exec_command )
	fh.close()


def main():
	
	if( len(sys.argv) > 1 ):
		exec_command = sys.argv[1]

		if( exec_command == "connect" ):
			listener_counter = listenercounter.ListenerCounter()
			num_listeners = listener_counter.increment_count()
			Logger.log_message( "Halite: listener connect, new num_listeners=%d" % num_listeners )
			if( num_listeners > 0 ):
				start()
		
		elif( exec_command == "disconnect" ):
			listener_counter = listenercounter.ListenerCounter()
			num_listeners = listener_counter.decrement_count()
			Logger.log_message( "Halite: listener disconnect, new num_listeners=%d" % num_listeners )
			if( num_listeners < 1 ):
				write_command( "stop" )
		
		elif( exec_command == "start" ):
			# Logger.PRINT_MESSAGES = False
			Logger.LOG_TO_USERCONSOLE = None
			start()
		
		else:
			# write command to COMMANDFILE so running instance can use it
			if( os.path.isfile(PIDFILE) ):
				write_command( exec_command )
			else:
				Logger.log_message( "There is no instance of Halite running" )
		
	else:
		Logger.log_message( "No argument provided" )
	
main()