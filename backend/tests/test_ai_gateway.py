from app.ai.gateway import AIGateway, InferenceRequest


def test_ai_gateway_semantic_label() -> None:
    gateway = AIGateway()
    resp = gateway.infer(InferenceRequest(task='semantic_label', payload={'name': 'kitchen_sensor'}))
    assert resp.output['label'] == 'Kitchen Sensor'
    assert resp.confidence > 0
