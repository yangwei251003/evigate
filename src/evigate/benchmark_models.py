"""Stable, serializable records for the EviGate benchmark."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BenchmarkIssue:
    """One deterministic benchmark validation diagnostic."""

    code: str
    message: str


def to_dict(value: BenchmarkIssue) -> dict[str, str]:
    """Serialize a diagnostic without exposing implementation details."""

    return asdict(value)
