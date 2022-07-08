import requests
import logging
def test_user_media(backend_service,test_user_header):
    
    resp = requests.get(f"http://{backend_service}/api/media", 
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
    