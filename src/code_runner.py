import re
import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT_SECONDS = 10
MAX_OUTPUT_CHARS = 5000


def extract_code(text):
    blocks = re.findall(r"```(?:python|py)?[ \t]*\n(.*?)```", text, re.DOTALL)
    if not blocks:
        return ""
    return blocks[0].strip()


def run_code(code):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "snippet.py"
        path.write_text(code, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, "-I", "-X", "utf8", str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT_SECONDS,
                cwd=folder,
            )
        except subprocess.TimeoutExpired:
            message = "Execution stopped: it took longer than " + str(TIMEOUT_SECONDS) + " seconds."
            return {"stdout": "", "stderr": message, "returncode": -1}

    return {
        "stdout": result.stdout[:MAX_OUTPUT_CHARS],
        "stderr": result.stderr[:MAX_OUTPUT_CHARS],
        "returncode": result.returncode,
    }