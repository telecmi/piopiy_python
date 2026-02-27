import unittest
from unittest.mock import MagicMock, patch

from piopiy import PipelineBuilder, PiopiyAPIError, PiopiyValidationError, RestClient


VALID_UUID = "bdd32bcb-767c-40a5-be4a-5f45eeb348a6"
CALL_UUID = "c4d0e5f6-a7b8-12c9-d3e4-f56789012345"
ORG_UUID = "f89dd77d-c226-4ff2-b88c-6d7e4f5a88e2"
FLOW_UUID = "7f4d89c7-3485-45c5-9016-f45a47cd885c"


def _mock_response(status_code, payload):
    response = MagicMock()
    response.status_code = status_code
    response.content = b"x"
    response.json.return_value = payload
    response.text = ""
    return response


class TestPiopiySDK(unittest.TestCase):
    def setUp(self):
        self.client = RestClient(token="test_bearer_token")

    @patch("piopiy.voice.http.requests.Session.post")
    def test_ai_call(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "call_queued"})

        response = self.client.ai.call(
            caller_id="919999999999",
            to_number="918888888888",
            agent_id=VALID_UUID,
            options={"record": True, "max_duration_sec": 600, "ring_timeout_sec": 40},
            variables={"customer": "alice", "is_vip": True, "score": 90},
        )

        self.assertEqual(response["message"], "call_queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/ai/call"))
        self.assertEqual(kwargs["json"]["agent_id"], VALID_UUID)

    @patch("piopiy.voice.http.requests.Session.post")
    def test_ai_call_with_failover_routes_to_pcmo(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "call_queued"})

        failover_agent_uuid = "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2"
        response = self.client.ai.call(
            caller_id="919999999999",
            to_number="918888888888",
            agent_id=VALID_UUID,
            app_id="app_1",
            failover={
                "agent_id": failover_agent_uuid,
                "strategy": "sequential",
                "ring_timeout_sec": 20,
            },
            options={"record": True},
        )

        self.assertEqual(response["message"], "call_queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/call"))

        payload = kwargs["json"]
        self.assertEqual(payload["app_id"], "app_1")
        self.assertEqual(payload["pipeline"][0]["action"], "connect")
        self.assertEqual(payload["pipeline"][0]["endpoints"][0]["id"], VALID_UUID)
        self.assertEqual(payload["pipeline"][0]["endpoints"][1]["id"], failover_agent_uuid)
        self.assertEqual(payload["pipeline"][0]["params"]["strategy"], "sequential")

    @patch("piopiy.voice.http.requests.Session.post")
    def test_hangup(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        response = self.client.voice.hangup(call_id=CALL_UUID, cause="NORMAL_CLEARING", reason="done")

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/call/hangup"))
        self.assertEqual(kwargs["json"]["call_id"], CALL_UUID)

    @patch("piopiy.voice.http.requests.Session.post")
    def test_ai_hangup_alias(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        response = self.client.ai.hangup(call_id=CALL_UUID, cause="NORMAL_CLEARING", reason="done")

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/call/hangup"))
        self.assertEqual(kwargs["json"]["call_id"], CALL_UUID)

    @patch("piopiy.voice.http.requests.Session.post")
    def test_pcmo_call(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "call_queued"})

        pipeline = [
            {
                "action": "connect",
                "params": {"caller_id": "919999999999"},
                "endpoints": [{"type": "pstn", "number": "918888888888"}],
            }
        ]

        response = self.client.pcmo.call(
            caller_id="919999999999",
            to_number="918888888888",
            app_id="app_1",
            pipeline=pipeline,
            options={"record": True, "ring_timeout_sec": 45, "max_duration_sec": 900},
            variables={"route": "sales"},
        )

        self.assertEqual(response["message"], "call_queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/call"))
        self.assertEqual(kwargs["json"]["pipeline"], pipeline)

    @patch("piopiy.voice.http.requests.Session.post")
    def test_voice_direct_call(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "call_queued"})

        response = self.client.voice.call(
            caller_id="919999999999",
            to_number="918888888888",
            app_id="app_1",
            call_options={"record": True, "ring_timeout_sec": 45, "max_duration_sec": 900},
            variables={"route": "direct"},
            connect={
                "strategy": "sequential",
                "options": {"ring_timeout_sec": 20, "machine_detection": True},
                "metadata": {"campaign": "normal_call"},
            },
        )

        self.assertEqual(response["message"], "call_queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/call"))

        payload = kwargs["json"]
        self.assertEqual(payload["caller_id"], "919999999999")
        self.assertEqual(payload["to_number"], "918888888888")
        self.assertEqual(payload["app_id"], "app_1")
        self.assertEqual(payload["pipeline"][0]["action"], "connect")
        self.assertEqual(payload["pipeline"][0]["endpoints"][0]["type"], "pstn")
        self.assertEqual(payload["pipeline"][0]["endpoints"][0]["number"], "918888888888")
        self.assertEqual(payload["pipeline"][0]["params"]["strategy"], "sequential")

    @patch("piopiy.voice.http.requests.Session.post")
    def test_voice_direct_call_legacy_args_backward_compatible(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "call_queued"})

        response = self.client.voice.call(
            caller_id="919999999999",
            to_number="918888888888",
            app_id="app_1",
            options={"record": True},
            strategy="sequential",
            connect_options={"ring_timeout_sec": 20},
            metadata={"campaign": "normal_call"},
        )

        self.assertEqual(response["message"], "call_queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/call"))
        self.assertEqual(kwargs["json"]["pipeline"][0]["params"]["strategy"], "sequential")

    def test_voice_direct_call_rejects_conflicting_call_options(self):
        with self.assertRaises(PiopiyValidationError):
            self.client.voice.call(
                caller_id="919999999999",
                to_number="918888888888",
                app_id="app_1",
                call_options={"record": True},
                options={"record": True},
            )

    def test_voice_direct_call_rejects_conflicting_connect_args(self):
        with self.assertRaises(PiopiyValidationError):
            self.client.voice.call(
                caller_id="919999999999",
                to_number="918888888888",
                app_id="app_1",
                connect={"strategy": "sequential"},
                strategy="sequential",
            )

    @patch("piopiy.voice.http.requests.Session.post")
    def test_voice_transfer_alias(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        response = self.client.voice.transfer(
            call_id=CALL_UUID,
            pipeline=[{"action": "hangup"}],
        )

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/transfer"))
        self.assertEqual(kwargs["json"]["call_id"], CALL_UUID)

    @patch("piopiy.voice.http.requests.Session.post")
    def test_voice_transfer_pipeline_builder(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        response = self.client.voice.transfer(
            call_id=CALL_UUID,
            pipeline=self.client.voice.pipeline().play("https://example.com/a.wav").hangup(),
        )

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/transfer"))
        self.assertEqual(kwargs["json"]["pipeline"][0]["action"], "play")
        self.assertEqual(kwargs["json"]["pipeline"][1]["action"], "hangup")

    @patch("piopiy.voice.http.requests.Session.post")
    def test_pcmo_transfer(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        response = self.client.pcmo.transfer(call_id=CALL_UUID, pipeline=[{"action": "hangup"}])

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/transfer"))
        self.assertEqual(kwargs["json"]["call_id"], CALL_UUID)

    @patch("piopiy.voice.http.requests.Session.post")
    def test_ai_transfer_alias(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        response = self.client.ai.transfer(call_id=CALL_UUID, pipeline=[{"action": "hangup"}])

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/transfer"))
        self.assertEqual(kwargs["json"]["call_id"], CALL_UUID)

    @patch("piopiy.voice.http.requests.Session.post")
    def test_ai_transfer_internal_builder(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        failover_agent_uuid = "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2"
        pipeline_builder = (
            PipelineBuilder()
            .play("https://example.com/transfer.wav")
            .connect(
                params={"caller_id": "919999999999", "strategy": "sequential", "options": {"ring_timeout_sec": 20}},
                endpoints=[
                    {"type": "agent", "id": VALID_UUID},
                    {"type": "agent", "id": failover_agent_uuid},
                ],
            )
            .hangup()
        )

        response = self.client.ai.transfer(
            call_id=CALL_UUID,
            pipeline=pipeline_builder,
        )

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/transfer"))

        pipeline = kwargs["json"]["pipeline"]
        self.assertEqual(pipeline[0]["action"], "play")
        self.assertEqual(pipeline[1]["action"], "connect")
        self.assertEqual(pipeline[1]["params"]["caller_id"], "919999999999")
        self.assertEqual(pipeline[1]["endpoints"][0]["id"], VALID_UUID)
        self.assertEqual(pipeline[1]["endpoints"][1]["id"], failover_agent_uuid)
        self.assertEqual(pipeline[2]["action"], "hangup")

    @patch("piopiy.voice.http.requests.Session.post")
    def test_flow_call(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "call_queued"})

        response = self.client.flow.call(
            flow_id=FLOW_UUID,
            org_id=ORG_UUID,
            caller_id="919999999999",
            to_number="918888888888",
            app_id="app_1",
            options={"record": True},
        )

        self.assertEqual(response["message"], "call_queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/flow/call"))
        self.assertEqual(kwargs["json"]["org_id"], ORG_UUID)

    def test_validation_error(self):
        with self.assertRaises(PiopiyValidationError):
            self.client.ai.call(
                caller_id="invalid",
                to_number="918888888888",
                agent_id=VALID_UUID,
            )

    def test_failover_requires_app_id(self):
        with self.assertRaises(PiopiyValidationError):
            self.client.ai.call(
                caller_id="919999999999",
                to_number="918888888888",
                agent_id=VALID_UUID,
                failover={"agent_id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2"},
            )

    def test_failover_agent_id_rejects_array(self):
        with self.assertRaises(PiopiyValidationError):
            self.client.ai.call(
                caller_id="919999999999",
                to_number="918888888888",
                agent_id=VALID_UUID,
                app_id="app_1",
                failover={
                    "agent_id": [
                        "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2",
                        "3090913e-ce1f-4f41-a357-5e7598ef2f0c",
                    ]
                },
            )

    def test_pipeline_validation_error(self):
        with self.assertRaises(PiopiyValidationError):
            self.client.pcmo.transfer(
                call_id=CALL_UUID,
                pipeline=[{"action": "invalid_action"}],
            )

    @patch("piopiy.voice.http.requests.Session.post")
    def test_ai_pipeline_factory(self, mock_post):
        mock_post.return_value = _mock_response(200, {"message": "queued"})

        response = self.client.ai.transfer(
            call_id=CALL_UUID,
            pipeline=self.client.ai.pipeline().hangup(),
        )

        self.assertEqual(response["message"], "queued")
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/voice/pcmo/transfer"))
        self.assertEqual(kwargs["json"]["pipeline"][0]["action"], "hangup")

    @patch("piopiy.voice.http.requests.Session.post")
    def test_api_error_mapping(self, mock_post):
        mock_post.return_value = _mock_response(403, {"error": "app_not_active"})

        with self.assertRaises(PiopiyAPIError) as err:
            self.client.ai.call(
                caller_id="919999999999",
                to_number="918888888888",
                agent_id=VALID_UUID,
            )

        self.assertEqual(err.exception.status_code, 403)
        self.assertEqual(err.exception.payload.get("error"), "app_not_active")

    def test_pipeline_builder(self):
        pipeline = (
            PipelineBuilder()
            .play("https://example.com/a.wav")
            .hangup()
            .build()
        )

        self.assertEqual(len(pipeline), 2)
        self.assertEqual(pipeline[0]["action"], "play")
        self.assertEqual(pipeline[1]["action"], "hangup")

    def test_legacy_imports_removed(self):
        with self.assertRaises(ImportError):
            from piopiy import Voice  # noqa: F401

        with self.assertRaises(ImportError):
            from piopiy import Action  # noqa: F401

    def test_piopiy_voice_alias_import(self):
        from piopiy_voice import RestClient as VoiceRestClient

        alias_client = VoiceRestClient(token="test_bearer_token")
        self.assertIsNotNone(alias_client.ai)


if __name__ == "__main__":
    unittest.main()
