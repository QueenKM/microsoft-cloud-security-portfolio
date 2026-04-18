# Project 04: Infrastructure as Code for Azure

## Goal

Automate the deployment of a secure Azure baseline using `Bicep`, `Terraform`, or both.

## Why This Project Matters

This project proves repeatability, operational maturity, and engineering discipline. It also strengthens the security lab by making the infrastructure reproducible.

## Core Scope

- resource group and naming model
- virtual network and subnets
- network security groups
- storage account
- VM or App Service
- diagnostic settings and logging
- RBAC assignment model
- optional CI validation with GitHub Actions

## Deliverables

- Bicep or Terraform modules
- environment parameter files
- architecture diagram
- deployment guide
- CI workflow
- validation checklist

## Current Implementation

- `Bicep` is the first implemented path for the Azure baseline.
- The current scope creates the lab resource groups, a `Log Analytics workspace`, a `VNet` with two subnets, two `NSG`s, and a secure demo `Storage Account`.
- Supported diagnostic settings are wired to `Log Analytics` for `NSG` and storage blob service logs.
- The Bicep baseline is designed to support `01-cloud-security-lab`.

## Starter Docs

- [Deployment Guide](docs/deployment-guide.md)
- [Validation Checklist](docs/validation-checklist.md)

## Bicep Entry Point

- [bicep/main.bicep](bicep/main.bicep)

## Build Phases

1. Design the landing zone baseline.
2. Build the first deployment in one IaC language.
3. Add security defaults, diagnostics, and tags.
4. Validate deployment and document the workflow.
5. Add CI and optionally recreate the same baseline in the second language.

## Evidence To Capture

- deployment tree
- code structure screenshots
- successful deployment output
- CI run screenshot
- before/after security improvements

## Cert Alignment

`AZ-104`, `AZ-305`
