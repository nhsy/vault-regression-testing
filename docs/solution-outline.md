# Vault Regression Testing Framework - Comprehensive Guide

This document provides a detailed overview of the Vault Regression Testing Framework, covering its architectural design, implementation strategy, and a step-by-step walkthrough for environment setup and verification.

---

## 1. Solution Outline

### Problem Statement
Manual regression testing of HashiCorp Vault configurations is error-prone and time-consuming. As security policies, authentication methods, and secrets engines evolve, a reliable, automated way to verify that the Vault instance behaves as expected is critical for maintaining a secure infrastructure.

### High-Level Architecture
The solution is built on a modular stack that emphasizes automation, reproducibility, and isolation.

- **Orchestration**: [Go Task](https://taskfile.dev/) (Taskfile.yml) serves as the entry point for all operations.
- **Infrastructure**: [Docker Compose](https://docs.docker.com/compose/) manages a Vault container in **Standard Mode** with a persistent `file` backend.
- **Configuration Management**: [Terraform](https://www.terraform.io/) is the "source of truth" for Vault's internal state (policies, auth methods, and secrets engines).
- **Verification**: [Pytest](https://docs.pytest.org/) with the [hvac](https://github.com/hvac/hvac) library performs assertions against the live Vault API.

---

## 2. Environment Setup

### Prerequisites Verification
Run the following command to check for required tools (`docker`, `terraform`, `task`, `python`, `jq`):
```bash
task prereqs
```

### Virtual Environment
Setup the Python virtual environment to manage dependencies:
```bash
task setup
```

---

## 3. The Automation Pipeline

The framework uses `Taskfile.yml` to orchestrate the entire lifecycle.

### Full Regression Run
To spin up, configure, and run tests in one go:
```bash
task all
```

### Step-by-Step Breakdown

1. **Start Vault**: `task up` starts the container using `configs/vault.hcl`.
2. **Initialize & Unseal**: 
   - `task init`: Generates keys and stores them in `.vault_init.json`.
   - `task unseal`: Makes the Vault operational.
3. **Configure Resources**: `task config` applies Terraform configuration:
   - **KV V2 Secrets Engine** at `secret/`.
   - **AppRole Auth** for machine authentication.
   - **Policies** (admin, read-only).
   - **Audit Devices** for tracking activity.

---

## 4. Verification & Testing

The project uses `pytest` for regression testing, located in the `tests/` directory.

### Running Tests Manually
```bash
task test
```

### Test Coverage
- **System Health**: Verifies initialization, unseal status, and versioning.
- **KV Secrets**: Tests CRUD operations on the V2 engine.
- **AppRole Auth**: Validates login capabilities and policy attachment.
- **Security**: Asserts unauthorized access blocks and audit log status.

---

## 5. Maintenance & Troubleshooting

### Upgrading & Status
- **Upgrade**: `task upgrade` updates the Vault version (defined by `VAULT_VERSION_UPGRADE` in `.env`), recreates the container, unseals it, and runs the regression suite to ensure compatibility.
- **Status**: `task status` provides a quick snapshot of the Vault server's health and seal status.

### Teardown
- **Stop**: `task down` stops the container.
- **Full Clean**: `task clean` removes temporary files and Docker volumes (preserves `.venv`).

### Troubleshooting
- **Vault is sealed**: Run `task unseal`.
- **Terraform errors**: Ensure `VAULT_ADDR` and `VAULT_TOKEN` are set correctly (handled by `task config`).
- **Python errors**: Ensure the virtual environment is used (`task test` handles this).

---

## 6. Future Roadmap
- **HA Mode Testing**: Implementing Consul or Raft for high-availability regression tests.
- **Sentinel/EGP Integration**: Testing Enterprise-grade features.
- **CI Enhancements**: Performance benchmarking in GitHub Actions.