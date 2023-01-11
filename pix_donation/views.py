from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from apiPIX.gerar_cobranca_pix import create_payment_pix
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from rest_framework.response import Response
from pix_donation.models import PixDonation
from pix_donation.serializers import PixDonationSerializer
from institutions.models import Institution
import asyncio
import ipdb


class PixDonationView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = PixDonationSerializer
    queryset = PixDonation.objects.all()

    def create(self, request, *args, **kwargs):
        data = self.request.data
        institution = Institution.objects.filter(id=data["donee_institution"])[0]
        # ipdb.set_trace()

        donor = self.request.user
        value = data["value"]
        pix_qrcode = asyncio.run(create_payment_pix(donor, value))
        # image_qrcode = pix_qrcode["imagemQrcode"].replace("data:image/png;base64,", "")

        # ipdb.set_trace()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # serializer.save(donee_institution=institution, user=donor)
        serializer.save()
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)

        send_mail(
            subject="Doação - AdoteUmPedido",
            message=f"""
                Olá, {donor.first_name}.
                    Este é o código pix da doação para a instituição {institution.name}:
                    {pix_qrcode['qrcode']}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[donor.email],
            fail_silently=False,
        )

        response = {
            "data": data,
            "qr_code": pix_qrcode['qrcode']
        }

        return Response(data=response)
