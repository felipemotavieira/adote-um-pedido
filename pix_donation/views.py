from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from apiPIX.gerar_cobranca_pix import create_payment_pix
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from rest_framework.response import Response
from pix_donation.models import PixDonation
from pix_donation.serializers import PixDonationSerializer
import ipdb


class PixDonationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = PixDonationSerializer
    queryset = PixDonation.objects.all()

    def create(self, request, *args, **kwargs):
        data = self.request.data
        institution = data.institution

        donor = self.request.user
        value = data.value
        pix_qrcode = create_payment_pix(donor, value)
        image_qrcode = pix_qrcode["imagemQrcode"].replace("data:image/png;base64,", "")

        self.perform_create(data)

        send_mail(
            subject="Doação - AdoteUmPedido",
            message=f"""
                Olá, {donor['first_name']}.
                    Este é o código pix da doação para a instituição {institution['name']}:
                    {pix_qrcode['qrcode']}
                    {image_qrcode}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[donor["email"]],
            fail_silently=False,
        )

        return Response(data={...})
