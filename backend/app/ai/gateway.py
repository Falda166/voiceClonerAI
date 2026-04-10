from __future__ import annotations

from pydantic import BaseModel


class InferenceRequest(BaseModel):
    task: str
    payload: dict


class InferenceResponse(BaseModel):
    task: str
    output: dict
    confidence: int
    explainability: dict


class AIGateway:
    def infer(self, req: InferenceRequest) -> InferenceResponse:
        if req.task == 'semantic_label':
            name = req.payload.get('name', 'Device')
            label = name.replace('_', ' ').title()
            return InferenceResponse(
                task=req.task,
                output={'label': label, 'equipment': 'Equipment'},
                confidence=60,
                explainability={'strategy': 'heuristic_title_case'},
            )
        return InferenceResponse(task=req.task, output={'note': 'fallback'}, confidence=30, explainability={'strategy': 'fallback'})
