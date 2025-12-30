# Vault Regression Testing Framework

[![CI](https://github.com/nhsy/vault-regression-testing/actions/workflows/ci.yml/badge.svg)](https://github.com/nhsy/vault-regression-testing/actions/workflows/ci.yml)

A robust regression testing framework for HashiCorp Vault, designed to automate infrastructure setup, configuration, and verification using modern tools.

## Project Overview

This project provides a Vault test environment running in Docker. It uses Terraform to configure Vault resources and Pytest to verify the setup against specific regression scenarios. All tasks are orchestrated through a `Taskfile`.

## Key Features

- **Automation**: Fully automated initialization, unsealing, and token management.
- **Testing**: Extended Pytest suite covering health checks, KV secrets, AppRole authentication, PKI certificates, security policies, and operational status.
- **OIDC Authentication**: Native OIDC integration with GitHub Actions provided by Vault's JWT auth backend.
- **Audit Logging**: Configurable file-based audit logging (enabled to stdout by default).
- **LDAP Integration**: Integrated OpenLDAP environment for testing authentication, group mapping, and dynamic secrets.
- **Database Secrets**: PostgreSQL integration with dynamic database credential generation and rotation testing.
- **Code Quality**: Automated Python linting with `flake8` and formatting with `black` (integrated into the pipeline).

## Prerequisites

- **Docker & Docker Compose**
- **Terraform**
- **Go Task** (`task`)
- **Python 3.14+**
- **jq**

You can verify your environment by running:
```bash
task prereqs
```

## Project Structure

```text
.
├── Taskfile.yml           # Core orchestration tasks
├── configs/               # Configuration files
│   ├── vault/             # Vault server config
│   │   └── vault.hcl
│   ├── ldap/              # LDAP seed data
│   │   └── ldap-example.ldif
│   └── postgres/          # PostgreSQL initialization
│       └── init.sql
├── docker-compose.yaml    # Docker infrastructure
├── terraform/             # Vault resource management
│   ├── main.tf            # Provider and core setup
│   ├── variables.tf       # Configuration variables
│   ├── audit.tf           # Audit logging configuration
│   ├── auth_oidc.tf       # OIDC configuration for GitHub Actions
│   ├── auth_approle.tf    # AppRole configuration
│   ├── auth_ldap.tf       # LDAP Auth configuration
│   ├── identity_ldap.tf   # Identity & Group mapping
│   ├── secrets_kv.tf      # KV secrets engine
│   ├── secrets_ldap.tf    # LDAP secrets engine
│   ├── secrets_database.tf # Database secrets engine
│   └── policies.tf        # Access control policies
├── tests/                 # Pytest regression suite
│   ├── conftest.py        # Shared fixtures & path handling
│   ├── test_approle.py    # AppRole auth tests
│   ├── test_pki.py        # PKI secrets engine tests
│   ├── test_database.py   # Database dynamic secrets tests
│   ├── test_health.py     # System health checks
│   ├── test_kv.py         # Secret readability tests
│   ├── test_ldap.py       # LDAP integration tests
│   └── test_enhanced.py   # Security, operational, and KV metadata tests
├── improvements.md        # Roadmap for future improvements
├── .env                   # Environment variables (auto-sourced)
├── .flake8                # Linter configuration
└── requirements.txt       # Python dependencies
```

## Getting Started

### 1. Initialize and Run Everything
First, set up the virtual environment (run once):
```bash
task setup
```

Then, run the full regression pipeline:
```bash
task all
```
*Note: `task all` runs `prereqs`, `lint`, `up`, `init`, `terraform:apply`, and `test`. It leaves the environment running for inspection.*

### 2. Individual Tasks
- `task prereqs`: Check if all required tools (Docker, Terraform, jq, Python) are installed.
- `task clean`: Cleanup temporary files and Docker resources (preserves `.venv`).
- `task setup`: Setup Python virtual environment, install dependencies, and create `.env` from template.
- `task lint`: Run flake8 and black check on the `tests/` directory.
- `task up`: Start Vault, PostgreSQL, and OpenLDAP containers.
- `task init`: Initialize both LDAP and Vault (runs `ldap:init`, `vault:init`, and `vault:unseal`).
- `task ldap:init`: Seed OpenLDAP with sample users and groups.
- `task ldap:status`: Check connectivity to OpenLDAP and list users.
- `task postgres:status`: Check connectivity to PostgreSQL database.
- `task postgres:test`: Run PostgreSQL connection tests (readonly and readwrite roles).
- `task vault:init`: Initialize Vault and generate `.vault_init.json`.
- `task vault:unseal`: Unseal the Vault using stored keys.
- `task vault:status`: Check the current status of the Vault server.
- `task vault:upgrade`: Upgrade Vault version (configurable via `VAULT_VERSION_UPGRADE` in `.env`) and re-run regression suite.
- `task terraform:apply`: Apply Terraform configuration (KV, AppRole, LDAP, Database, Policies, Audit).
- `task terraform:destroy`: Destroy Terraform resources.
- `task test`: Run the full pytest suite.
- `task down`: Stop the containers and remove networks.

## Documentation

For a detailed analysis of the architecture, setup instructions, and verification steps, refer to the [Solution Outline](docs/solution-outline.md).

---
*Note: This framework is intended for regression testing and development environments.*