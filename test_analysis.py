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
        "value": "Analysis output not yet written",
        "oper": "!="
    }
    wait_until(f"http://{backend_service}/api/analysis/{analysis_id}/meta.json",
    timeout=120,sleep=5,condition=condition,header=test_user_header)
    

    resp = requests.get(f"http://{backend_service}/api/analysis/{analysis_id}/meta.json", headers=test_user_header)
    metacontent = resp.content
    logging.info(f"Meta content {metacontent}")
    