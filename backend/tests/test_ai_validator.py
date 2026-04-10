import pytest

from app.services.ai.gateway import AIGateway


@pytest.mark.asyncio
async def test_fallback_ai_gateway() -> None:
    gateway = AIGateway('disabled')
    proposal = await gateway.propose_mapping({'uid': 'd1'})
    assert proposal.payload['itemType'] == 'Switch'
    assert proposal.confidence < 0.5
