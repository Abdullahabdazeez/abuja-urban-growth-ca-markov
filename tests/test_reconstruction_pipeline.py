import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

MODULE = Path(__file__).parents[1] / 'reconstruction' / 'full_automation_pipeline.py'
spec = importlib.util.spec_from_file_location('pipeline', MODULE)
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)


def test_reference_gate_excludes_unresolved_and_uses_human():
    rows = []
    for year in [2005, 2015, 2025]:
        for cid in [1,2,3,4,5]:
            for i in range(2):
                rows.append({'target_year': year, 'human_label': cid})
    rows.append({'target_year': 2005, 'human_label': np.nan, 'A1R2N_final_class': 2, 'A1R2N_final_resolution': 'MANUAL_REQUIRED'})
    df = pd.DataFrame(rows)
    out, result = pipeline.build_reference_gate(df, pipeline.GateThresholds(min_reference_per_class_year=2))
    assert result.passed
    assert out['reference_usable'].sum() == 30
    assert (~out['reference_usable']).sum() == 1


def test_classification_gate_passes_strong_predictions():
    y = [1,2,3,4,5] * 20
    result = pipeline.classification_gate(y, y, pipeline.GateThresholds())
    assert result.passed
    assert result.metrics['oa'] == 1.0


def test_transition_gate_rejects_low_built_persistence():
    a = np.array([1]*100 + [2]*100 + [3]*100 + [4]*100 + [5]*100)
    b = np.array([1]*70 + [2]*30 + [2]*100 + [3]*100 + [4]*100 + [5]*100)
    result = pipeline.temporal_transition_gate(a, b, pipeline.GateThresholds())
    assert not result.passed
    assert any('built_persistence' in x for x in result.failures)


def test_hindcast_gate_passes_exact_change():
    obs = np.array([0,1,0,1,1,0], dtype=bool)
    result = pipeline.hindcast_gate(obs, obs.copy(), pipeline.GateThresholds())
    assert result.passed
    assert result.metrics['fom'] == 1.0
