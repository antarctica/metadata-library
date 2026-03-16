import json
from typing import Optional

from jwskate import JweCompact, Jwk, JwtSigner

from bas_metadata_library.standards.magic_administration.v1 import AdministrationMetadata


class AdministrationMetadataSubjectMismatchError(Exception):
    """Raised when administration metadata does not relate to discovery metadata for the same resource."""

    pass


class AdministrationMetadataIntegrityError(Exception):
    """Raised when administration metadata ID does not match the subject of a JWT."""

    pass


class AdministrationKeys:
    """Encryption and signing keys for administration metadata."""

    def __init__(
        self, encryption_private: Jwk, signing_public: Optional[Jwk] = None, signing_private: Optional[Jwk] = None
    ) -> None:
        """One of the public or private signing key is needed depending on whether metadata needs verification and/or signing."""
        self.encryption_private: Jwk = encryption_private
        self.signing_private: Optional[Jwk] = signing_private

        if isinstance(signing_public, Jwk):
            self.signing_public: Jwk = signing_public
            return
        if isinstance(signing_private, Jwk):
            self.signing_public: Jwk = signing_private.public_jwk()
            return

        msg = "Public or private signing_key must be provided."
        raise TypeError(msg) from None

    def __getstate__(self) -> dict[str, str]:
        """
        Support pickling by dumping keys to JSON.

        Crytography keys within JWKs cannot be pickled.
        """
        out = {"encryption_private": self.encryption_private.to_json(), "signing_public": self.signing_public.to_json()}
        if self.signing_private:
            out["signing_private"] = self.signing_private.to_json()
        return out

    def __setstate__(self, state: dict[str, str]) -> None:
        """Load keys from JSON when unpickling."""
        self.encryption_private = Jwk.from_json(state["encryption_private"])
        self.signing_public = Jwk.from_json(state["signing_public"])
        try:
            self.signing_private = Jwk.from_json(state["signing_private"])
        except KeyError:
            self.signing_private = None

    def __eq__(self, other: object) -> bool:
        """Check equality."""
        if not isinstance(other, AdministrationKeys):
            return NotImplemented
        return (
            self.encryption_private == other.encryption_private
            and self.signing_public == other.signing_public
            and self.signing_private == other.signing_private
        )


class AdministrationWrapper:
    """
    Wrapper for encrypting/decrypting and signing/verifying Administration Metadata.

    Administration metadata is signed and encrypted as a JWT within a JWE using compact serialization.

    The JWT provides integrity protection via signing with an asymmetric key (allowing applications to verify metadata
    without being able to modify it). The JWE wrapper provides confidentiality via encryption with a symmetric key.

    Administration metadata is included in the JWT using a custom 'pyd' (payload) claim.

    This class checks the metadata ID corresponds to the JWT subject (internal integrity). It does not check admin
    metadata relates to discovery metadata.
    """

    _issuer = "magic.data.bas.ac.uk"
    _audience = "data.bas.ac.uk"
    _lifetime = 3_153_600_000  # 100 years
    _enc_alg = "A256GCM"

    def __init__(self, keys: AdministrationKeys) -> None:
        self._keys = keys

    def encode(self, metadata: AdministrationMetadata) -> str:
        """
        Sign and encrypt metadata.

        The JWT is signed using the private signing key (for anyone to then verify).
        The JWE is encrypted using the public encryption key (for only us to read).
        """
        if self._keys.signing_private is None:
            msg = "Private signing key is required for writing metadata."
            raise ValueError(msg) from None
        signer = JwtSigner(issuer=self._issuer, key=self._keys.signing_private, default_lifetime=self._lifetime)
        token: JweCompact = signer.sign(
            subject=metadata.id, audience=self._audience, extra_claims={"pyd": metadata.dumps_json()}
        ).encrypt(key=self._keys.encryption_private.public_jwk(), enc=self._enc_alg)
        return str(token)

    def decode(self, encrypted_metadata: str) -> AdministrationMetadata:
        """Decrypt and verify metadata."""
        token = JweCompact(encrypted_metadata)
        trusted_token = token.decrypt_jwt(self._keys.encryption_private)
        trusted_token.validate(key=self._keys.signing_public, issuer=self._issuer, audience=self._audience)
        value = AdministrationMetadata.loads_json(trusted_token.claims["pyd"])
        if trusted_token.subject != value.id:
            raise AdministrationMetadataIntegrityError() from None
        return value


def get_admin(keys: AdministrationKeys, config: dict) -> Optional[AdministrationMetadata]:
    """

    Get administration metadata for record if available.

    Checks loaded administration metadata relates to parent discovery metadata record via resource (file) identifier.
    """
    try:
        kv = get_kv(config)
    except ValueError:
        return None
    raw_value: Optional[str] = kv.get("admin_metadata", None)
    if raw_value is None:
        return None

    loader = AdministrationWrapper(keys)
    value = loader.decode(raw_value)
    if value.id != config.get("file_identifier"):
        raise AdministrationMetadataSubjectMismatchError() from None
    return value


def set_admin(keys: AdministrationKeys, config: dict, admin_meta: AdministrationMetadata) -> None:
    """Set administration metadata for record."""
    if admin_meta.id != config.get("file_identifier"):
        raise AdministrationMetadataSubjectMismatchError() from None
    wrapper = AdministrationWrapper(keys=keys)
    element = wrapper.encode(admin_meta)
    set_kv(kv={"admin_metadata": element}, config=config)


def get_kv(config: dict) -> dict:
    """Get key-value pairs from a JSON encoded string if used in record supplemental information."""
    if (
        "supplemental_information" not in config["identification"]
        or not config["identification"]["supplemental_information"]
    ):
        return {}
    try:
        kv = json.loads(config["identification"]["supplemental_information"])
    except json.JSONDecodeError:
        msg = "Supplemental information isn't JSON parsable."
        raise ValueError(msg) from None
    if not isinstance(kv, dict):
        msg = "Supplemental information isn't parsed as a dict."
        raise TypeError(msg) from None
    return kv


def set_kv(kv: dict, config: dict, replace: bool = False) -> None:
    """
    Set key-value pairs in a JSON encoded string for use in record supplemental information.

    Use `replace` to remove existing keys and replace with new value.

    Wraps any existing non-JSON encoded value as a 'statement' key.

    If new value is empty, removes element rather than setting an empty value.
    """
    try:
        kv_ = get_kv(config)
    except ValueError:
        kv_ = {"statement": config["identification"]["supplemental_information"]}
    kv_.update(kv)
    if replace:
        kv_ = kv

    config["identification"]["supplemental_information"] = json.dumps(kv_)
    if len(kv_) == 0:
        del config["identification"]["supplemental_information"]
