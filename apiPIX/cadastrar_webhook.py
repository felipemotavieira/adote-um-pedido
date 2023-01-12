from gerencianet import Gerencianet
from credenciais import CREDENTIALS

gn = Gerencianet(CREDENTIALS)

headers = {
    'x-skip-mtls-checking': 'false'
}

params = {
    'chave': 'd7cf267a-230c-47b0-b4cb-ed6d9a29b5f4'
}

body = {
    'webhookUrl': ''
}

response =  gn.pix_config_webhook(params=params, body=body, headers=headers)
print(response)