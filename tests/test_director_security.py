import io
import sys
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

import director


class DirectorCliSecurityTests(unittest.TestCase):
    def test_cli_redacts_configuration_errors(self):
        secret = "director-cli-secret"
        output = io.StringIO()
        with patch.object(director, "load_config", side_effect=RuntimeError(f"provider token={secret}")), patch(
            "sys.argv", ["director.py", "auditar el proyecto"]
        ), redirect_stderr(output):
            result = director.main()
        self.assertEqual(result, 1)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("token=[REDACTED]", output.getvalue())


if __name__ == "__main__":
    unittest.main()
