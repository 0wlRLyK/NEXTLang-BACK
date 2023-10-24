from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_uid(pk: str) -> str:
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(encoded_pk: str) -> str:
    decoded_bytes = urlsafe_base64_decode(encoded_pk)
    decoded_pk = force_str(decoded_bytes)
    return decoded_pk
