# UZ_AGENTIC_RAG
Agentic RAG AI Assistant tool
To run this program the following commands need to be used:

1. Logging in to Azure Account (If you decide to try using Azure again):

    "az login"

2. Open Docker on your personal device and build it:

    "docker build -t myaicrr.azurecr.io/my-aii-assistant:latest ."

3. Push changes made in your code to Docker

    "docker push myaicrr.azurecr.io/my-aii-assistant:latest"

4. Configure the Docker Container to your Azure account:

    "az webapp config container set --name my-aii-assistant-app \ 
    --resource-group myResourceGroup \
    --container-registry-url https://myaicrr.azurecr.io \
    --container-registry-user $(az acr credential show --name myaicrr --query username -o tsv) \
    --container-registry-password $(az acr credential show --name myaicrr --query "passwords[0].value" -o tsv) \
    --docker-custom-image-name myaicrr.azurecr.io/my-aii-assistant:latest"

5. Login to Azure with credientials (again):

    "az acr login --name myaicrr"

6. Push docker changes to the azure web app:

    "docker push myaicrr.azurecr.io/my-aii-assistant:latest"

7. restart azure web app:

    "az webapp restart --name my-aii-assistant-app --resource-group myResourceGroup"

8. Write a curl post request to test endpoint:

    "curl -X POST https://my-aii-assistant-app.azurewebsites.net/chat \            
     -H "Content-Type: application/json" \
     -d '{"query":"Hello", "user_id":"test_user"}'"
