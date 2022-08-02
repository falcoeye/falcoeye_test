import logging
import requests
from .utils import ops,random_string
import time
import logging
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

VIDEO = "arabian_angelfish.mp4"
TAGS = "arabian angelfish, kaust"
NOTES = "Beautiful arabian angelfish pass by KAUST camera"

def test_upload_video(backend_service,
    test_user,test_user_header_nocontenttype,
    test_user_header,
    arabian_angelfish_video):
    logging.info("Test: run upload video")
    
    if arabian_angelfish_video is not None:
        logging.info("Delete existing instance")
        resp = requests.delete(
            f"{backend_service}/api/media/video/{lutjanis_video['id']}",
            headers=test_user_header_nocontenttype)
        assert resp.status_code == 200
    
    filename = f"{basedir}/media/{VIDEO}"
    with open(filename, "rb") as f:
        files = {
            "file": (os.path.basename(filename), f, "video/mp4"),
        }
        
        resp = requests.post(
            f"{backend_service}/api/upload",
            headers=test_user_header_nocontenttype,
            files=files
        )

    logging.info(f"response: {resp.json()}")
    assert resp.status_code == 200
    assert "registry_key" in resp.json()

    registry_key = resp.json()["registry_key"]
    logging.info(f"file uploaded with registry: {registry_key}")

    video_info = {
        "camera_id": None,
        "tags": TAGS,
        "note": NOTES,
        "registry_key":registry_key ,
    }

    resp = requests.post(
        f"{backend_service}/api/media/video",
        data=json.dumps(video_info),
        headers=test_user_header,
    )

    assert resp.status_code == 201

    

