from gerencianet import Gerencianet
from credenciais import CREDENTIALS
import base64

gn = Gerencianet(CREDENTIALS)

body = {
    'calendario': {
        'expiracao': 3600
    },
    'devedor': {
        'cpf': '05203711275',
        'nome': 'Lívia Oliveira'
    },
    'valor': {
        'original': '0.01'
    },
    'chave': 'd7cf267a-230c-47b0-b4cb-ed6d9a29b5f4',
    'solicitacaoPagador': 'Cobrança dos serviços prestados.'
}

response =  gn.pix_create_immediate_charge(body=body)

params = {
    'id': response['loc']['id']
}

response =  gn.pix_generate_QRCode(params=params)
print(response)

#Generate QRCode Image
if('imagemQrcode' in response):
    with open("qrCodeImage.png", "wb") as fh:
        fh.write(base64.b64decode(response['imagemQrcode'].replace('data:image/png;base64,', '')))