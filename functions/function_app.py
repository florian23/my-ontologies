import json
import requests
from azure.functions import HttpRequest, HttpResponse
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

def main(req: HttpRequest) -> HttpResponse:
    action = req.params.get('action')
    credential = DefaultAzureCredential()
    client = ContainerInstanceManagementClient(credential, 'b908a739-b5f8-4fe2-8572-90c18b31355c')
    resource_group = 'my-ontologies_group'
    container_group_name = 'fuseki'
    
    if action == 'upload':
        # Start the container
        client.container_groups.start(resource_group, container_group_name)
        
        ontology = req.files['ontology'].read()
        response = requests.post('http://flocontainer.ctfvdbc0b2faawej.germanywestcentral.azurecontainer.io:3030/dataset/data', files={'file': ontology})
        
        # Stop the container
        client.container_groups.stop(resource_group, container_group_name)
        
        return HttpResponse(response.content, status_code=response.status_code)
    elif action == 'query':
        # Start the container
        client.container_groups.start(resource_group, container_group_name)
        
        query = req.params.get('query')
        response = requests.post('http://flocontainer.ctfvdbc0b2faawej.germanywestcentral.azurecontainer.io:3030/dataset/sparql', data={'query': query})
        
        # Stop the container
        client.container_groups.stop(resource_group, container_group_name)
        
        return HttpResponse(response.content, status_code=response.status_code)
    else:
        return HttpResponse("Invalid action.", status_code=400)