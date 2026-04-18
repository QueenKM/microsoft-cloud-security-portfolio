targetScope = 'subscription'

@description('Resource group name.')
param name string

@description('Azure region for the resource group.')
param location string

@description('Tags applied to the resource group.')
param tags object = {}

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: name
  location: location
  tags: tags
}

output resourceGroupName string = resourceGroup.name
output resourceGroupId string = resourceGroup.id
