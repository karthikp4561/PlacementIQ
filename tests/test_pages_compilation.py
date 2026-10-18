import py_compile
from pathlib import Path

def test_compile_all_python_files():
    root = Path(__file__).resolve().parent.parent
    py_files = list(root.glob("*.py")) + list((root / "utils").glob("*.py"))
    assert len(py_files) >= 8

    for py_file in py_files:
        compiled = py_compile.compile(str(py_file), doraise=True)
        assert compiled is not None
