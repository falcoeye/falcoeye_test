import requests
import logging
def test_user_media(backend_service,test_user_header):
    
    resp = requests.get(f"{backend_service}/api/media", 
        headers=test_user_header)

    pass_msgs = [
        "media data sent"
    ]
    if resp.status_code == 204:
        logging.info("no media")
        return
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs
    media = resdict["media"]
    for m in media:
        logging.info(m)

def test_lutjanis_video(backend_service,test_user_header,user_media):
    
    resp = requests.get(f"{backend_service}/api/media", 
        headers=test_user_header)

    if user_media is None:
        logging.info("No user media.")
        return
    video_id = None
    for m in user_media:
        if m["tags"] == "fish, lutjanis, moonfish":
            video_id = m["id"]

    if video_id is None:
        logging.info("Lutjanis video is not uploaded")
        return

    resp = requests.get(f"{backend_service}/api/media/video/{video_id}/video_original.mp4", 
        headers=test_user_header)
    
    resdict = resp.json()

    logging.info(resdict)
