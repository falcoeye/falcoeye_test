"""Global pytest fixtures."""
import pytest
import json 
import os
#from falcoeye_kubernetes import FalcoServingKube
import requests
import glob
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

DIR = os.path.dirname(os.path.realpath(__file__))

# @pytest.fixture
# def backend_service():
#     logging.info("Fixture: Getting backend service")
#     return f"http://localhost:5000"

# @pytest.fixture
# def backend():
#     logging.info("Fixture: Getting backend kube")
#     backend_kube = FalcoServingKube("falcoeye-backend")
#     return backend_kube

# @pytest.fixture
# def backend_service(backend):
#     logging.info("Fixture: Getting backend service")
#     service_address =  backend.get_service_address(external=True,hostname=True)
#     logging.info(f"Backend service address: {service_address}")
#     return f"http://{service_address}"

@pytest.fixture
def backend_service():
    logging.info("Fixture: Getting backend service")
    service_address =  "https://falcoeye-backend-xbjr6s7buq-uc.a.run.app"
    logging.info(f"Backend service address: {service_address}")
    return service_address

@pytest.fixture
def register_user(backend_service):
    logging.info("Fixture: Register test user")
    args = {
            "email": "falcoeye-test@falcoeye.io",
            "username": "falcoeye_test",
            "name": "falcoeye test",
            "password": "falcoeye-test"
    }
    pass_msgs =  [
            "email or username already exists",
            "successfully registered"
    ]
    logging.info(f"Posting to end point: {backend_service}/auth/register")
    res = requests.post(f"{backend_service}/auth/register", json=args)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs

@pytest.fixture
def login_test_user(backend_service):
    logging.info("Fixture: Login test user")
    args = {
        "email": "falcoeye-test@falcoeye.io",
        "password": "falcoeye-test"
    }

    pass_msgs =  [
        "successfully logged in"
    ]
    res = requests.post(f"{backend_service}/auth/login", json=args)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs
    assert "access_token" in resdict
    return resdict["access_token"]

@pytest.fixture
def test_user(backend_service,register_user,login_test_user):
    logging.info("Fixture: Getting test user")
    
    header = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": f'JWT {login_test_user}'
    }
    pass_msgs =  [
        "user data sent"
    ]
    url = f"{backend_service}/api/user/profile"
    logging.info(f"Posting to end point: {url}")
    res = requests.get(url, 
        headers=header)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs
    user =  resdict["user"]
    logging.info(f"test user info {user}")
    user["access_token"] = login_test_user
    return user

@pytest.fixture
def test_user_header(test_user):
    logging.info("Fixture: getting test user header and token")
    access_token = test_user.get("access_token")
    header = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": f'JWT {access_token}'
    }
    logging.info(f"{header}")
    return header

@pytest.fixture
def test_user_header_nocontenttype(test_user):
    logging.info("Fixture: getting test user header and token")
    access_token = test_user.get("access_token")
    header = {
        "accept": "application/json",
        "X-API-KEY": f'JWT {access_token}'
    }
    logging.info(f"{header}")
    return header
    
@pytest.fixture
def workflow_user_header(backend_service):
    logging.info("Fixture: Getting workflow user header")
    
    workflow_user = os.getenv("WORKFLOW_USER").strip()
    workflow_password = os.getenv("WORKFLOW_PASSWORD").strip()
    args = {
            "email": workflow_user,
            "password": workflow_password
    }
    pass_msgs =  [
        "successfully logged in"
    ]
    res = requests.post(f"{backend_service}/auth/login", json=args)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs
    assert "access_token" in resdict
   
    access_token = resdict["access_token"]
    header = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": f'JWT {access_token}'
    }
    return header

@pytest.fixture
def workflow_user_header_nocontenttype(backend_service):
    logging.info("Fixture: Getting workflow user header")
    
    workflow_user = os.getenv("WORKFLOW_USER").strip()
    workflow_password = os.getenv("WORKFLOW_PASSWORD").strip()
    args = {
            "email": workflow_user,
            "password": workflow_password
    }
    pass_msgs =  [
        "successfully logged in"
    ]
    res = requests.post(f"{backend_service}/auth/login", json=args)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs
    assert "access_token" in resdict
   
    access_token = resdict["access_token"]
    header = {
        "accept": "application/json",
        "X-API-KEY": f'JWT {access_token}'
    }
    return header

@pytest.fixture
def workflow_user(backend_service,workflow_user_header):
    logging.info("Fixture: Getting workflow user")

    pass_msgs =  [
        "user data sent"
    ]
    url = f"{backend_service}/api/user/profile"
    logging.info(f"Posting to end point: {url}")
    res = requests.get(url, 
        headers=workflow_user_header)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs
    user =  resdict["user"]
    
    return user

@pytest.fixture
def harbour_camera_add(backend_service,test_user_header):
    logging.info("Fixture: add harbour camera")
    
    pass_msgs = [
        "camera already exists",
        "camera added"
    ]
    data = {
        "name": "Harbour Village Bonaire Coral Reef",
        "streaming_type": "StreamingServer",
        "url": "https://www.youtube.com/watch?v=NwWgOilQuzw&t=4s",
        "status": "RUNNING",
    }
    resp = requests.post(f"{backend_service}/api/camera/", 
        json=data,headers=test_user_header)
    
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs

@pytest.fixture
def skitchen_camera_add(backend_service,test_user_header):
    logging.info("Fixture: add skitchen camera")
    
    pass_msgs = [
        "camera already exists",
        "camera added"
    ]
    data = {
        "name": "Skitchen Sultana Camera",
        "streaming_type": "RTSP",
        "host": "http://192.168.0.130/",
        "port": 554,
        "username":"",
        "password":"skitchen@2022",
        "status": "RUNNING",
    }
    resp = requests.post(f"{backend_service}/api/camera/", 
        json=data,headers=test_user_header)
    
    
    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs

@pytest.fixture
def cameras(backend_service,harbour_camera_add,test_user_header):
    logging.info("Fixture: get cameras")
    
    resp = requests.get(f"{backend_service}/api/camera", 
        headers=test_user_header)

    pass_msgs = [
        "camera data sent"
    ]

    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs

    return resdict["camera"]

@pytest.fixture
def harbour_camera(cameras,test_user_header):
    logging.info("Fixture: get harbour cameras")
    hcam = None
    for cam in cameras:
        if cam["name"] == "Harbour Village Bonaire Coral Reef":
            hcam =  cam
            break
    assert hcam is not None
    return hcam

@pytest.fixture
def skitchen_camera(cameras,test_user_header):
    logging.info("Fixture: get skitchen cameras")
    hcam = None
    for cam in cameras:
        if cam["name"] == "Skitchen Sultana Camera":
            hcam =  cam
            break
    assert hcam is not None
    return hcam


@pytest.fixture
def kaustfishcounter_workflow(backend_service,workflow_user,workflow_user_header):
    logging.info("Fixture: add kaust fish counter workflow")
     
    pass_msgs = [
        "name already exists",
        "workflowe added"
    ]

    wf = glob.glob("workflows/kaust_fish_counter_threaded_async.json")[0]
    with open(wf) as f:
        wkflowdict = json.load(f)

    logging.info(f"Adding workflow {wkflowdict['name']}")
    data = {
        "name": wkflowdict["name"],
        "creator": workflow_user["id"],
        "structure": wkflowdict["structure"],
        "usedfor": wkflowdict["usedfor"],
        "consideration": wkflowdict["consideration"],
        "assumption": wkflowdict["assumption"],
        "results_description": wkflowdict["results_description"],
    }

    resp = requests.post(f"{backend_service}/api/workflow/", 
        json=data, headers=workflow_user_header)
    logging.info(resp.json())
    #assert resp.status_code == 201
    assert resp.json().get("message") in pass_msgs
    logging.info(f"{wkflowdict['name']} added")

    #Getting workflows
    logging.info("Geting workflows")
    
    resp = requests.get(f"{backend_service}/api/workflow", 
        headers=workflow_user_header)

    pass_msgs = [
        "workflow data sent"
    ]

    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs
    hwf = None
    for wf in resdict["workflow"]:
        if wf["name"] == wkflowdict["name"]:
            hwf = wf
            break
    assert hwf is not None
    logging.info(f"Workflow found {wf}")
    return hwf

@pytest.fixture
def workflows(backend_service,test_user_header):
    logging.info("Fixture: get workflows")
    
    resp = requests.get(f"{backend_service}/api/workflow", 
        headers=test_user_header)

    pass_msgs = [
        "workflow data sent"
    ]

    resdict = resp.json()
    message = resdict["message"]
    assert message in pass_msgs

    return resdict["workflow"]

@pytest.fixture
def user_media(backend_service,test_user_header):
    
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

    return resdict["media"]

@pytest.fixture
def harbour_video(backend_service,
    harbour_camera,
    user_media,
    test_user_header):
    logging.info("Fixture: get harbour video")
    cam_id = harbour_camera["id"]
    hmedia = None
    logging.info(f"Harbour camera id: {cam_id}")
    for m in user_media:
        if m["camera_id"] == cam_id:
            hmedia = m
            break

    assert hmedia is not None
    return hmedia

@pytest.fixture
def dinein_video(backend_service,
    user_media,
    test_user_header):
    logging.info("Fixture: getting dine-in video")
    
    if user_media is not None:
        for m in user_media:
            if m["tags"] == "dinein":
                return m

@pytest.fixture
def coffeeshop_bar_video(backend_service,
    user_media,
    test_user_header):
    logging.info("Fixture: getting coffeeshop bar video")
    
    if user_media is not None:
        for m in user_media:
            if m["tags"] == "coffeeshop, behind cashier":
                return m

@pytest.fixture
def arabian_angelfish_video(backend_service,
    user_media,
    test_user_header):
    logging.info("Fixture: getting arabian angelfish video")
    
    if user_media is not None:
        for m in user_media:
            if m["tags"] == "arabian angelfish, kaust":
                return m

    return None

@pytest.fixture
def arabian_angelfish_video_short(backend_service,
    user_media,
    test_user_header):
    logging.info("Fixture: getting arabian angelfish video")
    video = None
    if user_media is not None:
        for m in user_media:
            if m["tags"] == "fish,arabian angelfish":
                video = m
                break
    assert video is not None
    return video

@pytest.fixture
def house_cars_video(backend_service,
    user_media,
    test_user_header):
    logging.info("Fixture: getting house cars video")
    
    if user_media is not None:
        for m in user_media:
            if m["tags"] == "cars,my house":
                return m

    return None

@pytest.fixture
def lutjanis_video(backend_service,
    user_media,
    test_user_header):
    logging.info("Fixture: getting lutjanis video")
    
    if user_media is not None:
        for m in user_media:
            if m["tags"] == "fish, lutjanis, moonfish":
                return m

    return None
