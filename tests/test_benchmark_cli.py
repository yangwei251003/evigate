import json
import subprocess
import sys

from evigate.benchmark_io import write_new_json


def test_validate_benchmark_manifest_refuses_existing_output(tmp_path):
    output = tmp_path / "score.json"
    output.write_text("{}", encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps({"run_id": "RUN-001", "output_path": str(output)}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "evigate.cli",
            "validate-benchmark-manifest",
            str(manifest),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "BENCHMARK-OUTPUT-EXISTS" in result.stdout


def test_write_new_json_never_overwrites_existing_file(tmp_path):
    path = tmp_path / "existing.json"
    path.write_text('{"preserve": true}', encoding="utf-8")

    try:
        write_new_json(path, {"replace": True})
    except FileExistsError:
        pass
    else:
        raise AssertionError("Existing formal artifact was overwritten")

    assert json.loads(path.read_text(encoding="utf-8")) == {"preserve": True}
