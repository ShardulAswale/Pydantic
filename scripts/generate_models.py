"""Generate Pydantic V2 models from JSON Schema using datamodel-code-generator.

Run with: python -m scripts.generate_models
"""
from pathlib import Path
import sys

try:
    from datamodel_code_generator import generate
    from datamodel_code_generator.model import PythonVersion
except Exception as exc:  # pragma: no cover
    print("datamodel-code-generator not installed. Did you run 'pip install -e .[dev]'?", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "src" / "car_api" / "models" / "schemas" / "car_schema.json"
OUT = ROOT / "src" / "car_api" / "models" / "car_model.py"

def main() -> None:
    if not SCHEMA.exists():
        raise SystemExit(f"Schema file not found: {SCHEMA}")

    generate(
        input_=str(SCHEMA),
        output=OUT,
        input_file_type="jsonschema",
        target_python_version=PythonVersion.PY_313,
        use_union_operator=True,
        field_constraints=True,
        use_pydantic_v2=True,
        disable_timestamps=True,
    )
    print(f"Generated: {OUT}")

if __name__ == "__main__":
    main()
