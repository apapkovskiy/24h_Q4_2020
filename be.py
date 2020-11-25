import requests
import json
from enum import Enum
import config

# import boto3
# from botocore.config import Config

# iot_client = boto3.client('iot')

# iot = boto3.client(
#     "iot",
#     config=Config(
#         retries={
#             'max_attempts': 7,
#             'mode': 'standard'
#         }
#     )
# )

# iot_data = boto3.client(
#     "iot-data",
#     config=Config(
#         retries={
#             'max_attempts': 7,
#             'mode': 'standard'
#         }
#     )
# )


class AssetType(Enum):
    """AssetType class represents the possible values of an asset can get."""

    PGCONNECT_ANDROID_APP = "PGCONNECT_ANDROID_APP"
    TRADE_FAIR_DEMO_APP = "TRADE_FAIR_DEMO_APP"
    INSIGHT_MOBILE_APP = "INSIGHT_MOBILE_APP"
    MARK_FIRMWARE = "MARK_FIRMWARE"
    GATEWAY1_APPLICATION = "GATEWAY1_APPLICATION_FIRMWARE"
    INSIGHT_MOBILE_IOS_SDK = "INSIGHT_MOBILE_IOS_SDK"


class InsightBE():
    def __init__(self):
        self.auth_token = self.auth_token()

    def get_gateway_info(self, gw: str):

        end_point = "{}/{}/gateways/{}".format(
            config.BASE_URL, config.CUSTOMER_ID, gw)
        resp = requests.get(url=end_point, headers=self.get_headers())
        
        assert resp.status_code == 200
        assert resp.ok
        assert resp.headers["content-type"] == "application/json"

        resp_body = json.loads(resp.text)

        return resp_body

    def update_gw_config(self, gw: str, url: str):
        request = {
            "mark_fw": "",
            "gateway_fw": "",
            "gateway_config": url
        }

        end_point = "{}/{}/gateways/{}".format(
            config.BASE_URL, config.CUSTOMER_ID, gw)
        resp = requests.post(url=end_point, headers=self.post_headers(
        ), data=json.dumps(request),)

        assert resp.status_code == 200
        assert resp.ok
        assert resp.headers["content-type"] == "application/json"

        resp_body = json.loads(resp.text)
        return resp_body

    def update_mark_be(self, gw: str, url: str):
        request = {
            "mark_fw": url,
            "gateway_fw": "",
            "gateway_config": ""
        }

        end_point = "{}/{}/gateways/{}".format(
            config.BASE_URL, config.CUSTOMER_ID, gw)
        resp = requests.post(url=end_point, headers=self.post_headers(
        ), data=json.dumps(request),)

        assert resp.status_code == 200
        assert resp.ok
        assert resp.headers["content-type"] == "application/json"

        resp_body = json.loads(resp.text)
        return resp_body
    
    def update_mark(self, gw: str, url: str):
        iot_data.update_thing_shadow(
            thingName=gw,
            payload=json.dumps(
                {
                    "state": {
                        "desired": {
                            "mark_fw": url,
                            "gateway_fw": "",
                            "gateway_config": ""
                        }
                    }
                }
            ),
        )

    def update_gw_be(self, gw: str, url: str):
        request = {
            "gateway_fw": url,
            "mark_fw": ""
        }

        end_point = "{}/{}/gateways/{}".format(
            config.BASE_URL, config.CUSTOMER_ID, gw)
        resp = requests.post(url=end_point, headers=self.post_headers(
        ), data=json.dumps(request),)

        assert resp.status_code == 200
        assert resp.ok
        assert resp.headers["content-type"] == "application/json"

        resp_body = json.loads(resp.text)
        return resp_body
    
    def update_gw(self, gw: str, url: str):
        iot_data.update_thing_shadow(
            thingName=gw,
            payload=json.dumps(
                {
                    "state": {
                        "desired": {
                            "gateway_fw": url,
                            "mark_fw": ""                        }
                    }
                }
            ),
        )

    def get_url(self, asset: AssetType, version: str):
        request = {
            "eula_version": "1.0.0",
            "eula_checksum": "FDABC1234",
            "agreed_by": "test@test.com",
            "asset_type": asset.value,
            "asset_version": version
        }

        end_point = "{}/{}/generate-download-url".format(
            config.BASE_URL, config.CUSTOMER_ID)
        resp = requests.post(url=end_point, headers=self.post_headers(
        ), data=json.dumps(request),)

        assert resp.status_code == 200
        assert resp.ok
        assert resp.headers["content-type"] == "application/json"

        resp_body = json.loads(resp.text)
        return resp_body["asset_download_url"]

    def get_headers(self):
        headers = {
            "Authorization": self.auth_token,
        }
        return headers

    def post_headers(self):
        headers = {
            "Authorization": self.auth_token,
            "Content-Type": "application/json",
        }
        return headers

    @staticmethod
    def auth_token():
        # Additional headers.
        headers = {
            "Content-Type": "application/x-amz-json-1.1",
            "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
        }

        # Body
        payload = {
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": config.COGNITO_CLIENT_ID,
            "AuthParameters": {
                "USERNAME": config.AUTH_USERNAME,
                "PASSWORD": config.AUTH_PASSWORD,
            },
        }

        # convert dict to json by json.dumps() for body data.
        resp = requests.post(
            config.AUTH_URL, headers=headers, data=json.dumps(payload))

        # Validate response headers and body contents, e.g. status code.
        assert resp.status_code == 200
        resp_body = resp.json()

        # access_token = resp_body["AuthenticationResult"]["AccessToken"]
        id_token = resp_body["AuthenticationResult"]["IdToken"]

        return id_token

