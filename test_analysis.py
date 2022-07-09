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
            "filename": f"/user-assets/{test_user['id']}/videos/{harbour_video['id']}/video_original.mp4",
            "sample_every": 30,
            "min_score_thresh": 0.30,
            "max_boxes": 30
        }
    }
    

    pass_msgs = [
        "analysis added"
    ]

    resp = requests.post(f"http://{backend_service}/api/analysis/", 
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
    wait_until(f"http://{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=120,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"http://{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
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

    resp = requests.post(f"http://{backend_service}/api/analysis/", 
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
    wait_until(f"http://{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=300,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"http://{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")

def test_print_meta(backend_service,
    test_user,
    test_user_header):

    pass_msgs = [
        "analysis data sent"
    ]

    resp = requests.get(f"http://{backend_service}/api/analysis/", headers=test_user_header)
    
    assert resp.json().get("message") in pass_msgs

    for a in resp.json()["analysis"]:
        aid = a["id"]
        aresp = requests.get(f"http://{backend_service}/api/analysis/{aid}/meta.json", headers=test_user_header)
        logging.info(f"{aid}: {aresp.content}")


