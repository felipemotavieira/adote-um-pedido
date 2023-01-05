from rest_framework.exceptions import APIException


class InstitutionDoesNotExist(APIException):
    status_code = 400
    default_detail = "You don't have an institution yet. Create your institution first and then create the address"
    default_code = "service_unavailable"
