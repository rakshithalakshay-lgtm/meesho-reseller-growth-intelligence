import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
commands = [
    [sys.executable, str(ROOT / "part2_engine" / "test_growth_engine.py")],
    [sys.executable, str(ROOT / "part3_narrative" / "test_masking.py")],
    [sys.executable, str(ROOT / "part4_agent" / "test_mock_agent_runner.py")],
]
for command in commands:
    print("\n$", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)
print("\nALL TESTS PASSED")
