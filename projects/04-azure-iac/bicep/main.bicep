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

@description('Deploy the optional demo Linux virtual machine.')
param deployDemoVirtualMachine bool = false

@description('Virtual machine size for the optional demo workload.')
param demoVirtualMachineSize string = 'Standard_B1s'

@description('Administrator username for the optional demo virtual machine.')
param demoVirtualMachineAdminUsername string = 'azureuser'

@description('SSH public key for the optional demo virtual machine. Required when deployDemoVirtualMachine is true.')
@secure()
param demoVirtualMachineSshPublicKey string = ''

@description('Create a public IP for the optional demo virtual machine.')
param demoVirtualMachinePublicIpEnabled bool = false

@description('Principal ID for the IT admin persona or group. Leave empty to skip RBAC assignment.')
param itAdminPrincipalId string = ''

@description('Principal type for the IT admin assignment.')
@allowed([
  'User'
  'Group'
  'ServicePrincipal'
])
param itAdminPrincipalType string = 'Group'

@description('Principal ID for the security analyst persona or group. Leave empty to skip RBAC assignment.')
param securityAnalystPrincipalId string = ''

@description('Principal type for the security analyst assignment.')
@allowed([
  'User'
  'Group'
  'ServicePrincipal'
])
param securityAnalystPrincipalType string = 'Group'

@description('Deploy Azure Monitor scheduled query alerts for the lab baseline.')
param enablePlatformAlertRules bool = true

@description('Optional email address for the alert action group. Leave empty to create rules without notifications.')
param alertNotificationEmail string = ''

@description('Evaluation frequency for the scheduled query alerts.')
param alertEvaluationFrequency string = 'PT5M'

@description('Lookback window for the scheduled query alerts.')
param alertWindowSize string = 'PT15M'

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
var demoVirtualMachineName = 'vm-${workloadPrefix}-${environmentName}-${uniqueSuffix}'
var alertActionGroupName = 'ag-${workloadPrefix}-${environmentName}-ops'
var readerRoleDefinitionId = 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
var contributorRoleDefinitionId = 'b24988ac-6180-42a0-ab88-20f7382dd24c'
var monitoringContributorRoleDefinitionId = '749f88d5-cbae-40b8-bcfc-e573ddc772fa'
var logAnalyticsReaderRoleDefinitionId = '73c42c96-874c-492b-b04d-ab87d138a893'
var rbacRoleAssignmentAlertQuery = loadTextContent('../../01-cloud-security-lab/queries/01-rbac-role-assignment-changes.kql')
var nsgChangeAlertQuery = loadTextContent('../../01-cloud-security-lab/queries/02-nsg-security-rule-changes.kql')
var diagnosticSettingsChangeAlertQuery = loadTextContent('../../01-cloud-security-lab/queries/03-diagnostic-settings-changes.kql')
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

module demoVirtualMachine './modules/linux-virtual-machine.bicep' = if (deployDemoVirtualMachine) {
  name: 'demoVirtualMachineDeployment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
  ]
  params: {
    adminUsername: demoVirtualMachineAdminUsername
    enablePublicIp: demoVirtualMachinePublicIpEnabled
    location: location
    name: demoVirtualMachineName
    size: demoVirtualMachineSize
    sshPublicKey: demoVirtualMachineSshPublicKey
    subnetResourceId: virtualNetwork.outputs.workloadSubnetId
    tags: baselineTags
  }
}

module itAdminWorkloadRole './modules/role-assignment.bicep' = if (itAdminPrincipalId != '') {
  name: 'itAdminWorkloadRoleAssignment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
  ]
  params: {
    assignmentGuidSeed: 'it-admin-demo-workload-contributor'
    principalId: itAdminPrincipalId
    principalType: itAdminPrincipalType
    roleDefinitionId: contributorRoleDefinitionId
  }
}

module itAdminMonitoringRole './modules/role-assignment.bicep' = if (itAdminPrincipalId != '') {
  name: 'itAdminMonitoringRoleAssignment'
  scope: resourceGroup(monitoringResourceGroupName)
  dependsOn: [
    monitoringResourceGroup
  ]
  params: {
    assignmentGuidSeed: 'it-admin-monitoring-contributor'
    principalId: itAdminPrincipalId
    principalType: itAdminPrincipalType
    roleDefinitionId: monitoringContributorRoleDefinitionId
  }
}

module securityAnalystDemoReaderRole './modules/role-assignment.bicep' = if (securityAnalystPrincipalId != '') {
  name: 'securityAnalystDemoReaderRoleAssignment'
  scope: resourceGroup(demoWorkloadResourceGroupName)
  dependsOn: [
    demoWorkloadResourceGroup
  ]
  params: {
    assignmentGuidSeed: 'security-analyst-demo-reader'
    principalId: securityAnalystPrincipalId
    principalType: securityAnalystPrincipalType
    roleDefinitionId: readerRoleDefinitionId
  }
}

module securityAnalystSecurityOperationsReaderRole './modules/role-assignment.bicep' = if (securityAnalystPrincipalId != '') {
  name: 'securityAnalystSecurityOperationsReaderRoleAssignment'
  scope: resourceGroup(securityOperationsResourceGroupName)
  dependsOn: [
    securityOperationsResourceGroup
  ]
  params: {
    assignmentGuidSeed: 'security-analyst-security-operations-reader'
    principalId: securityAnalystPrincipalId
    principalType: securityAnalystPrincipalType
    roleDefinitionId: readerRoleDefinitionId
  }
}

module securityAnalystLogAnalyticsReaderRole './modules/role-assignment.bicep' = if (securityAnalystPrincipalId != '') {
  name: 'securityAnalystLogAnalyticsReaderRoleAssignment'
  scope: resourceGroup(monitoringResourceGroupName)
  dependsOn: [
    monitoringResourceGroup
    logAnalyticsWorkspace
  ]
  params: {
    assignmentGuidSeed: 'security-analyst-log-analytics-reader'
    principalId: securityAnalystPrincipalId
    principalType: securityAnalystPrincipalType
    roleDefinitionId: logAnalyticsReaderRoleDefinitionId
  }
}

module alertActionGroup './modules/action-group.bicep' = if (enablePlatformAlertRules && alertNotificationEmail != '') {
  name: 'alertActionGroupDeployment'
  scope: resourceGroup(monitoringResourceGroupName)
  dependsOn: [
    monitoringResourceGroup
  ]
  params: {
    emailAddress: alertNotificationEmail
    name: alertActionGroupName
    shortName: 'asteraops'
  }
}

module rbacRoleAssignmentAlert './modules/scheduled-query-alert.bicep' = if (enablePlatformAlertRules) {
  name: 'rbacRoleAssignmentAlertDeployment'
  scope: resourceGroup(monitoringResourceGroupName)
  dependsOn: [
    monitoringResourceGroup
    logAnalyticsWorkspace
    alertActionGroup
  ]
  params: {
    actionGroupResourceIds: alertNotificationEmail != '' ? [alertActionGroup.outputs.actionGroupId!] : []
    alertDescription: 'Detects Azure RBAC role assignment changes in the lab subscription.'
    displayName: 'RBAC Role Assignment Changes'
    evaluationFrequency: alertEvaluationFrequency
    location: location
    name: 'al-${workloadPrefix}-${environmentName}-rbac-changes'
    query: rbacRoleAssignmentAlertQuery
    scopeResourceId: logAnalyticsWorkspace.outputs.workspaceId
    severity: 2
    tags: baselineTags
    threshold: 0
    windowSize: alertWindowSize
  }
}

module nsgSecurityRuleChangeAlert './modules/scheduled-query-alert.bicep' = if (enablePlatformAlertRules) {
  name: 'nsgSecurityRuleChangeAlertDeployment'
  scope: resourceGroup(monitoringResourceGroupName)
  dependsOn: [
    monitoringResourceGroup
  ]
  params: {
    actionGroupResourceIds: alertNotificationEmail != '' ? [alertActionGroup.outputs.actionGroupId!] : []
    alertDescription: 'Detects network security group and security rule changes in the lab subscription.'
    displayName: 'NSG Or Security Rule Changes'
    evaluationFrequency: alertEvaluationFrequency
    location: location
    name: 'al-${workloadPrefix}-${environmentName}-nsg-changes'
    query: nsgChangeAlertQuery
    scopeResourceId: logAnalyticsWorkspace.outputs.workspaceId
    severity: 2
    tags: baselineTags
    threshold: 0
    windowSize: alertWindowSize
  }
}

module diagnosticSettingsChangeAlert './modules/scheduled-query-alert.bicep' = if (enablePlatformAlertRules) {
  name: 'diagnosticSettingsChangeAlertDeployment'
  scope: resourceGroup(monitoringResourceGroupName)
  dependsOn: [
    monitoringResourceGroup
  ]
  params: {
    actionGroupResourceIds: alertNotificationEmail != '' ? [alertActionGroup.outputs.actionGroupId!] : []
    alertDescription: 'Detects diagnostic settings changes that could reduce visibility in the lab.'
    displayName: 'Diagnostic Settings Changes'
    evaluationFrequency: alertEvaluationFrequency
    location: location
    name: 'al-${workloadPrefix}-${environmentName}-diag-changes'
    query: diagnosticSettingsChangeAlertQuery
    scopeResourceId: logAnalyticsWorkspace.outputs.workspaceId
    severity: 1
    tags: baselineTags
    threshold: 0
    windowSize: alertWindowSize
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
output demoVirtualMachineName string = deployDemoVirtualMachine ? demoVirtualMachine.outputs.virtualMachineName! : ''
output demoVirtualMachineResourceId string = deployDemoVirtualMachine ? demoVirtualMachine.outputs.virtualMachineId! : ''
output alertActionGroupName string = alertNotificationEmail != '' ? alertActionGroup.outputs.actionGroupName! : ''
