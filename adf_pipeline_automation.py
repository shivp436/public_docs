import requests
from azure.identity import ClientSecretCredential
 
# Define your Azure AD tenant ID, client ID (application ID), and client secret
tenant_id = ''
client_id = ''
client_secret = ''
 
# Define your Azure Data Factory details
subscription_id = ''
resource_group_name = ''
data_factory_name = ''
 
# Function to authenticate and retrieve access token
def authenticate_client(tenant_id, client_id, client_secret):
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    token = credential.get_token('https://management.azure.com/.default').token
    print("token:", token)
    return token
 
# Function to retrieve pipeline details from Azure Data Factory
def get_pipeline_details(token, subscription_id, resource_group_name, data_factory_name):
    print("entered pipeline function")
    # Define the API endpoint to retrieve pipeline details
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.DataFactory/factories/{data_factory_name}/pipelines?api-version=2018-06-01"
 
    # Set headers with the access token for authentication
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
 
    # Make a GET request to the ADF API
    response = requests.get(url, headers=headers)
 
    # Check if request was successful
    if response.status_code == 200:
        pipelines = response.json()['value']
        print("Success bro")
        for pipeline in pipelines:
            print(f"Pipeline ID: {pipeline['name']}, Properties: {pipeline}")
    else:
        print(f"Failed to retrieve pipelines: {response.status_code}, {response.text}")
 
# Main function to orchestrate the process
def main():
    # Authenticate using service principal credentials
    token = authenticate_client(tenant_id, client_id, client_secret)
 
    # Retrieve and print pipeline details
    get_pipeline_details(token, subscription_id, resource_group_name, data_factory_name)
 
# Entry point of the script
if __name__ == '__main__':
    main()