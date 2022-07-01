import requests
import logging
def test_add_camera(backend_service, test_user):
    logging.info("Test: add camera")
    access_token = test_user.get("access_token")
    header = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": access_token
    }
    pass_msgs = [
        "Camera already exist",
        "Camera has been added",
        "Successfully added camera"
    ]
    data = {
        "name": "Harbour Village Bonaire Coral Reef",
        "streaming_type": "StreamingServer",
        "url": "https://www.youtube.com/watch?v=tk-qJJbdOh4",
        "status": "RUNNING",
    }
    resp = requests.post(f"http://{backend_service}/api/camera/", 
        json=data,headers=header)
    
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs



# def test_list_cameras(client, camera):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.get("/api/camera/", headers=headers)
#     assert resp.status_code == 200
#     assert resp.json.get("message") == "Camera data sent"


# def test_empty_cameras(client, user):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.get("/api/camera/", headers=headers)
#     assert resp.status_code == 404


# def test_get_camera_by_id(client, camera):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.get(f"/api/camera/{camera.id}", headers=headers)
#     assert resp.status_code == 200
#     assert resp.json.get("camera").get("name") == camera.name
#     assert resp.json.get("message") == "Camera data sent"


# def test_get_invalid_camera_by_id(client, user):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.get(f"/api/camera/{uuid.uuid4()}", headers=headers)
#     assert resp.status_code == 404
#     assert resp.json.get("message") == "Camera not found!"


# def test_delete_camera_by_id(client, camera):
#     resp = login_user(client)
#     headers = {"X-API-KEY": resp.json.get("access_token")}
#     resp = client.delete(f"/api/camera/{camera.id}", headers=headers)
#     assert resp.status_code == 200
#     assert resp.json.get("message") == "Camera deleted"


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

