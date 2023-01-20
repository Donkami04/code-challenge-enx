"""requests allow make HTTP requests"""
import requests

from datetime import datetime


def upgrade(id, new_subscription):
    
    """_summary_
    The upgrade function allows to improve a customer's subscription, create or actualize
    the date of the last upgrade and replaces the date of the last downgrade if it exists.
    Upgrade function calls the up_or_down function which validates the new subscription.
    
    Args:
        id ( UUID ): Unique code to identify each customer 
        new_subscription ( Str ) : It is the new desired subscription, only allow free, basic or premium
      
    Raises Error:
        Error Code 1: Bad id or does not exist.
        Error Code 2: Bad subscription option or does not exist.
        Error Code 3: (Exception) Occurs if something goes wrong with the microservice
            for which the request is made or unkonw error.
        Error Code 4: If you use the upgrade function to downgrade the subscription.
        Error Code 5: The user already has the Subscription that you are trying to update.
        
    Returns:
        Success ( Str ): Console message informing if the upgrade was successful.
    """

    try:
        url = f'http://localhost:8010/api/v1/customerdata/{id}/'
        response = requests.get(url)
        customer = response.json()
        if response.status_code == 404:
            return print('Error code 1: the ID does not exist or is badly formated') 
              
        data = customer['data']
        current_subscription = data["SUBSCRIPTION"]
        result = up_or_down(current_subscription, new_subscription) 
        if result == True:
            data['SUBSCRIPTION'] = new_subscription
            data['UPGRADE_DATE'] = datetime.now().isoformat() # .isoformat() make serializable the datetime
            try:
                data.pop('DOWNGRADE_DATE') # If DOWNGRADE_DATE exists then remove it, if not do nothing
            except:
                pass
            put_request = requests.put(url, json=customer)
            if put_request.status_code == 200:
                return print("Success!!")
    
        elif result == False:
            print('Error code 4: You can not downgrade a custommer subscription with this function')
        
        else:
            print(result) #The user already has the Subscription {current_subscription}
            
    except:
        return Exception('Error code 3: other unknown error')
           

def downgrade(id, new_subscription):

    """_summary_
    The downgrade function allows to lower a customer's subscription, create or actualize
    the date of the last downgrade and replaces the date of the last upgrade if it exists.
    If the new subscription is free turn all the ENABLED_FEATURES to False.
    Downgrade function calls the up_or_down function which validates the new subscription.
    
    Args:
        id ( UUID ): Unique code to identify each customer 
        new_subscription ( Str ) : It is the new desired subscription, only allow free, basic or premium
        
    Raises:
        Error Code 1: Bad id or does not exist.
        Error Code 2: Bad subscription option or does not exist.
        Error Code 3: (Exception) Occurs if something goes wrong with the microservice
            for which the request is made or unkonw error.
        Error Code 4: If you use the downgrade function to upgrade the subscription.
        Error Code 5: The user already has the Subscription that you are trying to update.
        
    Returns:
        Success ( Str ): Console message informing if the downgrade was successful.
    """

    try:
        url = f'http://localhost:8010/api/v1/customerdata/{id}/'
        response = requests.get(url)
        customer = response.json()
        if response.status_code == 404:
            return print('Error code 1: the ID does not exist or is badly formated')
        
        data = customer['data']
        current_subscription = data["SUBSCRIPTION"]
        result = up_or_down(current_subscription, new_subscription) # return True, False or a string message
        if result == False:
            data['SUBSCRIPTION'] = new_subscription
            data['DOWNGRADE_DATE'] = datetime.now().isoformat() # .isoformat() make serializable the datetime
            try:
                data.pop('UPGRADE_DATE') # If UPGRADE_DATE exists then remove it, if not do nothing
            except:
                pass
            
            """
            The below for loop through each feature of ENABLED_FEATURES and, 
            for each iteration changes it to False
            """
            if new_subscription == 'free':
              for feature in data['ENABLED_FEATURES']:
                data["ENABLED_FEATURES"][feature] = False
                       
            put_request = requests.put(url, json=customer)
            if put_request.status_code == 200:
                print("Success!!")
                
        elif result == True:
            print('Error code 4: You can not upgrade a custommer subscription with this function')
        
        else:
            print(result) #The user already has the Subscription {current_subscription}
    
    except:
        raise Exception("Error code 3: other unknown error")
    
def up_or_down(current_subscription, new_subscription): 
    
    """_summary_
    The up_or_down function acts as an intermediary to validate that:
    - The new subscription is valid and exists.
    - The new subscription is not equal to the current subscription.
    - It assigns numerical values to each type of subscription to confirm whether 
        the new subscription has increased or decreased.
    
    Args:
        current_subscription ( Str ): It is the current subscription of the customer.
        new_subscription ( Str ) : It is the new desired subscription, only allow free, basic or premium.
        
    Returns:
        The returns are inputs for the functions upgrade and downgrade.
        True ( Boolean ) : If the new subscription is better than the current one.
        False ( Boolean ) : If the new subscription is lower than the current one.
        ( Str ): "Error code 2: the target subscription level is not reachable."
        ( Str ): f"Error code 5: the user already has the Subscription {current_subscription}".   
    """
    
    avaible_subscriptions = ['free', 'basic', 'premium'] 
    if new_subscription not in avaible_subscriptions:
        return ('Error code 2: the target subscription level is not reachable') 
      
    new_subscription_value = avaible_subscriptions.index(new_subscription)
    current_subscription_value = avaible_subscriptions.index(current_subscription)

    if new_subscription_value == current_subscription_value:
        return (f'Error code 5: The user already has the Subscription {current_subscription}')
    elif new_subscription_value > current_subscription_value:
        return True
    elif new_subscription_value < current_subscription_value:
        return False
 