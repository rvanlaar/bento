from pathlib import Path

from click.testing import CliRunner

import bento.cli
import bento.constants as constants
from _pytest.monkeypatch import MonkeyPatch
from bento import __version__
from bento.cli import cli
from bento.context import Context
from tests.util import strip_ansi

INTEGRATION = Path(__file__).parent.parent / "integration"
SIMPLE = INTEGRATION / "simple"
PY_ONLY = INTEGRATION / "py-only"


def test_version() -> None:
    """Validates that version string is printed"""

    runner = CliRunner()
    context = Context(base_path=SIMPLE)

    result = runner.invoke(cli, ["--version"], obj=context)
    assert result.output.strip() == f"bento/{__version__}"
