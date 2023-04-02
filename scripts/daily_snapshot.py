from arlo import Arlo

from datetime import timedelta, date
import datetime
import sys
import os
import uuid
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
        
	filename = "./downloads/" + str(uuid.uuid4()) + "-.jpg"

	# Download the snapshot
	arlo.DownloadSnapshot(drivewayCameraSnapshotUrl, filename) # Save the snapshot to a file

except Exception as e:
    print(e)