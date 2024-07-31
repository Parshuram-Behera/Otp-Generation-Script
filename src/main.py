from appwrite.client import Client
import os
import logging
from pytubefix import YouTube

environments = {
    'WEB': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'WEB',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'clientVersion': '2.20240709.01.00',
                    'platform': 'DESKTOP'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0',
            'X-Youtube-Client-Name': '1',
            'X-Youtube-Client-Version': '2.20240709.01.00'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True
    },
    # Define other environments here...
}


def getDownloadUrls(video_url, environment='WEB'):
    try:
        # Set up YouTube object with the specified environment
        headers = environments[environment]['header']
        yt = YouTube(video_url, headers=headers)

        # Get all video streams sorted by resolution
        streams = yt.streams.order_by('resolution')

        # List to hold tuples of (resolution, download_url)
        download_list = []

        # Loop through each stream and collect the resolution and download URL
        for stream in streams:
            resolution = stream.resolution  # Get the resolution of the stream
            download_url = stream.url  # Get the download URL
            download_list.append((resolution, download_url))  # Append to the list

        return download_list  # Return the list of download URLs

    except Exception as e:
        logging.error(f"Error processing URL {video_url}: {e}")
        raise e


# Example usage in an API
def main(context):
    if context.req.method == "GET":
        value = context.req.query.get("value")
        if value:
            try:
                download_urls = getDownloadUrls(value)
                result_string = str(download_urls)
                return context.res.send(result_string)
            except Exception as e:
                return context.res.send(f"Error processing URL: {str(e)}")
        else:
            return context.res.send("Value parameter is missing in GET REQUEST")
    return context.res.json({"message": "Hello Parshuram Behera"})
