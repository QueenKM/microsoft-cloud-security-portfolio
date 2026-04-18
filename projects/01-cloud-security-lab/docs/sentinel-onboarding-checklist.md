# Microsoft Sentinel Onboarding Checklist

## Goal

Provide a reproducible checklist for enabling Microsoft Sentinel in the lab and collecting enough data to demonstrate detections and incident response.

## Prerequisites

- active Azure sandbox subscription
- one `Log Analytics workspace`
- sufficient permissions to enable Sentinel and connect data sources
- Entra ID and Azure activity logging available for the tenant

## Workspace Setup

- [ ] create or confirm the `Log Analytics workspace`
- [ ] define retention settings suitable for the lab budget
- [ ] document workspace region and naming convention

## Enable Sentinel

- [ ] enable `Microsoft Sentinel` on the chosen workspace
- [ ] record the workspace name and subscription in the README or notes
- [ ] capture the empty overview page before data starts flowing

## Connect Data Sources

- [ ] connect `Azure Activity`
- [ ] connect `Entra ID Sign-in Logs`, if available
- [ ] connect `Entra ID Audit Logs`, if available
- [ ] connect `Defender for Cloud`, if available in the tenant
- [ ] enable diagnostic settings for the demo workload

## Initial Analytics Content

- [ ] create a rule for repeated failed sign-ins by user
- [ ] create a rule for repeated failed sign-ins by IP
- [ ] create a rule or workbook view for RBAC or role assignment changes
- [ ] document thresholds and why they were chosen for a small lab

## Investigation Readiness

- [ ] configure incident creation settings
- [ ] define severity mapping for the starter detections
- [ ] note who acts as the `security-analyst` persona
- [ ] prepare one short incident response walkthrough

## Portfolio Evidence

- [ ] screenshot of enabled data connectors
- [ ] screenshot of analytic rules
- [ ] screenshot of an incident or alert
- [ ] one short summary of what data was available and what was missing

## Common Pitfalls

- connectors may require licensing or tenant capabilities not present in a student lab
- no detections will fire until logs actually arrive in the workspace
- thresholds that are too high can make a small lab look silent
- thresholds that are too low can create noisy or misleading incidents
