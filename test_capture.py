
import requests
import logging
import json
import time


def post_capture(backend_service,cam_id, ctype, user_header, **args):
    request_data = {"capture_type": ctype, "camera_id": str(cam_id)}
    for k, v in args.items():
        request_data[k] = v

    resp = requests.post(
        f"{backend_service}/api/capture",
        data=json.dumps(request_data),
        headers=user_header
    )
    logging.info(resp.json())
    assert "registry_key" in resp.json()
    rg_key = resp.json().get("registry_key")

    return rg_key

def loop_until_finished(backend_service,reg_key, time_before_kill, sleep_time, user_header):

    resp = requests.get(
        f"{backend_service}/api/capture/{reg_key}",
        headers=user_header,
    )

    respjson = resp.json()
    status = respjson.get("capture_status")
    elapsed = 0
    while status == "STARTED":
        logging.info(status)
        time.sleep(sleep_time)
        if elapsed > time_before_kill:
            break

        resp = requests.get(
            f"{backend_service}/api/capture/{reg_key}",
            headers=user_header,
        )
        respjson = resp.json()
        status = respjson.get("capture_status")
        elapsed += sleep_time
    return respjson

def test_capture_image_harbour(backend_service,harbour_camera,test_user_header):
    logging.info("Test: capture image harbour")
    
    registry_key = post_capture(backend_service,harbour_camera["id"], "image", test_user_header)

    time_before_kill = 100
    sleep_time = 3
    resp = loop_until_finished(
        backend_service,registry_key, time_before_kill, sleep_time, test_user_header
    )
    
    logging.info("Capturing finished")
    logging.info(resp)
    image_info = {
        "camera_id": str(harbour_camera["id"]),
        "tags": "Harbour",
        "note": "Harbour test image",
        "registry_key": registry_key,
    }

    resp = requests.post(
        f"{backend_service}/api/media/image",
        data=json.dumps(image_info),
        headers=test_user_header
    )
    logging.info(resp.json())

def test_capture_video_harbour(backend_service,harbour_camera,test_user_header):
    logging.info("Test: capture video harbour")
    
    registry_key = post_capture(backend_service,
        harbour_camera["id"], "video", test_user_header,length=3)

    time_before_kill = 100
    sleep_time = 3
    # sleep because the server might need to boot
    time.sleep(15)
    resp = loop_until_finished(
        backend_service,registry_key, time_before_kill, sleep_time, test_user_header
    )
    logging.info(resp)
    video_info = {
        "camera_id": str(harbour_camera["id"]),
        "tags": "Harbour",
        "note": "Harbour test video",
        "registry_key": registry_key,
    }

    resp = requests.post(
        f"{backend_service}/api/media/video",
        data=json.dumps(video_info),
        headers=test_user_header
    )
    respjson = resp.json()
    logging.info(respjson)
    vid = respjson["video"]["id"]
    temp_path = requests.get(
        f"{backend_service}/api/media/video/{vid}/video_original.mp4",
        headers=test_user_header)
    
    logging.info(temp_path.content)
    

