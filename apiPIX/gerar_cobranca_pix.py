from gerencianet import Gerencianet
from .credenciais import CREDENTIALS
import base64
import asyncio


gn = Gerencianet(CREDENTIALS)


async def create_payment_pix(donor, value):
    # body = {
    #     'calendario': {
    #         'expiracao': 3600
    #     },
    #     'devedor': {
    #         'cpf': '05203711275',
    #         'nome': 'Lívia Oliveira'
    #     },
    #     'valor': {
    #         'original': '0.01'
    #     },
    #     'chave': 'd7cf267a-230c-47b0-b4cb-ed6d9a29b5f4',
    #     'solicitacaoPagador': 'Cobrança dos serviços prestados.'
    # }

    body = {
        'calendario': {
            'expiracao': 3600
        },
        'devedor': {
            'cpf': donor.cpf,
            'nome': donor.first_name,
        },
        'valor': {
            'original': value,
        },
        'chave': 'd7cf267a-230c-47b0-b4cb-ed6d9a29b5f4',
        'solicitacaoPagador': 'Doação Pix'
    }

    response = gn.pix_create_immediate_charge(body=body)
    print(response)

    params = {
        'id': response['loc']['id']
    }

    response = gn.pix_generate_QRCode(params=params)
    print(response)

    # #Generate QRCode Image
    # if('imagemQrcode' in response):
    #     with open("qrCodeImage.png", "wb") as fh:
    #         fh.write(base64.b64decode(response['imagemQrcode'].replace('data:image/png;base64,', '')))

    return response
# asyncio.run(create_payment_pix())
