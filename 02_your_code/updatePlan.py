import requests
from datetime import datetime

def upgrade(id, plan):
    
    if plan != 'free' and plan != 'basic' and plan != 'premium':
        raise SyntaxError('Error code 2: the target subscription level is not reachable')
    
    else:
        try:
            url = f'http://localhost:8010/api/v1/customerdata/{id}/'
            customer = requests.get(url)
            customer = customer.json()
            
            #! Pendiente hacer la validacion del ID
            # if customer['detail'] == "Not found.":
            #     return print('Error code 1: the ID does not exist or is badly formated')
            
            currentPlan = customer["data"]["SUBSCRIPTION"]
            
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
            raise Exception('Error code 3: other unknown error')
           

def downgrade(id, plan):

    if plan != 'free' and plan != 'basic' and plan != 'premium':
        raise SyntaxError('Error code 2: the target subscription level is not reachable')
            
    else:
    
        try:
            url = f'http://localhost:8010/api/v1/customerdata/{id}/'
            customer = requests.get(url)
            customer = customer.json()
            currentPlan = customer["data"]["SUBSCRIPTION"]
            

            
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
                customer['data']['ENABLED_FEATURES']['ENABLE_DASHBOARD_SEARCH'] = False
                customer['data']['ENABLED_FEATURES']['INSTRUCTOR_BACKGROUND_TASKS'] = False
                customer['data']['ENABLED_FEATURES']['ENABLE_COURSE_DISCOVERY'] = False
            

            customer["data"]["SUBSCRIPTION"] = plan
            
            response = requests.put(url, json=customer)
            response.raise_for_status()
            print("Successfully changed")
        
        except:
            raise Exception("Error code 3: other unknown error")

upgrade('49a6307e-c261-414d-86f5-c6004bcec8ab', 'premium')
