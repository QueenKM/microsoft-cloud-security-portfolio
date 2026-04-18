targetScope = 'resourceGroup'

@description('Storage account name.')
param storageAccountName string

@description('Azure region for the storage account.')
param location string

@description('Storage SKU.')
@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_RAGRS'
])
param storageSku string = 'Standard_LRS'

@description('Tags applied to the storage account.')
param tags object = {}

@description('Enable blob versioning and soft delete.')
param enableVersioning bool = true

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageSku
  }
  kind: 'StorageV2'
  tags: tags
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: true
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Enabled'
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = if (enableVersioning) {
  parent: storageAccount
  name: 'default'
  properties: {
    deleteRetentionPolicy: {
      days: 7
      enabled: true
    }
    isVersioningEnabled: true
  }
}

output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
