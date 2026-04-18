targetScope = 'resourceGroup'

@description('Log Analytics workspace name.')
param workspaceName string

@description('Azure region for the workspace.')
param location string

@description('Tags applied to the workspace.')
param tags object = {}

@description('Workspace SKU.')
@allowed([
  'PerGB2018'
])
param sku string = 'PerGB2018'

@description('Retention period in days.')
@minValue(30)
@maxValue(730)
param retentionInDays int = 30

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: workspaceName
  location: location
  tags: tags
  properties: {
    retentionInDays: retentionInDays
  }
  sku: {
    name: sku
  }
}

output workspaceName string = workspace.name
output workspaceId string = workspace.id
