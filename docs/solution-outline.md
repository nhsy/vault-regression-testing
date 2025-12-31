# Vault Regression Testing Framework - Comprehensive Guide

This document provides a detailed overview of the Vault Regression Testing Framework, covering its architectural design, implementation strategy, and a step-by-step walkthrough for environment setup and verification.

---

## 1. Solution Outline

### Problem Statement

Manual regression testing of HashiCorp Vault configurations is error-prone and time-consuming. As security policies, authentication methods, and secrets engines evolve, a reliable, automated way to verify that the Vault instance behaves as expected is critical for maintaining a secure infrastructure.

### High-Level Architecture

The solution is built on a modular stack that emphasizes automation, reproducibility, and isolation.

- **Orchestration**: [Go Task](https://taskfile.dev/) (Taskfile.yml) serves as the entry point for all operations.
- **Infrastructure**: [Docker Compose](https://docs.docker.com/compose/) manages a Vault container in **Standard Mode** with a persistent `file` backend, a **PostgreSQL** container for database secrets testing, and an **OpenLDAP** container for identity testing.
- **Configuration Management**: [Terraform](https://www.terraform.io/) is the "source of truth" for Vault's internal state (policies, auth methods, and secrets engines).
- **Verification**: [Pytest](https://docs.pytest.org/) with the [hvac](https://github.com/hvac/hvac) library performs assertions against the live Vault API.

![Architecture Diagram](diagram.png)

---

## 2. Environment Setup

### Prerequisites Verification

Run the following command to check for required tools (`docker`, `terraform`, `task`, `python`, `uv`, `jq`):

```bash
task prereqs
```

### Virtual Environment

Setup the Python virtual environment using `uv`, install dependencies, and create `.env` from template:

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

1. **Start Infrastructure**: `task up` starts Vault, PostgreSQL, and OpenLDAP containers and waits for readiness.
2. **Initialize Services**: `task init` performs consolidated initialization:
   - Seeds LDAP server with sample users and groups.
   - Generates Vault keys and stores them in `.vault_init.json`.
   - Unseals Vault to make it operational.
3. **Configure Resources**: `task terraform:apply` applies Terraform configuration:
   - **KV V2 Secrets Engine** at `secret/`.
   - **PKI Secrets Engine** for certificate generation.
   - **AppRole Auth** for machine authentication.
   - **OIDC/JWT Auth** for GitHub Actions integration.
   - **LDAP Auth** with Identity Group mapping.
   - **LDAP Secrets Engine** for static/dynamic credentials.
   - **Database Secrets Engine** with PostgreSQL connection and dynamic roles.
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
- **PKI Secrets**:
  - Validates certificate generation against configured roles.
  - Verifies certificate fields (CN, issuer, private key).
- **AppRole Auth**: Validates login capabilities and policy attachment.
- **OIDC Integration**:
  - Verifies GitHub Actions OIDC login (skipped locally).
  - Validates `repository` claim binding to specific GitHub repositories.
  - Verifies authenticated access to KV secrets (`test-12345`).
- **Database Secrets**:
  - Generates dynamic PostgreSQL credentials (readonly and readwrite roles).
  - Verifies database connectivity with generated credentials.
  - Tests credential revocation and TTL limits.
  - Validates proper role permissions and isolation.
- **LDAP Integration**:
  - Authenticates as LDAP users (`alice`, `bob`).
  - Verifies policy assignment via Identity Groups.
  - Rotates static LDAP credentials.
  - Generates dynamic LDAP credentials.
- **Security**: Asserts unauthorized access blocks and audit log status.

---

## 5. Maintenance & Troubleshooting

### Upgrading & Status

- **Upgrade**: `task vault:upgrade` updates the Vault version (defined by `VAULT_VERSION_UPGRADE` in `.env`), recreates the container, unseals it, and runs the regression suite to ensure compatibility.
- **Status**: `task vault:status` provides a quick snapshot of the Vault server's health and seal status.

### Teardown

- **Stop**: `task down` stops the container.
- **Full Clean**: `task clean` removes temporary files and Docker volumes (preserves `.venv`).

### Troubleshooting

- **Vault is sealed**: Run `task vault:unseal`.
- **Terraform errors**: Ensure `VAULT_ADDR` and `VAULT_TOKEN` are set correctly (handled by `task terraform:apply`).
- **Python errors**: Ensure the virtual environment is used (`task test` handles this).

---

## 6. Future Roadmap

- **CI Enhancements**: Performance benchmarking in GitHub Actions.
- **HA Mode Testing**: Implementing Consul or Raft for high-availability regression tests.
