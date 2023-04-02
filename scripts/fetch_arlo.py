from arlo import Arlo

from datetime import timedelta, date
import datetime
import sys
import os
import config

from dotenv import load_dotenv

USERNAME = config.username
PASSWORD = config.password

try:
	# Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
	# Subsequent successful calls to login will update the oAuth token.
	arlo = Arlo(USERNAME, PASSWORD, 'gmail.credentials')
	# At this point you're logged into Arlo.

	# Fetch the Base Station
	baseStation = arlo.GetDevices(device_type='basestation')[0]
	
	# Fetch the Driveway Camera Device
	cameras = arlo.GetDevices(device_type='camera')
	# print(cameras)
	drivewayCamera = [camera for camera in cameras if 'Driveway' in camera['deviceName']][0]
	print(drivewayCamera)

	# Take a snapshot with the camera
	drivewayCameraSnapshotUrl = arlo.TriggerFullFrameSnapshot(baseStation, drivewayCamera)

	# Download the snapshot
	arlo.DownloadSnapshot(drivewayCameraSnapshotUrl, 'driveway-snapshot.jpg') # Save the snapshot to a file

	
	exit()

	today = (date.today()-timedelta(days=0)).strftime("%Y%m%d")
	seven_days_ago = (date.today()-timedelta(days=7)).strftime("%Y%m%d")

	# Get all of the recordings for a date range.
	library = arlo.GetLibrary(seven_days_ago, today)

	# Iterate through the recordings in the library.
	for recording in library:

		videofilename = datetime.datetime.fromtimestamp(int(recording['name'])//1000).strftime('%Y-%m-%d %H-%M-%S') + ' ' + recording['uniqueId'] + '.mp4'
		##
		# The videos produced by Arlo are pretty small, even in their longest, best quality settings,
		# but you should probably prefer the chunked stream (see below). 
		###    
		#    # Download the whole video into memory as a single chunk.
		#    video = arlo.GetRecording(recording['presignedContentUrl'])
		#	 with open('videos/'+videofilename, 'wb') as f:
		#        f.write(video)
		#        f.close()
		# Or:
		#
		# Get video as a chunked stream; this function returns a generator.
		# stream = arlo.StreamRecording(recording['presignedContentUrl'])
		# with open('videos/'+videofilename, 'wb') as f:
		# 	for chunk in stream:
		# 		f.write(chunk)
		# 	f.close()

		print('Downloaded video '+videofilename+' from '+recording['createdDate']+'.')

	# Delete all of the videos you just downloaded from the Arlo library.
	# Notice that you can pass the "library" object we got back from the GetLibrary() call.
	# result = arlo.BatchDeleteRecordings(library)

	# If we made it here without an exception, then the videos were successfully deleted.
	# print('Batch deletion of videos completed successfully.')

except Exception as e:
    print(e)