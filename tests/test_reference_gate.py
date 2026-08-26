import pandas as pd

from reconstruction_pipeline.reference_gate import build_final_reference, compute_gate_metrics, evaluate_gate


def fixture_df():
    return pd.DataFrame({
        "candidate_id": [f"x{i}" for i in range(5)],
        "target_year": [2005, 2005, 2015, 2025, 2025],
        "latitude": [9.0, 9.1, 9.2, 9.3, 9.4],
        "longitude": [7.0, 7.1, 7.2, 7.3, 7.4],
        "A1R2N_final_class": [1, 2, 3, 4, 5],
        "A1R2N_human_confidence": ["HIGH"] * 5,
    })


def test_reference_gate_passes_clean_complete_reference():
    df = build_final_reference(fixture_df())
    metrics = compute_gate_metrics(df)
    passed, failures = evaluate_gate(metrics)
    assert passed
    assert failures == []
    assert metrics["resolved"] == 5


def test_reference_gate_rejects_unresolved_class():
    raw = fixture_df()
    raw.loc[0, "A1R2N_final_class"] = pd.NA
    df = build_final_reference(raw)
    metrics = compute_gate_metrics(df)
    passed, failures = evaluate_gate(metrics)
    assert not passed
    assert any("resolved_fraction" in x for x in failures)


def test_reference_gate_rejects_duplicate_candidate_id():
    raw = fixture_df()
    raw.loc[1, "candidate_id"] = raw.loc[0, "candidate_id"]
    df = build_final_reference(raw)
    metrics = compute_gate_metrics(df)
    passed, failures = evaluate_gate(metrics)
    assert not passed
    assert any("duplicate_candidate_ids" in x for x in failures)
