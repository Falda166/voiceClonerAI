from dataclasses import dataclass


@dataclass
class AIProposal:
    task: str
    payload: dict
    confidence: float
    explanation: str


class AIGateway:
    def __init__(self, mode: str) -> None:
        self.mode = mode

    async def propose_mapping(self, device: dict) -> AIProposal:
        if self.mode == 'disabled':
            return AIProposal(
                task='mapping',
                payload={'itemType': 'Switch', 'semanticTags': ['Control']},
                confidence=0.45,
                explanation='Heuristic fallback used because AI mode is disabled.',
            )
        return AIProposal(
            task='mapping',
            payload={'itemType': 'Switch', 'semanticTags': ['Light', 'Switchable']},
            confidence=0.76,
            explanation='Model classified device as switchable light endpoint.',
        )
