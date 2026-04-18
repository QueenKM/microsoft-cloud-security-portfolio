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

@description('Optional Log Analytics workspace resource ID for diagnostic settings.')
param diagnosticWorkspaceId string = ''

@description('Enable diagnostic settings for the blob service.')
param enableDiagnostics bool = true

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

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    deleteRetentionPolicy: {
      days: 7
      enabled: enableVersioning
    }
    isVersioningEnabled: enableVersioning
  }
}

resource diagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (enableDiagnostics && diagnosticWorkspaceId != '') {
  name: '${storageAccount.name}-blob-diag'
  scope: blobService
  properties: {
    workspaceId: diagnosticWorkspaceId
    logs: [
      {
        category: 'StorageRead'
        enabled: true
      }
      {
        category: 'StorageWrite'
        enabled: true
      }
      {
        category: 'StorageDelete'
        enabled: true
      }
    ]
  }
}

output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
