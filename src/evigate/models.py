"""Stable, serializable model types used by EviGate validators."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Issue:
    """A deterministic validation finding."""

    code: str
    message: str
