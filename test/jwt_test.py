# -*- coding: utf-8 -*-

import jwt
import datetime
from jwt import exceptions

JWT_SALT = ''

def encode():
    encoded = jwt.encode({'login_user_key': '900bb019-e8a6-4f2e-b806-8bc8081e3ab9'}, JWT_SALT, algorithm="HS512")
    print(encoded)

    parse_token(encoded)

def parse_token(szToken):
    try:
        jwt_options = {
            'verify_signature': False,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }

        verified_payload = jwt.decode(szToken, JWT_SALT, algorithms=["HS512"], options=jwt_options)
        print(verified_payload)
        print("SUCCESS!!!")
    except Exception as ex:
        print(ex)


def main():
    parse_token("eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjkwMGJiMDE5LWU4YTYtNGYyZS1iODA2LThiYzgwODFlM2FiOSJ9.i1p1tQiMKKFmmoUnkIJ7HbTEiHyTwQT2UpK31h1hxJ2N2UomvEgsLC2QueAuMUdT31FklzgiDSiO7NDJJp-lhA")
    encode()

if __name__ == '__main__':
    main()