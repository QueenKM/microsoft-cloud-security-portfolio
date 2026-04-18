targetScope = 'resourceGroup'

@description('Network security group name.')
param name string

@description('Azure region for the network security group.')
param location string

@description('Tags applied to the network security group.')
param tags object = {}

@description('Optional Log Analytics workspace resource ID for diagnostic settings.')
param diagnosticWorkspaceId string = ''

@description('Enable diagnostic settings for the network security group.')
param enableDiagnostics bool = true

@description('Optional custom security rules to apply to the network security group.')
param customSecurityRules array = []

resource networkSecurityGroup 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    securityRules: [for rule in customSecurityRules: {
      name: rule.name
      properties: {
        access: rule.access
        direction: rule.direction
        destinationAddressPrefix: rule.destinationAddressPrefix
        destinationPortRange: rule.destinationPortRange
        priority: rule.priority
        protocol: rule.protocol
        sourceAddressPrefix: rule.sourceAddressPrefix
        sourcePortRange: rule.sourcePortRange
      }
    }]
  }
}

resource diagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (enableDiagnostics && diagnosticWorkspaceId != '') {
  name: '${name}-diag'
  scope: networkSecurityGroup
  properties: {
    workspaceId: diagnosticWorkspaceId
    logs: [
      {
        category: 'NetworkSecurityGroupEvent'
        enabled: true
      }
      {
        category: 'NetworkSecurityGroupRuleCounter'
        enabled: true
      }
    ]
  }
}

output networkSecurityGroupName string = networkSecurityGroup.name
output networkSecurityGroupId string = networkSecurityGroup.id
