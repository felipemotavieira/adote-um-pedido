from rest_framework.exceptions import APIException


class SolicitationAlreadyReceived(APIException):
    status_code = 400
    default_detail = "Solicitation already received. There are no more possible updates."
    default_code = "service_unavailable"
    