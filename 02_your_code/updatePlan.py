"""
'requests' allow make any HTTP requests, also is used for connect microservices
"""
import requests

from datetime import datetime

"""
This function is used to upgrade the subscription of one customer.
"""

def upgrade(id, plan):
    """_summary_
        This function is used to upgrade the subscription of one customer.
        Has differents validations layers
    
    Args:
        id (_type_): _description_
        plan (_type_): _description_

    Raises:
        SyntaxError: _description_

    Returns:
        _type_: _description_
    """
    if plan not in ['free', 'basic', 'premium']:
        raise SyntaxError('Error code 2: the target subscription level is not reachable')
    
    else:
        try:
            url = f'http://localhost:8010/api/v1/customerdata/{id}/'
            response = requests.get(url)
            customer = response.json()
            
            if response.status_code == 404:
                return SyntaxError('Error code 1: the ID does not exist or is badly formated')
            
            currentPlan = customer["data"]["SUBSCRIPTION"]
            
            if currentPlan == 'premium' and plan == 'basic' or plan == 'free':
                return print("You can't upgrade the subscription in this function")
            
            elif currentPlan == 'basic' and plan == 'free':
                return print ("You can't upgrade the subscription in this function")
            
            if currentPlan == plan:
                return print(f'The user already has the Subscription {plan}')
            
            elif currentPlan == 'free' and plan == 'basic' or plan == 'premium':
                customer['data']['UPGRADE_DATE'] = datetime.now().isoformat()
                
            elif currentPlan == 'basic' and plan == 'premium':
                customer['data']['UPGRADE_DATE'] = datetime.now().isoformat()
                
                
            customer["data"]["SUBSCRIPTION"] = plan
            
            response = requests.put(url, json=customer)
            response.raise_for_status()
            print("Successfully changed")
            
        except:
            return Exception('Error code 3: other unknown error')
           

def downgrade(id, plan):

    if plan not in ['free', 'basic', 'premium']:
        return SyntaxError('Error code 2: the target subscription level is not reachable')
            
    else:
    
        try:
            url = f'http://localhost:8010/api/v1/customerdata/{id}/'
            response = requests.get(url)
            customer = response.json()
            
            if response.status_code == 404:
                return SyntaxError('Error code 1: the ID does not exist or is badly formated')
            
            currentPlan = customer["data"]["SUBSCRIPTION"]
            #! debo hacer el middleware
            if currentPlan == 'free' and plan == 'basic' or plan == 'premium':
                return print("You can't upgrade the subscription in this function")
            
            elif currentPlan == 'basic' and plan == 'premium':
                return print ("You can't upgrade the subscription in this function")
            #! evitar que mejor en la funcion de down
            if currentPlan == plan:
                return print(f'The user already has the Subscription {plan}')
            
            elif currentPlan == 'premium' and plan == 'basic' or plan == 'free':
                customer['data']['DOWNGRADE_DATE'] = datetime.now().isoformat()
                
            elif currentPlan == 'basic' and plan == 'free':
                customer['data']['DOWNGRADE_DATE'] = datetime.now().isoformat()
            
            if plan == 'free':    
                customer['data']['ENABLED_FEATURES']['CERTIFICATES_INSTRUCTOR_GENERATION'] = False
                customer['data']['ENABLED_FEATURES']['ENABLE_COURSEWARE_SEARCH'] = False
                customer['data']['ENABLED_FEATURES']['ENABLE_EDXNOTES'] = False
                customer['data']['ENABLED_FEATURES']['ENABLE_COURSE_DISCOVERY'] = False
                customer['data']['ENABLED_FEATURES']['ENABLE_DASHBOARD_SEARCH'] = False
                customer['data']['ENABLED_FEATURES']['INSTRUCTOR_BACKGROUND_TASKS'] = False


            customer["data"]["SUBSCRIPTION"] = plan
            
            response = requests.put(url, json=customer)
            response.raise_for_status()
            print("Successfully changed")
        
        except:
            raise Exception("Error code 3: other unknown error")

upgrade('e02deb01-d7a4-430c-9461-2674bc1e935a', 'basic')

