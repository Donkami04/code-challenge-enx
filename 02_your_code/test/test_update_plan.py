"""
Testing the upgrade, downgrade and up_or_down functions

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
    Try with a wrong Uuid, the status code should be 404
    """
    
    id = 'donkami'
    url = f'http://localhost:8010/api/v1/customerdata/{id}/'
    response = requests.get(url)
    assert response.status_code == 404

def test_current_subscription_is_lower_than_new_subscription():
    
    """
    This test try a upgrade case, where the new subscription is better
    than the current subscription, could be return True
    """
    
    new_subscription = 'premium'
    current_subscription = 'basic'
    
    avaible_subscriptions = ['free', 'basic', 'premium'] 
    
    new_subscription_value = avaible_subscriptions.index(new_subscription)
    current_subscription_value = avaible_subscriptions.index(current_subscription)

    if new_subscription_value > current_subscription_value:
        return True

def test_current_subscription_is_lower_than_new_subscription_output():
    
    """
    This test validate the output of the `test_current_subscription_is_lower_than_new_subscription`
    """
    
    assert test_current_subscription_is_lower_than_new_subscription() == True
    

def test_current_subscription_is_best_than_new_subscription():
    
    """
    This test try a downgrade case, where the new subscription is lower
    than the current subscription, could be return False
    """
    
    new_subscription = 'basic'
    current_subscription = 'premium'
    
    avaible_subscriptions = ['free', 'basic', 'premium'] 
    
    new_subscription_value = avaible_subscriptions.index(new_subscription)
    current_subscription_value = avaible_subscriptions.index(current_subscription)

    if new_subscription_value < current_subscription_value:
        return False

def test_current_subscription_is_lower_than_new_subscription_output():
    
    """
    This test validate the output of the `test_current_subscription_is_lower_than_new_subscription_output`
    """
    assert test_current_subscription_is_best_than_new_subscription() == False
 
    