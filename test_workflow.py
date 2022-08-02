import requests
import logging
import glob
import json
import os

def test_login_as_workflow(backend_service):
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
    logging.info(access_token)
    header = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": f'JWT {access_token}'
    }

def test_add_workflows(backend_service,workflow_user,workflow_user_header):
    logging.info("Test: add workflow")
     
    pass_msgs = [
        "name already exists",
        "workflow added"
    ]

    wf = glob.glob("workflows/*.json")
    for w in wf:
        with open(w) as f:
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

def test_get_workflow_params(backend_service,test_user_header,kaustfishcounter_workflow):
    logging.info("Test: getting workflow params")
    url = f"{backend_service}/api/workflow/{kaustfishcounter_workflow['id']}/params"
    logging.info(f"Params' url: {url}")
    resp = requests.get(url, 
            headers=test_user_header)
    
    logging.info(resp.json())
     


