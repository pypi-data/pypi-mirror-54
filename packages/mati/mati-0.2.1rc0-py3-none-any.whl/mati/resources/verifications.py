from dataclasses import dataclass
from typing import ClassVar, List

from .base import Resource
from ..types import VerificationDocument


@dataclass
class Verification(Resource):
    _endpoint: ClassVar[str] = '/api/v1/verifications'
    _token_score: ClassVar[str] = 'identity'

    id: str
    expired: bool
    steps: list
    documents: List[VerificationDocument]
    hasProblem: bool
    computed: dict
    metadata: dict

    @classmethod
    def retrieve(cls, verification_id: str) -> 'Verification':
        endpoint = f'{cls._endpoint}/{verification_id}'
        resp = cls._client.get(endpoint, token_score=cls._token_score)
        docs = []
        for doc in resp['documents']:
            docs.append(VerificationDocument(**doc))
        resp['documents'] = docs
        return cls(**resp)
