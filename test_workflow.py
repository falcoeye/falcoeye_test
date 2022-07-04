import requests
import logging
import glob
import json
import os


def test_add_workflow(backend_service,workflow_user,workflow_user_header):
    logging.info("Test: add workflow")
     
    pass_msgs = [
        "name already exists",
        "workflow added"
    ]

    wf = glob.glob("workflows/*.json")[0]
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

    resp = requests.post(f"http://{backend_service}/api/workflow/", 
        json=data, headers=workflow_user_header)
    logging.info(resp.json())
    #assert resp.status_code == 201
    assert resp.json().get("message") in pass_msgs
    logging.info(f"{wkflowdict['name']} added")

