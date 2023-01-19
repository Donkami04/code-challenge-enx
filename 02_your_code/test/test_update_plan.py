import requests
import pytest

    
def test_if_the_get_request_works_to_the_microservice():

    id = '49a6307e-c261-414d-86f5-c6004bcec8ab' 
    url = f'http://localhost:8010/api/v1/customerdata/{id}'
    response = requests.get(url)
    assert response.status_code == 200

def test_upgrade_plan_customer():
    
    id = '49a6307e-c261-414d-86f5-c6004bcec8ab' 
    url = f'http://localhost:8010/api/v1/customerdata/{id}/'   
    response = requests.get(url)
    customer = response.json()
    customer["data"]["SUBSCRIPTION"] = 'premium'
    response = requests.put(url, json=customer)
    assert response.status_code == 200
    
def test_downgrade_plan_customer():
    
    id = '49a6307e-c261-414d-86f5-c6004bcec8ab' 
    url = f'http://localhost:8010/api/v1/customerdata/{id}/'   
    response = requests.get(url)
    customer = response.json()
    customer["data"]["SUBSCRIPTION"] = 'free'
    response = requests.put(url, json=customer)
    assert response.status_code == 200
    
def is_the_plan_reachable(plan):
    avaible_plans = ['free', 'basic', 'premium']
    if plan not in avaible_plans:
        raise ValueError('Error code 2: the target subscription level is not reachable')
    
def test_test_if_plan_is_reachable():
    with pytest.raises(ValueError):
        is_the_plan_reachable('otroplan')
        
def test_id_does_not_exists():
    id = 'donkami'
    url = f'http://localhost:8010/api/v1/customerdata/{id}/'
    response = requests.get(url)
    assert response.status_code == 404
    
def test_downgrade_to_free_customer_plan_enabled_features_are_false():
    id = '49a6307e-c261-414d-86f5-c6004bcec8ab' 
    url = f'http://localhost:8010/api/v1/customerdata/{id}/' 
    plan = 'free'  
    response = requests.get(url)
    customer = response.json()
    customer["data"]["SUBSCRIPTION"] = plan
    if plan == 'free':
        customer['data']['ENABLED_FEATURES']['CERTIFICATES_INSTRUCTOR_GENERATION'] = False
        customer['data']['ENABLED_FEATURES']['ENABLE_COURSEWARE_SEARCH'] = False
        customer['data']['ENABLED_FEATURES']['ENABLE_EDXNOTES'] = False
        customer['data']['ENABLED_FEATURES']['ENABLE_COURSE_DISCOVERY'] = False
        customer['data']['ENABLED_FEATURES']['ENABLE_DASHBOARD_SEARCH'] = False
        customer['data']['ENABLED_FEATURES']['INSTRUCTOR_BACKGROUND_TASKS'] = False
        
    response = requests.put(url, json=customer)
    assert response.status_code == 200