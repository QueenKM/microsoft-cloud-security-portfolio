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

@description('Enable resource diagnostic settings that send supported logs to Log Analytics.')
param enableResourceDiagnostics bool = true

@description('Virtual network address space for the sandbox baseline.')
param virtualNetworkAddressPrefixes array = [
  '10.42.0.0/16'
]

@description('Address prefix for the management subnet.')
param managementSubnetAddressPrefix string = '10.42.1.0/24'

@description('Address prefix for the workload subnet.')
param workloadSubnetAddressPrefix string = '10.42.2.0/24'

var uniqueSuffix = take(uniqueString(subscription().subscriptionId, environmentName, location), 6)
var monitoringResourceGroupName = 'rg-${workloadPrefix}-${environmentName}-identity-monitoring'
var securityOperationsResourceGroupName = 'rg-${workloadPrefix}-${environmentName}-security-operations'
var demoWorkloadResourceGroupName = 'rg-${workloadPrefix}-${environmentName}-demo-workload'
var logAnalyticsWorkspaceName = 'law-${workloadPrefix}-${environmentName}-${uniqueSuffix}'
var storageAccountName = toLower(take(replace('st${workloadPrefix}${environmentName}${uniqueSuffix}', '-', ''), 24))
var virtualNetworkName = 'vnet-${workloadPrefix}-${environmentName}-core'
var managementNetworkSecurityGroupName = 'nsg-${workloadPrefix}-${environmentName}-management'
var workloadNetworkSecurityGroupName = 'nsg-${workloadPrefix}-${environmentName}-workload'
var managementSubnetName = 'snet-management'
var workloadSubnetName = 'snet-workload'
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

module managementNetworkSecurityGroup './modules/network-security-group.bicep' = {
  name: 'managementNetworkSecurityGroupDeployment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
    logAnalyticsWorkspace
  ]
  params: {
    diagnosticWorkspaceId: logAnalyticsWorkspace.outputs.workspaceId
    enableDiagnostics: enableResourceDiagnostics
    location: location
    name: managementNetworkSecurityGroupName
    tags: baselineTags
  }
}

module workloadNetworkSecurityGroup './modules/network-security-group.bicep' = {
  name: 'workloadNetworkSecurityGroupDeployment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
    logAnalyticsWorkspace
  ]
  params: {
    diagnosticWorkspaceId: logAnalyticsWorkspace.outputs.workspaceId
    enableDiagnostics: enableResourceDiagnostics
    location: location
    name: workloadNetworkSecurityGroupName
    tags: baselineTags
  }
}

module virtualNetwork './modules/virtual-network.bicep' = {
  name: 'virtualNetworkDeployment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
    managementNetworkSecurityGroup
    workloadNetworkSecurityGroup
  ]
  params: {
    addressPrefixes: virtualNetworkAddressPrefixes
    location: location
    managementNetworkSecurityGroupId: managementNetworkSecurityGroup.outputs.networkSecurityGroupId
    managementSubnetAddressPrefix: managementSubnetAddressPrefix
    managementSubnetName: managementSubnetName
    name: virtualNetworkName
    tags: baselineTags
    workloadNetworkSecurityGroupId: workloadNetworkSecurityGroup.outputs.networkSecurityGroupId
    workloadSubnetAddressPrefix: workloadSubnetAddressPrefix
    workloadSubnetName: workloadSubnetName
  }
}

module demoStorageAccount './modules/storage-account.bicep' = {
  name: 'demoStorageAccountDeployment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
    logAnalyticsWorkspace
  ]
  params: {
    diagnosticWorkspaceId: logAnalyticsWorkspace.outputs.workspaceId
    enableDiagnostics: enableResourceDiagnostics
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
output virtualNetworkName string = virtualNetwork.outputs.virtualNetworkName
output virtualNetworkResourceId string = virtualNetwork.outputs.virtualNetworkId
output managementSubnetResourceId string = virtualNetwork.outputs.managementSubnetId
output workloadSubnetResourceId string = virtualNetwork.outputs.workloadSubnetId
output managementNetworkSecurityGroupResourceId string = managementNetworkSecurityGroup.outputs.networkSecurityGroupId
output workloadNetworkSecurityGroupResourceId string = workloadNetworkSecurityGroup.outputs.networkSecurityGroupId
output storageAccountName string = demoStorageAccount.outputs.storageAccountName
output storageAccountResourceId string = demoStorageAccount.outputs.storageAccountId
