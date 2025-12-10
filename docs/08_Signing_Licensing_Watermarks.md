# Signing, Licensing & Watermarks

Dexes are often valuable IP. The schema allows optional protection features:

- `dex_signature` – cryptographic signature (e.g. ed25519)
- `dex_license` – embedded license terms, licensee, expiration
- `dex_watermark` – non-cryptographic leak tracing

StashKit itself does **not** enforce legal terms. It simply exposes:

- whether a Dex is signed
- whether the signature verifies
- any embedded license metadata

Your application decides whether to:

- load unsigned Dexes
- reject expired licenses
- warn on invalid signatures
