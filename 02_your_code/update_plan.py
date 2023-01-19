"""
'requests' allow make any HTTP requests, also is used for connect microservices
"""
import requests

from datetime import datetime

    
def upgrade(id, new_plan):
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

    try:
        url = f'http://localhost:8010/api/v1/customerdata/{id}/'
        response = requests.get(url)
        customer = response.json()
        if response.status_code == 404:
            return print('Error code 1: the ID does not exist or is badly formated') 
              
        data = customer['data']
        current_plan = data["SUBSCRIPTION"]
        result = up_or_down(current_plan, new_plan)
        if result == True:
            data['SUBSCRIPTION'] = new_plan
            data['UPGRADE_DATE'] = datetime.now().isoformat()
            try:
                data.pop('DOWNGRADE_DATE')
            except:
                pass
            put_request = requests.put(url, json=customer)
            if put_request.status_code == 200:
                print("Success!!")
    
        elif result == False:
            print('Error code 4: You can not downgrade a custommer subscription with this function')
        
        else:
            print(result) #The user already has the Subscription {current_plan}
            
    except:
        return Exception('Error code 3: other unknown error')
           

def downgrade(id, new_plan):

    try:
        url = f'http://localhost:8010/api/v1/customerdata/{id}/'
        response = requests.get(url)
        customer = response.json()
        if response.status_code == 404:
            return print('Error code 1: the ID does not exist or is badly formated')
        
        data = customer['data']
        current_plan = data["SUBSCRIPTION"]
        result = up_or_down(current_plan, new_plan)
        if result == False:
            data['SUBSCRIPTION'] = new_plan
            data['DOWNGRADE_DATE'] = datetime.now().isoformat()
            try:
                data.pop('UPGRADE_DATE')
            except:
                pass
            
            if new_plan == 'free':
              for feature in data['ENABLED_FEATURES']:
                data["ENABLED_FEATURES"][feature] = False
                       
            put_request = requests.put(url, json=customer)
            if put_request.status_code == 200:
                print("Success!!")
                
        elif result == True:
            print('Error code 4: You can not upgrade a custommer subscription with this function')
        
        else:
            print(result) #The user already has the Subscription {current_plan}
    
    except:
        raise Exception("Error code 3: other unknown error")
    
def up_or_down(current_plan, new_plan): 
    
    avaible_plans = ['free', 'basic', 'premium'] 
    if new_plan not in avaible_plans:
        return ('Error code 2: the target subscription level is not reachable') 
      
    new_plan_value = avaible_plans.index(new_plan)
    current_plan_value = avaible_plans.index(current_plan)

    if new_plan_value == current_plan_value:
        return (f'Error code 5: The user already has the Subscription {current_plan}')
    elif new_plan_value > current_plan_value:
        return True
    elif new_plan_value < current_plan_value:
        return False

#upgrade('e02deb01-d7a4-430c-9461-2674bc1e935a', 'premium')
downgrade('e02deb01-d7a4-430c-9461-2674bc1e935a', 'free')