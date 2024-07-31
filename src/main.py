from appwrite.client import Client
import os
import logging
from pytubefix import YouTube


def getDownloadUrls(video_url):
    try:
        yt = YouTube(video_url,use_oauth= false)
        streams = yt.streams.order_by('resolution')
        download_list = []

        for stream in streams:
            resolution = stream.resolution
            download_url = stream.url
            download_list.append((resolution, download_url))

        return download_list  # Ensure the list is returned

    except Exception as e:
        logging.error(f"Error processing URL {video_url}: {e}")
        raise e


def main(context):
    if context.req.method == "GET":
        value = context.req.query.get("value")

        if value:
            try:
                download_urls = getDownloadUrls(value)
                result_string = "\n".join([f"Resolution: {res}, URL: {url}" for res, url in download_urls])
                return context.res.send(result_string)
            except Exception as e:
                return context.res.send(f"Error processing URL: {str(e)}")
        else:
            return context.res.send("Value parameter is missing in GET REQUEST")

    return context.res.json({"message": "Hello Parshuram Behera"})
