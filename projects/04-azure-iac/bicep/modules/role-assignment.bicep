targetScope = 'resourceGroup'

@description('Principal ID to receive the role assignment.')
param principalId string

@description('Principal type for the role assignment.')
@allowed([
  'User'
  'Group'
  'ServicePrincipal'
])
param principalType string

@description('Role definition GUID for the built-in role.')
param roleDefinitionId string

@description('Extra seed value to keep deterministic role assignment names unique.')
param assignmentGuidSeed string = ''

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, principalId, roleDefinitionId, assignmentGuidSeed)
  properties: {
    principalId: principalId
    principalType: principalType
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
  }
}

output roleAssignmentId string = roleAssignment.id
