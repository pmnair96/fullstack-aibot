# Azure OpenAI Setup Guide

## Prerequisites

1. **Azure Subscription**: You need an active Azure subscription (free tier available)
2. **Azure OpenAI Access**: Request access to Azure OpenAI Service (may require approval)

## Step 1: Create Azure OpenAI Resource

1. **Go to Azure Portal**: https://portal.azure.com/
2. **Create Resource**: Click "Create a resource"
3. **Search**: Look for "Azure OpenAI"
4. **Select**: Choose "Azure OpenAI" service
5. **Create**: Fill in the required fields:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Region**: Choose a supported region (e.g., East US, West Europe)
   - **Name**: Give your resource a unique name (e.g., `my-openai-resource`)
   - **Pricing Tier**: Choose your pricing tier (Standard S0 recommended)

## Step 2: Deploy a Model

1. **Go to Azure OpenAI Studio**: https://oai.azure.com/
2. **Select your resource**: Choose the resource you just created
3. **Go to Deployments**: Click on "Deployments" in the left sidebar
4. **Create New Deployment**:
   - **Model**: Choose `gpt-35-turbo` (recommended for chat)
   - **Deployment Name**: Give it a name (e.g., `gpt-35-turbo`)
   - **Model Version**: Use the latest version
   - **Scale Settings**: Choose appropriate settings for your needs

## Step 3: Get Your Credentials

1. **Go to Resource**: In Azure Portal, navigate to your OpenAI resource
2. **Keys and Endpoint**: Click on "Keys and Endpoint" in the left sidebar
3. **Copy Values**:
   - **Endpoint**: Copy the endpoint URL (e.g., `https://your-resource-name.openai.azure.com/`)
   - **Key**: Copy one of the access keys (KEY 1 or KEY 2)

## Step 4: Update Environment Variables

Update your `.env` file with the Azure credentials:

```properties
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
```

## Step 5: Update Render Environment Variables

If deploying to Render, update the environment variables in:
1. **Render Dashboard**: Go to your service settings
2. **Environment**: Add/update these variables:
   - `AZURE_OPENAI_ENDPOINT`: Your Azure endpoint URL
   - `AZURE_OPENAI_API_KEY`: Your Azure API key
   - `AZURE_OPENAI_API_VERSION`: `2024-02-15-preview`
   - `AZURE_OPENAI_DEPLOYMENT_NAME`: Your deployment name (e.g., `gpt-35-turbo`)

## Available Models

- **gpt-35-turbo**: Fast, cost-effective for most chat applications
- **gpt-4**: More capable but slower and more expensive
- **gpt-4-turbo**: Latest GPT-4 model with larger context window
- **gpt-35-turbo-16k**: GPT-3.5 with larger context window

## Pricing Information

- **Free Tier**: Azure offers $200 free credit for new accounts
- **Pay-as-you-go**: You pay only for what you use
- **Cost Control**: Set up budgets and alerts in Azure Portal

## Testing Your Setup

1. **Deploy your app**: Push your changes to trigger deployment
2. **Test chat**: Go to your frontend and send a message
3. **Check logs**: Monitor the backend logs for Azure API calls
4. **Verify responses**: You should see "Powered by Azure OpenAI" in responses

## Troubleshooting

### Common Issues:

1. **401 Authentication Error**:
   - Check your API key is correct
   - Verify the endpoint URL is correct
   - Ensure the resource is active

2. **404 Not Found**:
   - Check your deployment name is correct
   - Verify the model is deployed and active

3. **429 Rate Limit**:
   - You've exceeded your quota
   - Check your Azure billing and limits

4. **403 Forbidden**:
   - Your subscription may not have access to Azure OpenAI
   - Request access through Azure Portal

### Getting Help:

- **Azure Support**: Use Azure Portal support
- **Documentation**: https://docs.microsoft.com/en-us/azure/cognitive-services/openai/
- **Pricing Calculator**: https://azure.microsoft.com/en-us/pricing/calculator/

## Benefits of Azure OpenAI

- ✅ **Enterprise-grade**: Reliable, scalable infrastructure
- ✅ **Data Privacy**: Your data stays in your Azure tenant
- ✅ **Compliance**: Meets enterprise compliance requirements
- ✅ **Integration**: Seamless integration with other Azure services
- ✅ **Cost Control**: Detailed billing and cost management
- ✅ **Latest Models**: Access to latest OpenAI models
