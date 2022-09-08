import os
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import quote


## Uploading image in the https://pubrepo.martspy.com/api/files server
def image_upload(url, img_name):

    # img = Image.open(requests.get(url, stream=True).raw)
    img = Image.open(url)

    # Create a buffer to hold the bytes
    buf = BytesIO()

    # Save the image as jpeg to the buffer
    img.save(buf, 'png')

    # Rewind the buffer's file pointer
    buf.seek(0)

    # Read the bytes from the buffer
    image_bytes = buf.read()

    # # Close the buffer
    # buf.close()

    files = {

        'fdata': (img_name, image_bytes),
        'key': (None, 'accelx'),
    }

    response = requests.post('https://pubrepo.martspy.com/api/files', files=files, verify = False)
    path = response.content
    print(response.content)

    return str(path)




## Uploading video in the https://pubrepo.martspy.com/api/files server
def video_upload(file):

    ## open video file
    my_file = open((file),'rb')
  

    ## pass the paremeter and file
    video_file = {
        'fdata': ('video.mp4', my_file),
        'key': (None, 'accelx'),
    }

    response = requests.post('https://pubrepo.martspy.com/api/files', files=video_file, verify = False)
    path = response.content
    print(response.content)

    return str(path)
