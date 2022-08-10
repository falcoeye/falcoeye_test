import logging
import requests
from .utils import ops,random_string
import time
def wait_until(link,timeout,sleep,condition,header):

    ckey = condition["key"]
    cval = condition["value"]
    copestr = condition.get("oper", "in")
    coper = ops[copestr]

    tm = 0
    while tm < timeout:
        resp = requests.get(f"{link}",
            headers=header)
        
        resdict = resp.json()

        if ckey not in resdict:
            logging.info(f"{ckey} not in the response. Breaking...")
            break

        logging.info(f"Checking if {resdict[ckey]} {copestr} {cval}")
        if coper(resdict[ckey], cval):
            logging.info(f"Condition met {ckey} {copestr} {resdict[ckey]}")
            return
        logging.info(f"Condition not yet met {ckey} {copestr} {resdict[ckey]}")
        time.sleep(sleep)
        tm += sleep

def test_kaustfishcounter_file(backend_service,
    test_user,test_user_header,
    harbour_video,
    kaustfishcounter_workflow):
    logging.info("Test: run kaust fish counter")
    
    data = {
        "name": f"FishCounter_Test_{random_string()}",
        "workflow_id": kaustfishcounter_workflow["id"],
        "status": "new",
        "args": {
            "filename": f"falcoeye-bucket-test/user-assets/{test_user['id']}/videos/{harbour_video['id']}/video_original.mp4",
            "sample_every": 30,
            "min_score_thresh": 0.30,
            "max_boxes": 30
        }
    }
    logging.info(data)

    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=120,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_dinin_file(backend_service,
    test_user,test_user_header,
    dinein_video,
    workflows):
    logging.info("Test: run dine-in counter")

    hwf = None
    for wf in workflows:
        if wf["name"] == "Dine-In":
            hwf = wf
            break

    data = {
        "name": f"Dinein_Test_{random_string()}",
        "workflow_id": hwf["id"],
        "status": "new",
        "args": {
            "filename": f"/user-assets/{test_user['id']}/videos/{dinein_video['id']}/video_original.mp4",
            "sample_every": 30,
            "min_score_thresh": 0.30,
            "max_boxes": 30
        }
    }

    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=120,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_dinin_camera(backend_service,
    test_user,test_user_header,
    skitchen_camera,
    workflows):
    logging.info("Test: run dine-in counter")

    hwf = None
    for wf in workflows:
        if wf["name"] == "Dine-In":
            hwf = wf
            break



    data = {
        "name": f"Dinein_Test_{random_string()}",
        "workflow_id": hwf["id"],
        "status": "new",
        "args": {
            "host":skitchen_camera["host"],
            "port":skitchen_camera["port"],
            "username": skitchen_camera["username"],
            "password": skitchen_camera["password"],
            "sample_every": 30,
            "min_score_thresh": 0.30,
            "max_boxes": 30
        }
    }

    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=120,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_cofeeshop_bar_file(backend_service,
    test_user,test_user_header,
    coffeeshop_bar_video,
    workflows):
    logging.info("Test: run coffeeshop bar video")

    hwf = None
    for wf in workflows:
        if wf["name"] == "Dine-In":
            hwf = wf
            break

    data = {
        "name": f"coffeeshop_bar_{random_string()}",
        "workflow_id": hwf["id"],
        "status": "new",
        "args": {
            "filename": f"/user-assets/{test_user['id']}/videos/{coffeeshop_bar_video['id']}/video_original.mp4",
            "sample_every": 30,
            "min_score_thresh": 0.30,
            "max_boxes": 30
        }
    }

    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=120,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_carcounter_file(backend_service,
    test_user,
    test_user_header,
    house_cars_video,
    workflows):
    logging.info("Test: run car counter")

    hwf = None
    for wf in workflows:
        if wf["name"] == "Car monitor":
            hwf = wf
            break
    assert hwf is not None

    data = {
        "name": f"CarCounter_Test_{random_string()}",
        "workflow_id": hwf["id"],
        "status": "new",
        "args": {
            "filename": f"/user-assets/{test_user['id']}/videos/{house_cars_video['id']}/video_original.mp4",
            "sample_every": 1,
            "min_score_thresh": 0.10,
            "max_boxes": 30,
            "min_to_trigger_in": 5,
            "min_to_trigger_out": 5,
            "length": 60,
            "frequency": 1
        }
    }
    

    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=300,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_print_meta(backend_service,
    test_user,
    test_user_header):

    pass_msgs = [
        "analysis data sent"
    ]

    resp = requests.get(f"{backend_service}/api/analysis/", headers=test_user_header)
    
    assert resp.json().get("message") in pass_msgs

    for a in resp.json()["analysis"]:
        aid = a["id"]
        aresp = requests.get(f"{backend_service}/api/analysis/{aid}/meta.json", headers=test_user_header)
        logging.info(f"{aid}: {aresp.content}")

def test_leaky_car_monitor(backend_service,
    test_user,
    test_user_header,
    house_cars_video,
    workflows):
    logging.info("Test: run car counter")

    hwf = None
    for wf in workflows:
        if wf["name"] == "Leaky Car Monitor":
            hwf = wf
            break
    assert hwf is not None

    data = {
        "name": f"CarMonitor_Test_{random_string()}",
        "workflow_id": hwf["id"],
        "status": "new",
        "args": {
            "filename": f"/user-assets/{test_user['id']}/videos/{house_cars_video['id']}/video_original.mp4",
            "sample_every": 1,
            "min_score_thresh": 0.10,
            "max_boxes": 30,
            "min_to_trigger_in": 5,
            "min_to_trigger_out": 5,
            "length": -1,
            "frequency": 1,
            "timed_gate_open_freq": 30,
            "timed_gate_opened_last": 8
        }
    }
    
    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=300,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_leaky_arabian_angelfish(backend_service,
    test_user,
    test_user_header,
    arabian_angelfish_video,
    workflows):
    logging.info("Test: run arabian angelfish")

    hwf = None
    for wf in workflows:
        if wf["name"] == "Arabian Angelfish Monitor":
            hwf = wf
            break
    assert hwf is not None

    data = {
        "name": f"Arabian_Angelfish_Test_{random_string()}",
        "workflow_id": hwf["id"],
        "status": "new",
        "args": {
            "filename": f"falcoeye-bucket-test/user-assets/{test_user['id']}/videos/{arabian_angelfish_video['id']}/video_original.mp4",
            "sample_every": 1,
            "min_score_thresh": 0.10,
            "max_boxes": 30,
            "min_to_trigger_in": 5,
            "min_to_trigger_out": 5,
            "length": -1,
            "frequency": 1,
            "timed_gate_open_freq": 30,
            "timed_gate_opened_last": 5,
            "tcplimit": 12
        }
    }
    
    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=300,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_leaky_arabian_angelfish_short(backend_service,
    test_user,
    test_user_header,
    arabian_angelfish_video_short,
    workflows):
    logging.info("Test: run arabian angelfish")

    hwf = None
    for wf in workflows:
        if wf["name"] == "Arabian Angelfish Monitor":
            hwf = wf
            break
    assert hwf is not None

    data = {
        "name": f"Arabian_Angelfish_Test_{random_string()}",
        "workflow_id": hwf["id"],
        "status": "new",
        "feeds": {
            "source": {
                "type": "video",
                "id": arabian_angelfish_video_short['id']
            },
            "params": {
                "sample_every": 1,
                "min_score_thresh": 0.30,
                "max_boxes": 30,
                "min_to_trigger_in": 5,
                "min_to_trigger_out": 5,
                "length": -1,
                "frequency": 1,
                "timed_gate_open_freq": 30,
                "timed_gate_opened_last": 5,
                "ntasks": 12
            }
        }
    }
    print(data)
    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"{backend_service}/api/analysis/", 
        json=data, headers=test_user_header)
    logging.info(resp.json())
    respdict = resp.json()
    assert respdict.get("message") in pass_msgs

    analysis_id = respdict["analysis"]["id"]
    condition = {
        "key":"message",
        "value": "no output yet",
        "oper": "!="
    }
    wait_until(f"{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=300,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

