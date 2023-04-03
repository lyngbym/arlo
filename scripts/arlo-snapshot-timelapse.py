import uuid
from arlo import Arlo
import config

print(config.basestation)
print(config.camera_1)

try:
    # if config.basestation is null or empty, then set it to 'basestation'
    if not config.basestation:
        config.basestation = 'basestation'

    # if config.camera_1 is null or empty, then set it to 'camera'
    if not config.camera_1:
        config.camera_1 = 'camera'

    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(config.username, config.password, 'gmail.credentials')
    # At this point you're logged into Arlo.

    # Get the list of devices and filter on device type to only get the basestation.
    # This will return an array which includes all of the basestation's associated metadata.
    basestation = arlo.GetDevices(device_type='basestation')[0]
    print(basestation)
    
    # Get the list of devices and filter on device type to only get the cameras.
    # This will return an array of cameras, including all of the cameras' associated metadata.
    cameras = arlo.GetDevices(device_type='camera')

    # filter to only the camera matching config.camera_1
    drivewayCamera = [camera for camera in cameras if camera['deviceName'] == config.camera_1][0]

    # Trigger the snapshot.
    url = arlo.TriggerFullFrameSnapshot(basestation, drivewayCamera)

    # Randomize the filename
    filename = './downloads/' + str(uuid.uuid4()) + '.jpg'
    
    # # Download snapshot.
    arlo.DownloadSnapshot(url, filename)
    
    # If you are already recording, or have a need to snapshot while recording, you can do so like this:
    """
    # Starting recording with a camera.
    arlo.StartRecording(basestations[0], cameras[0]);

    # Wait for 4 seconds while the camera records. (There are probably better ways to do this, but you get the idea.)
    time.sleep(4)

    # Trigger the snapshot.
    url = arlo.TriggerStreamSnapshot(basestations[0], cameras[0]);
    
    # Download snapshot.
    arlo.DownloadSnapshot(url, 'snapshot.jpg')
    
    # Stop recording.
    arlo.StopRecording(cameras[0]);
    """
except Exception as e:
    print(e)
