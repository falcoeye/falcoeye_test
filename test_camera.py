import requests
import logging

def test_add_camera(backend_service, test_user_header):
    logging.info("Test: add camera")
     
    pass_msgs = [
        "camera already exists",
        "camera added"
    ]
    data = {
        "name": "Harbour Village Bonaire Coral Reef",
        "streaming_type": "StreamingServer",
        "url": "https://www.youtube.com/watch?v=tk-qJJbdOh4",
        "status": "RUNNING",
    }
    resp = requests.post(f"{backend_service}/api/camera/", 
        json=data,headers=test_user_header)
    
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs

def test_list_cameras(backend_service,harbour_camera_add,test_user_header):
    logging.info("Test: list cameras")
    
    pass_msgs = [
        "camera data sent"
    ]
    resp = requests.get(f"{backend_service}/api/camera", 
        headers=test_user_header)
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs
    logging.info(resdict["camera"])

    assert len(resdict["camera"]) > 0

def test_get_camera_by_id(backend_service,cameras,test_user_header):
    logging.info("Test: get camera by id")
    
    pass_msgs = [
        "camera data sent"
    ]

    camera0 = cameras[0]
    resp = requests.get(f"{backend_service}/api/camera/{camera0['id']}", 
        headers=test_user_header)
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs
    logging.info(resdict["camera"])

def test_delete_camera_by_id(backend_service,test_user_header):
    
    logging.info("Test: delete camera by id")
    
    pass_msgs = [
        "camera added"
    ]
    # To avoid cascade problem if we use harbour camera
    data = {
        "name": "dummy",
        "streaming_type": "StreamingServer",
        "url": "https://www.dummy.com/",
        "status": "RUNNING",
    }
    resp = requests.post(f"{backend_service}/api/camera/", 
        json=data,headers=test_user_header)
    
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs

    camera = resdict["camera"]

    pass_msgs = [
        "camera deleted"
    ]
    resp = requests.delete(f"{backend_service}/api/camera/{camera['id']}", 
        headers=test_user_header)
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs

def test_update_camera_by_id(backend_service, harbour_camera,test_user_header):

    logging.info(harbour_camera)
    resp = requests.put(
        f"{backend_service}/api/camera/{harbour_camera['id']}",
        headers=test_user_header,
        json={"url": "https://www.youtube.com/watch?v=NwWgOilQuzw&t=4s"}
    )
    logging.info(resp.json())
    assert resp.status_code == 200
    assert resp.json().get("message") == "camera edited"

    resp = requests.get(f"{backend_service}/api/camera/{harbour_camera['id']}", headers=test_user_header)
    logging.info(resp.json())
    assert resp.status_code == 200
    



# def test_empty_cameras(client, user):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.get("/api/camera/", headers=headers)
#     assert resp.status_code == 404


# def test_get_invalid_camera_by_id(client, user):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.get(f"/api/camera/{uuid.uuid4()}", headers=headers)
#     assert resp.status_code == 404
#     assert resp.json.get("message") == "Camera not found!"


# def test_delete_invalid_camera_by_id(client, user):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.delete(f"/api/camera/{uuid.uuid4()}", headers=headers)
#     assert resp.status_code == 404
#     assert resp.json.get("message") == "Camera not found!"


# def test_update_camera_by_id(client, camera):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     camera.name = "UpdatedCamera"
#     resp = client.put(
#         f"/api/camera/{camera.id}",
#         headers=headers,
#         data=json.dumps(camera_schema.dump(camera)),
#         content_type="application/json",
#     )
#     assert resp.status_code == 200
#     assert resp.json.get("message") == "Camera has been updated"

#     resp = client.get(f"/api/camera/{camera.id}", headers=headers)
#     assert resp.status_code == 200
#     assert resp.json.get("camera").get("name") == "UpdatedCamera"

