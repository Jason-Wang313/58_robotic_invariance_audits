# Reproducibility Checklist

1. Run `python run_full_scale_invariance_audit_suite.py`.
2. Verify `results/full_scale/experiment_validation.json` reports:
   - `condition_rows`: 201600
   - `row_count_ok`: true
   - `represented_evaluations`: 105696460800
   - `represented_planning_tick_decisions`: 6764573491200
   - `audit_observer_only_ok`: true
   - `max_abs_success_delta`: 0.0
3. Run `powershell -ExecutionPolicy Bypass -File build_pdf.ps1`.
4. Confirm the canonical artifact is `C:/Users/wangz/Downloads/58.pdf`.
5. Confirm `data/build_status.json` records 25 pages and SHA256 `3F4945B84202530A3EA82E1153C4EDBA464AACD011A919E849F094E8A683266A`.
6. Confirm `paper/main.pdf` is removed after export.
7. Render the Downloads PDF and visually inspect representative pages.

Legacy v2 reproduction remains available through `python v2_measurement_control.py`; it is preserved as a negative control.
