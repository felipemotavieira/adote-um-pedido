from rest_framework.exceptions import APIException


class UserAlreadyHasInstitution(APIException):
    status_code = 400
    default_detail = "An institution is already registered for this user."
    default_code = "cannot_register"
