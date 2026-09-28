import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_caddy_status', REPO / 'scripts/check_caddy_status.py')
status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(status)


class ReleaseTests(unittest.TestCase):
    def test_release_with_supported_build_platforms_triggers_missing_image(self):
        official = {'images': [{'os': 'linux', 'architecture': arch} for arch in ('amd64', 'arm64', 'ppc64le')]}
        outputs = {}
        with patch.object(status, 'get_latest_caddy_release', return_value='v2.11.0'), \
             patch.object(status, 'check_docker_hub_tag', side_effect=[official, None]), \
             patch.object(status, 'set_action_output', side_effect=outputs.__setitem__):
            try:
                status.main()
            except SystemExit:
                pass
        self.assertEqual(outputs['NEEDS_BUILD'], 'true')


if __name__ == '__main__':
    unittest.main()
