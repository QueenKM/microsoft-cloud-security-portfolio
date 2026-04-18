targetScope = 'resourceGroup'

@description('Scheduled query alert rule name.')
param name string

@description('Azure region for the alert rule.')
param location string

@description('Display name for the alert rule.')
param displayName string

@description('Description for the alert rule.')
param alertDescription string

@description('Target scope for the alert query, usually the Log Analytics workspace resource ID.')
param scopeResourceId string

@description('KQL query used by the alert.')
param query string

@description('Alert severity from 0 to 4.')
@minValue(0)
@maxValue(4)
param severity int = 2

@description('Evaluation frequency in ISO 8601 duration format.')
param evaluationFrequency string = 'PT5M'

@description('Lookback window size in ISO 8601 duration format.')
param windowSize string = 'PT15M'

@description('Threshold for the alert query aggregation.')
param threshold int = 0

@description('Action group resource IDs to notify when the alert fires.')
param actionGroupResourceIds array = []

@description('Skip query validation to support early lab deployments before data arrives.')
param skipQueryValidation bool = true

@description('Tags applied to the alert rule.')
param tags object = {}

resource scheduledQueryRule 'Microsoft.Insights/scheduledQueryRules@2023-12-01' = {
  name: name
  location: location
  kind: 'LogAlert'
  properties: {
    actions: {
      actionGroups: actionGroupResourceIds
      customProperties: {}
    }
    criteria: {
      allOf: [
        {
          failingPeriods: {
            minFailingPeriodsToAlert: 1
            numberOfEvaluationPeriods: 1
          }
          operator: 'GreaterThan'
          query: query
          threshold: threshold
          timeAggregation: 'Count'
        }
      ]
    }
    description: alertDescription
    displayName: displayName
    enabled: true
    evaluationFrequency: evaluationFrequency
    resolveConfiguration: {
      autoResolved: true
      timeToResolve: 'PT15M'
    }
    scopes: [
      scopeResourceId
    ]
    severity: severity
    skipQueryValidation: skipQueryValidation
    windowSize: windowSize
  }
  tags: tags
}

output alertRuleId string = scheduledQueryRule.id
