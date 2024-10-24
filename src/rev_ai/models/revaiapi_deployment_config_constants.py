from enum import Enum

class RevAiApiDeployment(Enum):
    US = 'US'
    EU = 'EU'

RevAiApiDeploymentConfigMap = {
    RevAiApiDeployment.US: { 'base_url': 'https://api.rev.ai', 'base_websocket_url': 'wss://api.rev.ai' },
    RevAiApiDeployment.EU: { 'base_url': 'https://ec1.api.rev.ai', 'base_websocket_url': 'wss://ec1.api.rev.ai' }
}
