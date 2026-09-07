from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "revision_results" / "phase2"
MANIFEST = RESULT / "manifests" / "run_manifest_phase2.json"
CHECKSUM = RESULT / "manifests" / "MANIFEST_PHASE2.sha256"
BUNDLE = ROOT / "GARQ_phase2_handoff_bundle.zip"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    include = [
        *ROOT.glob("revision_exp/methods/*_adapter.py"),
        ROOT / "revision_exp/methods/common_assignment_evaluator.py",
        *ROOT.glob("revision_exp/workflows/*.py"),
        *RESULT.glob("01_size_resolution/*.csv"),
        *RESULT.glob("02_modality/*.csv"),
        *RESULT.glob("07_trimodal/*.csv"),
        *RESULT.glob("08_scalability/*.csv"),
        *RESULT.glob("08_scalability/inference_stability/*/*/*.csv"),
        RESULT / "08_scalability/D16/GARQ/full_seed0_profile_K002_retry2/metacell_size_summary.csv",
        RESULT / "08_scalability/D16/GARQ/full_seed0_profile_K002_retry2/stage_profile.csv",
        RESULT / "08_scalability/D16/GARQ/full_seed0_profile_K002_retry2/per_type_metrics_long.csv",
        *RESULT.glob("audit/*"),
        *RESULT.glob("environments/*"),
        *RESULT.glob("reports/*.md"),
        *ROOT.glob("fig4b/reviewer_mast_quantification/*"),
    ]
    files = sorted({p.resolve() for p in include if p.is_file() and p != MANIFEST})
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    payload = {
        "status": "PARTIAL",
        "branch": "revision/major-review-experiments-phase2",
        "base_commit": "5da45adcd62f1be8ee318d8742c80c59cb242ca2",
        "phase1_commit": "cfaf79bdcbc26840b6cbf67e3531d6fab6540a09",
        "pre_delivery_head": head,
        "matched_requested_k_runs": 48,
        "matched_methods": ["GARQ", "KMeans", "MetaQ", "SEACells"],
        "matched_datasets": ["D5", "D11", "D17", "D18"],
        "seeds": [0, 1, 2],
        "tests": "43 passed, 13 warnings",
        "files": [
            {
                "path": p.relative_to(ROOT).as_posix(),
                "bytes": p.stat().st_size,
                "sha256": digest(p),
            }
            for p in files
        ],
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    CHECKSUM.write_text(
        f"{digest(MANIFEST)}  {MANIFEST.relative_to(ROOT).as_posix()}\n",
        encoding="utf-8",
    )
    bundle_files = files + [MANIFEST, CHECKSUM]
    with zipfile.ZipFile(BUNDLE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in bundle_files:
            archive.write(path, path.relative_to(ROOT).as_posix())
    print({"manifest_entries": len(files), "bundle_bytes": BUNDLE.stat().st_size})


if __name__ == "__main__":
    main()
