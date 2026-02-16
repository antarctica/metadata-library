from jwskate import Jwk

from bas_metadata_library.standards.magic_administration.v1.utils import AdministrationKeys


def make_keys() -> None:
    """
    Generate new test keys.

    Note: This should not be needed again but is retained to allow keys to be rotated.
    """
    signing_key_private = Jwk.generate(alg="ES256", kid="bas_metadata_testing_signing_key")
    signing_key_public = signing_key_private.public_jwk()
    encryption_key_private = Jwk.generate(alg="ECDH-ES+A128KW", crv="P-256", kid="bas_metadata_testing_encryption_key")
    keys = [
        ("Signing Key (private)", signing_key_private),
        ("Signing Key (public)", signing_key_public),
        ("Encryption Key", encryption_key_private),
    ]

    print("New testing keys generated:")
    for _ in keys:
        label, jwk = _
        print(f"\n# {label}\n")
        print(jwk.to_json(indent=2))
        print("Env safe value:")
        print(jwk.to_json(compact=True).replace('"', '\\"'))


def load_keys() -> AdministrationKeys:
    """
    Load keys from static values.

    These test keys are not secret and so not sensitive.
    """
    SIGNING_KEY_PUBLIC = {  # noqa: N806
        "kty": "EC",
        "kid": "bas_metadata_testing_signing_key",
        "alg": "ES256",
        "crv": "P-256",
        "x": "FzxBM1ZPO5W2bYlhT9AjZUKz5_oH5vIh4_k4aEZ64rM",
        "y": "vmK5PWOoIA9eO0ntLh37AMpVODyj0NWf842FwoN-GRs",
    }
    SIGNING_KEY_PRVIATE = {  # noqa: N806
        "kty": "EC",
        "crv": "P-256",
        "x": "FzxBM1ZPO5W2bYlhT9AjZUKz5_oH5vIh4_k4aEZ64rM",
        "y": "vmK5PWOoIA9eO0ntLh37AMpVODyj0NWf842FwoN-GRs",
        "d": "FdxFSRF2zAAfn7_GaDk81T8PdBGlzZpRtxd10-kc4PE",
        "alg": "ES256",
        "kid": "bas_metadata_testing_signing_key",
    }
    ENCRYPTION_KEY_PRVIATE = {  # noqa: N806
        "kty": "EC",
        "crv": "P-256",
        "x": "kYiwq6MW8lGN6PB2csVMuMRcISVk5eNUpGkjM-mm8QY",
        "y": "raOTT2xAQhHFKhPHy338L8Ql0hvgsDtHwtEc8pCOf2Q",
        "d": "2lBuUtJK2TcV_b4B-bDCPnRVAqMnYvnLZ41IUguprs8",
        "alg": "ECDH-ES+A128KW",
        "kid": "bas_metadata_testing_encryption_key",
    }

    keys = AdministrationKeys(
        signing_public=Jwk(SIGNING_KEY_PUBLIC),
        signing_private=Jwk(SIGNING_KEY_PRVIATE),
        encryption_private=Jwk(ENCRYPTION_KEY_PRVIATE),
    )

    if keys.encryption_private.kid != "bas_metadata_testing_encryption_key":
        msg = "Incorrect encryption key loaded."
        raise ValueError(msg) from None
    if keys.signing_private.kid != "bas_metadata_testing_signing_key":
        msg = "Incorrect signing key loaded."
        raise ValueError(msg) from None

    return keys


def main() -> None:
    """Entrypoint."""
    make_keys()


if __name__ == "__main__":
    main()
