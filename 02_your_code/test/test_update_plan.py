"""
Testing the upgrade/downgrade

Run pytest from the root directory (02_your_code)!
"""

import requests
import pytest
import subprocess

    
def test_if_the_get_request_works_to_the_microservice():
    
    """
    This test make a get request to the microservice
    """

    id = '49a6307e-c261-414d-86f5-c6004bcec8ab' 
    url = f'http://localhost:8010/api/v1/customerdata/{id}'
    response = requests.get(url)
    assert response.status_code == 200

def test_upgrade_subscription_customer_to_basic():
    
    """
    This test must run after `make data` for the customerdataapi since it relies on this microservice.
    
    The test itself runs the `upgrade 49a6307e-c261-414d-86f5-c6004bcec8ab basic` and looks at the result.
    """
    
    id = '49a6307e-c261-414d-86f5-c6004bcec8ab'
        
    subprocess.run(f'cd ../02_your_code; ./cli upgrade {id} basic',
    shell=True, check=True,
    executable='/bin/bash')
    
    response = requests.get(f'http://localhost:8010/api/v1/customerdata/{id}/')
    customer = response.json()
    data = customer['data']

    assert response.status_code == 200
    assert customer['id'] == id
    assert data['SUBSCRIPTION'] == 'basic'
    assert "DOWNGRADE_DATE" not in data
    assert "UPGRADE_DATE" in data
    
def test_downgrade_subscription_customer_to_free():
    
    """
    This test must run after `make data` for the customerdataapi since it relies on this microservice.

    The test itself runs the `downgrade a237ed14-88fb-45f3-b9b1-471877dbdc60 free` and looks at the result.
    """
    id = '49a6307e-c261-414d-86f5-c6004bcec8ab' 
    
    subprocess.run(f'cd ../02_your_code; ./cli downgrade {id} free',
    shell=True, check=True,
    executable='/bin/bash')  
    
    response = requests.get(f'http://localhost:8010/api/v1/customerdata/{id}/' )
    customer = response.json()
    data = customer['data']
    
    assert customer['id'] == id
    assert data['SUBSCRIPTION'] == 'free'
    assert "DOWNGRADE_DATE" in data
    assert "UPGRADE_DATE" not in data
    
    """ Test that all the features are false"""
    for feat in data['ENABLED_FEATURES'].values():
        assert feat == False
                
def test_id_does_not_exists():
    
    """
    Try with and wrong Uuid and the status code should be 404
    """
    
    id = 'donkami'
    url = f'http://localhost:8010/api/v1/customerdata/{id}/'
    response = requests.get(url)
    assert response.status_code == 404
