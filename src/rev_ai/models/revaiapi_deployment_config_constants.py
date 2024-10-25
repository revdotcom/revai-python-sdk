from enum import Enum
from typing import Dict, TypedDict


class RevAiApiDeployment(Enum):
    """
    Enum representing the deployment regions for Rev AI API.

    Attributes:
        US: Represents the United States deployment.
        EU: Represents the European Union deployment.
    """
    US = 'US'
    EU = 'EU'


class RevAiApiConfig(TypedDict):
    """
    TypedDict representing the configuration for a Rev AI API deployment.

    Attributes:
        base_url: The base URL for API requests.
        base_websocket_url: The base URL for WebSocket connections.
    """
    base_url: str
    base_websocket_url: str


# Dictionary mapping RevAiApiDeployment enum values to their respective configuration settings.
RevAiApiDeploymentConfigMap: Dict[RevAiApiDeployment, RevAiApiConfig] = {
    RevAiApiDeployment.US: {
        'base_url': 'https://api.rev.ai',
        'base_websocket_url': 'wss://api.rev.ai'
    },
    RevAiApiDeployment.EU: {
        'base_url': 'https://ec1.api.rev.ai',
        'base_websocket_url': 'wss://ec1.api.rev.ai'
    }
}
