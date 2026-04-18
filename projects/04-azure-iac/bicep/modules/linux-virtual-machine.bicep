targetScope = 'resourceGroup'

@description('Virtual machine name.')
param name string

@description('Azure region for the virtual machine.')
param location string

@description('Tags applied to the virtual machine and related resources.')
param tags object = {}

@description('Virtual machine size.')
param size string = 'Standard_B1s'

@description('Administrator username for the virtual machine.')
param adminUsername string = 'azureuser'

@description('SSH public key for the virtual machine.')
@secure()
param sshPublicKey string

@description('Subnet resource ID for the virtual machine network interface.')
param subnetResourceId string

@description('Create a public IP address for the virtual machine.')
param enablePublicIp bool = false

var networkInterfaceName = 'nic-${name}'
var publicIpName = 'pip-${name}'
var osDiskName = 'osdisk-${name}'

resource publicIp 'Microsoft.Network/publicIPAddresses@2024-05-01' = if (enablePublicIp) {
  name: publicIpName
  location: location
  tags: tags
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAddressVersion: 'IPv4'
    publicIPAllocationMethod: 'Static'
  }
}

resource networkInterface 'Microsoft.Network/networkInterfaces@2024-05-01' = {
  name: networkInterfaceName
  location: location
  tags: tags
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: union({
          privateIPAllocationMethod: 'Dynamic'
          subnet: {
            id: subnetResourceId
          }
        }, enablePublicIp ? {
          publicIPAddress: {
            id: publicIp.id
          }
        } : {})
      }
    ]
  }
}

resource virtualMachine 'Microsoft.Compute/virtualMachines@2024-07-01' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    hardwareProfile: {
      vmSize: size
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: networkInterface.id
          properties: {
            primary: true
          }
        }
      ]
    }
    osProfile: {
      adminUsername: adminUsername
      computerName: name
      linuxConfiguration: {
        disablePasswordAuthentication: true
        provisionVMAgent: true
        ssh: {
          publicKeys: [
            {
              keyData: sshPublicKey
              path: '/home/${adminUsername}/.ssh/authorized_keys'
            }
          ]
        }
      }
    }
    storageProfile: {
      imageReference: {
        offer: '0001-com-ubuntu-server-jammy'
        publisher: 'Canonical'
        sku: '22_04-lts-gen2'
        version: 'latest'
      }
      osDisk: {
        createOption: 'FromImage'
        deleteOption: 'Delete'
        managedDisk: {
          storageAccountType: 'StandardSSD_LRS'
        }
        name: osDiskName
      }
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
      }
    }
  }
}

output virtualMachineName string = virtualMachine.name
output virtualMachineId string = virtualMachine.id
output networkInterfaceId string = networkInterface.id
output publicIpId string = enablePublicIp ? publicIp.id : ''
