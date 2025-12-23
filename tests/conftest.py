import pytest
import hvac
import json
import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def tf_outputs():
    """Load outputs from Terraform state."""
    terraform_dir = Path(__file__).parent.parent / "terraform"
    env = os.environ.copy()
    if f"{os.getenv('HOME')}/bin" not in env.get("PATH", ""):
        env["PATH"] = f"{env.get('PATH', '')}:{os.getenv('HOME')}/bin"

    try:
        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd=terraform_dir,
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        outputs = json.loads(result.stdout)
        return {key: value.get("value") for key, value in outputs.items()}
    except Exception as e:
        pytest.fail(f"Failed to load Terraform outputs: {e}")


@pytest.fixture(scope="session")
def vault_client():
    """Provide a Vault client using the root token."""
    client = hvac.Client(
        url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
        token=os.getenv("VAULT_TOKEN", "root"),
    )
    if not client.is_authenticated():
        pytest.fail("Vault client not authenticated")
    return client


@pytest.fixture(scope="session")
def approle_client(vault_client, tf_outputs):
    """Client authenticated via AppRole."""
    role_name = tf_outputs["approle_role_name"]
    mount_point = tf_outputs["approle_mount_point"]
    role_id = tf_outputs["approle_role_id"]

    # Generate secret_id
    secret_id_response = vault_client.auth.approle.generate_secret_id(
        role_name=role_name, mount_point=mount_point
    )
    secret_id = secret_id_response["data"]["secret_id"]

    # Create a new client for AppRole login
    client = hvac.Client(url=os.getenv("VAULT_ADDR"))

    # Login
    client.auth.approle.login(
        role_id=role_id, secret_id=secret_id, mount_point=mount_point
    )

    return client
