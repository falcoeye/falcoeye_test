"""Global pytest fixtures."""
import pytest
import json 
import os
from falcoeye_kubernetes import FalcoServingKube
import requests
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture
def backend():
    logging.info("Fixture: Getting backend kube")
    backend_kube = FalcoServingKube("falcoeye-backend")
    return backend_kube

@pytest.fixture
def backend_service(backend):
    logging.info("Fixture: Getting backend service")
    service_address =  backend.get_service_address(external=True,hostname=True)
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
            "Email is already being used.",
            "User has been registered.",
            "Successfully registered user."
    ]
    logging.info(f"Posting to end point: http://{backend_service}/auth/register")
    res = requests.post(f"http://{backend_service}/auth/register", json=args)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs

@pytest.fixture
def login_user(backend_service):
    logging.info("Fixture: Login test user")
    args = {
        "email": "falcoeye-test@falcoeye.io",
        "password": "falcoeye-test"
    }
    pass_msgs =  [
        "Successfully logged in."
    ]
    res = requests.post(f"http://{backend_service}/auth/login", json=args)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs
    assert "access_token" in resdict
    return resdict["access_token"]

@pytest.fixture
def test_user(backend_service,register_user,login_user):
    logging.info("Fixture: Getting test user")
    
    header = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": login_user
    }
    pass_msgs =  [
        "User data sent",
        "User data successfully sent"
    ]
    url = f"http://{backend_service}/api/user/profile"
    logging.info(f"Posting to end point: {url}")
    res = requests.get(url, 
        headers=header)
    resdict = res.json()
    message = resdict["message"]
    assert message in pass_msgs
    user =  resdict["user"]
    user["access_token"] = login_user
    return user

    