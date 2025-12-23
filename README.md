# Vault Regression Testing Framework

[![CI](https://github.com/nhsy/vault-regression-testing/actions/workflows/ci.yml/badge.svg)](https://github.com/nhsy/vault-regression-testing/actions/workflows/ci.yml)

A robust regression testing framework for HashiCorp Vault, designed to automate infrastructure setup, configuration, and verification using modern tools.

## Project Overview

This project provides a Vault test environment running in Docker. It uses Terraform to configure Vault resources and Pytest to verify the setup against specific regression scenarios. All tasks are orchestrated through a `Taskfile`.

## Key Features

- **Automation**: Fully automated initialization, unsealing, and token management.
- **Testing**: Extended Pytest suite covering health checks, KV secrets, AppRole authentication, security policies, and operational status.
- **Audit Logging**: Configurable file-based audit logging (enabled to stdout by default).
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
├── configs/               # Vault configuration files
│   └── vault.hcl          # Vault server config (Docker Config)
├── docker-compose.yaml    # Docker infrastructure
├── terraform/             # Vault resource management
│   ├── main.tf            # Provider and core setup
│   ├── audit.tf           # Audit logging configuration
│   ├── auth_approle.tf    # AppRole configuration
│   ├── secrets_kv.tf      # KV secrets engine
│   └── policies.tf        # Access control policies
├── tests/                 # Pytest regression suite
│   ├── conftest.py        # Shared fixtures & path handling
│   ├── test_approle.py    # AppRole auth tests
│   ├── test_health.py     # System health checks
│   ├── test_kv.py         # Secret readability tests
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
*Note: `task all` runs `prereqs`, `lint`, `up`, `init`, `unseal`, `config`, and `test`. It leaves the environment running for inspection.*

### 2. Individual Tasks
- `task prereqs`: Check if all required tools (Docker, Terraform, jq, Python) are installed.
- `task clean`: Cleanup temporary files and Docker resources (preserves `.venv`).
- `task setup`: Setup Python virtual environment & install dependencies.
- `task lint`: Run flake8 and black check on the `tests/` directory.
- `task up`: Start Vault container.
- `task init`: Initialize Vault and generate `.vault_init.json`.
- `task unseal`: Unseal the Vault using stored keys.
- `task config`: Apply Terraform configuration (KV, AppRole, Policies, Audit).
- `task test`: Run the full pytest suite.
- `task upgrade`: Upgrade Vault version (configurable via `VAULT_VERSION_UPGRADE` in `.env`) and re-run regression suite.
- `task status`: Check the current status of the Vault server.
- `task teardown`: Destroy Terraform resources.
- `task down`: Stop the Vault container and remove networks.

## Documentation

For a detailed analysis of the architecture, setup instructions, and verification steps, refer to the [Solution Outline](docs/solution-outline.md).

---
*Note: This framework is intended for regression testing and development environments.*