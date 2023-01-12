import dotenv
import os


dotenv.load_dotenv()

CREDENTIALS = {
    'client_id': os.getenv("CLIENT_ID"),
    'client_secret': os.getenv("CLIENT_SECRET"),
    'sandbox': False,
    'certificate': 'apiPIX/certificado.pem'
}
