targetScope = 'subscription'

@description('Primary Azure region for the sandbox baseline.')
param location string = 'westeurope'

@description('Short environment label used in naming and tags.')
param environmentName string = 'sandbox'

@description('Short workload prefix used in resource names.')
param workloadPrefix string = 'astera'

@description('Optional extra tags merged into the default baseline tags.')
param tags object = {}

@description('Retention period for the Log Analytics workspace.')
@minValue(30)
@maxValue(730)
param logAnalyticsRetentionInDays int = 30

@description('SKU for the Log Analytics workspace.')
@allowed([
  'PerGB2018'
])
param logAnalyticsSku string = 'PerGB2018'

@description('SKU for the demo storage account.')
@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_RAGRS'
])
param storageSku string = 'Standard_LRS'

@description('Enable blob versioning and soft delete for the demo storage account.')
param enableStorageVersioning bool = true

var uniqueSuffix = take(uniqueString(subscription().subscriptionId, environmentName, location), 6)
var monitoringResourceGroupName = 'rg-${workloadPrefix}-${environmentName}-identity-monitoring'
var securityOperationsResourceGroupName = 'rg-${workloadPrefix}-${environmentName}-security-operations'
var demoWorkloadResourceGroupName = 'rg-${workloadPrefix}-${environmentName}-demo-workload'
var logAnalyticsWorkspaceName = 'law-${workloadPrefix}-${environmentName}-${uniqueSuffix}'
var storageAccountName = toLower(take(replace('st${workloadPrefix}${environmentName}${uniqueSuffix}', '-', ''), 24))
var baselineTags = union({
  environment: environmentName
  managedBy: 'bicep'
  owner: 'QueenKM'
  project: 'azure-iac'
  scenario: 'AsteraUniversity'
  workload: 'cloud-security-lab'
}, tags)

module monitoringResourceGroup './modules/resource-group.bicep' = {
  name: 'monitoringResourceGroupDeployment'
  params: {
    location: location
    name: monitoringResourceGroupName
    tags: baselineTags
  }
}

module securityOperationsResourceGroup './modules/resource-group.bicep' = {
  name: 'securityOperationsResourceGroupDeployment'
  params: {
    location: location
    name: securityOperationsResourceGroupName
    tags: baselineTags
  }
}

module demoWorkloadResourceGroup './modules/resource-group.bicep' = {
  name: 'demoWorkloadResourceGroupDeployment'
  params: {
    location: location
    name: demoWorkloadResourceGroupName
    tags: baselineTags
  }
}

module logAnalyticsWorkspace './modules/log-analytics-workspace.bicep' = {
  name: 'logAnalyticsWorkspaceDeployment'
  scope: resourceGroup(monitoringResourceGroupName)
  dependsOn: [
    monitoringResourceGroup
  ]
  params: {
    location: location
    retentionInDays: logAnalyticsRetentionInDays
    sku: logAnalyticsSku
    tags: baselineTags
    workspaceName: logAnalyticsWorkspaceName
  }
}

module demoStorageAccount './modules/storage-account.bicep' = {
  name: 'demoStorageAccountDeployment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
  ]
  params: {
    enableVersioning: enableStorageVersioning
    location: location
    storageAccountName: storageAccountName
    storageSku: storageSku
    tags: baselineTags
  }
}

output monitoringResourceGroupName string = monitoringResourceGroupName
output securityOperationsResourceGroupName string = securityOperationsResourceGroupName
output demoWorkloadResourceGroupName string = demoWorkloadResourceGroupName
output logAnalyticsWorkspaceName string = logAnalyticsWorkspace.outputs.workspaceName
output logAnalyticsWorkspaceResourceId string = logAnalyticsWorkspace.outputs.workspaceId
output storageAccountName string = demoStorageAccount.outputs.storageAccountName
output storageAccountResourceId string = demoStorageAccount.outputs.storageAccountId
