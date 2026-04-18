targetScope = 'resourceGroup'

@description('Virtual network name.')
param name string

@description('Azure region for the virtual network.')
param location string

@description('Tags applied to the virtual network.')
param tags object = {}

@description('Address prefixes for the virtual network.')
param addressPrefixes array

@description('Management subnet name.')
param managementSubnetName string

@description('Management subnet address prefix.')
param managementSubnetAddressPrefix string

@description('Optional network security group ID for the management subnet.')
param managementNetworkSecurityGroupId string = ''

@description('Workload subnet name.')
param workloadSubnetName string

@description('Workload subnet address prefix.')
param workloadSubnetAddressPrefix string

@description('Optional network security group ID for the workload subnet.')
param workloadNetworkSecurityGroupId string = ''

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    addressSpace: {
      addressPrefixes: addressPrefixes
    }
  }
}

resource managementSubnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' = {
  parent: virtualNetwork
  name: managementSubnetName
  properties: union({
    addressPrefix: managementSubnetAddressPrefix
  }, managementNetworkSecurityGroupId == '' ? {} : {
    networkSecurityGroup: {
      id: managementNetworkSecurityGroupId
    }
  })
}

resource workloadSubnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' = {
  parent: virtualNetwork
  name: workloadSubnetName
  properties: union({
    addressPrefix: workloadSubnetAddressPrefix
    serviceEndpoints: [
      {
        service: 'Microsoft.Storage'
      }
    ]
  }, workloadNetworkSecurityGroupId == '' ? {} : {
    networkSecurityGroup: {
      id: workloadNetworkSecurityGroupId
    }
  })
}

output virtualNetworkName string = virtualNetwork.name
output virtualNetworkId string = virtualNetwork.id
output managementSubnetId string = managementSubnet.id
output workloadSubnetId string = workloadSubnet.id
