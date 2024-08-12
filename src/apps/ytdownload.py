from flask import Blueprint, render_template, request
from pytubefix import YouTubeDownloader
from datetime import timedelta
import logging

blueprint = Blueprint("app_ytdownload", __name__,)

@blueprint.route("/", methods=["GET"])
def app_ytdownload():
    return render_template("app/ytdownload.html")

@blueprint.route("/api/<action>/<target>", methods=["GET"])
def app_ytdownload_api(action=None, target=None):
    api = f"/{action}/{target}"
    returned_dict = {"status": "ok", "message": "", "results": {}}
    if api == "/get/streams":
        if "url" in request.args:
            try:
                downloader = YouTubeDownloader(request.args["url"])
                returned_dict["results"] = {
                    "title": downloader.title,
                    "length": str(timedelta(seconds=downloader.length)),
                    "thumbnail_url": downloader.thumbnail_url,
                    "streams": downloader.streams
                }
            except:
                logging.exception(f"Cannot resolve the video from {request.args['url']}")
                returned_dict["results"] = {
                    "title": "",
                    "length": "00:00:00",
                    "thumbnail_url": "",
                    "streams": {"Video": [], "Audio": []}
                }
            if len(returned_dict["results"]["streams"]["Video"]) == 0:
                returned_dict["status"] = "warning"
                returned_dict["message"] = f"Cannot resolve the video from {request.args['url']}"
        else:
            returned_dict["status"] = "warning"
            returned_dict["message"] = "argment `url` is not given"

    return returned_dict