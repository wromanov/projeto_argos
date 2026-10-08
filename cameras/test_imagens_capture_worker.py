from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase


class CaptureWorkerCommandTests(SimpleTestCase):
    @patch("cameras.management.commands.run_capture_worker.run_next_capture", return_value=None)
    def test_once_option_checks_queue_once_without_migrating_database(self, run_next):
        output = StringIO()

        call_command("run_capture_worker", "--once", stdout=output)

        run_next.assert_called_once_with()
        self.assertEqual(output.getvalue(), "")
