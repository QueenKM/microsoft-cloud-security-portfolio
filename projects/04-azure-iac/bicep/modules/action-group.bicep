targetScope = 'resourceGroup'

@description('Action group name.')
param name string

@description('Short name for the action group.')
param shortName string

@description('Email address to receive alert notifications.')
param emailAddress string

@description('Use the common alert schema for notifications.')
param useCommonAlertSchema bool = true

resource actionGroup 'Microsoft.Insights/actionGroups@2023-01-01' = {
  name: name
  location: 'global'
  properties: {
    armRoleReceivers: []
    automationRunbookReceivers: []
    azureAppPushReceivers: []
    azureFunctionReceivers: []
    emailReceivers: [
      {
        emailAddress: emailAddress
        name: 'primary-email'
        useCommonAlertSchema: useCommonAlertSchema
      }
    ]
    enabled: true
    eventHubReceivers: []
    groupShortName: shortName
    itsmReceivers: []
    logicAppReceivers: []
    smsReceivers: []
    voiceReceivers: []
    webhookReceivers: []
  }
}

output actionGroupId string = actionGroup.id
output actionGroupName string = actionGroup.name
