"""Upstream Gist mirrors and the provenance that their UPSTREAM.md records."""

from __future__ import annotations

import re

UPSTREAM_MIRRORS = {
    "japanese-tech-writing": "https://gist.github.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d",
    "cognitive-rhythm-writing": "https://gist.github.com/k16shikano/eb2929f13ed19c97188393d297be8432",
}
UPSTREAM_LICENSE_DECLARATION = "https://gist.github.com/k16shikano/67625f2a7d96e3bbdfae8d571a936063"
MIRROR_HASH = re.compile(r"^- SKILL\.md SHA-256: `sha256:([0-9a-f]{64})`$", re.MULTILINE)


def recorded_mirror_hash(provenance: str) -> str | None:
    """Return the SKILL.md SHA-256 recorded in an upstream mirror's UPSTREAM.md."""
    match = MIRROR_HASH.search(provenance)
    return match.group(1) if match else None
