
import unittest
try:
    from httplib import OK
except ImportError:
    from http.client import OK
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from piopiy import RestClient

class TestAIAgent(unittest.TestCase):
    def setUp(self):
        self.token = "test_bearer_token"
        self.client = RestClient(token=self.token)

    @patch('piopiy.voice.ai_agent.requests.post')
    def test_init_call(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "call_id": "123"}
        mock_post.return_value = mock_response

        caller_id = "919999999999"
        to_number = "918888888888"
        agent_id = "agent-123"
        
        response = self.client.ai.call(caller_id, to_number, agent_id)

        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['call_id'], '123')
        
        # Verify call args
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['Authorization'], f"Bearer {self.token}")
        self.assertEqual(kwargs['json']['caller_id'], caller_id)
        self.assertEqual(kwargs['json']['agent_id'], agent_id)

    def test_legacy_imports_removed(self):
        """Ensure legacy components are no longer exposed."""
        with self.assertRaises(ImportError):
            from piopiy import Voice
        with self.assertRaises(ImportError):
            from piopiy import Action

    @patch('piopiy.voice.hangup.requests.post')
    def test_hangup_call(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "disconnected"}
        mock_post.return_value = mock_response

        call_id = "call-uuid-123"
        response = self.client.voice.hangup(call_id)

        self.assertEqual(response['status'], 'disconnected')
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['Authorization'], f"Bearer {self.token}")
        self.assertEqual(kwargs['json']['call_id'], call_id)

if __name__ == '__main__':
    unittest.main()
