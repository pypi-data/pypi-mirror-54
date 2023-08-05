import hashlib
import json
import time
import asyncio
import functools
from aiohttp import web
from datetime import datetime, timedelta
from pathlib import Path
from werkzeug.wrappers import Request, Response


class AsyncFakeCloudServer:
    """ a fake server to act as the HMIP cloud"""

    # region __init__ & helper functions
    def __init__(self, home_path=Path(__file__).parent.joinpath("json_data/home.json")):
        with open(home_path, encoding="utf-8") as file:
            self.data = json.load(file, encoding="UTF-8")
            self.sgtin = "3014F711A000000BAD0C0DED"
            self.client_auth_token = (
                hashlib.sha512(str(self.sgtin + "jiLpVitHvWnIGD1yo7MA").encode("utf-8"))
                .hexdigest()
                .upper()
            )

            self.client_token_map = {
                "00000000-0000-0000-0000-000000000000": "8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE"
            }

            self.pin = None

            self.client_auth_waiting = None  # used in auth
            self.home_id = "00000000-0000-0000-0000-000000000001"
            self.ws = None

    def __del__(self):
        if self.ws:
            self.ws.close()  # pragma: no cover

    async def __call__(self, request):
        response = Response()
        methodname = "{}{}".format(
            request.method.lower(), request.path.replace("/", "_")
        )
        if request.method.lower() == "post":
            request.data = await request.content.read()

        response.content_type = "application/json"
        try:
            response = await self.call_method(methodname, request, response)
        except NameError as e:
            response.status_code = 404
            response.data = json.dumps({"errorCode": str(e)})
        except TypeError as e:
            response = await self.call_method(methodname, request)
        if isinstance(response, Response):  # Workaround until all methods are converted
            res = web.Response(
                body=(response.data),
                status=response.status_code,
                headers=response.headers,
            )
            return res
        elif isinstance(response, web.StreamResponse):
            return response

    async def call_method(self, func_name, *args, **kwargs):
        if func_name[0] == "_":
            raise NameError("Can't call internal function {}".format(func_name))

        def func_not_found(*args, **kwargs):  # just in case we dont have the function
            raise NameError("Can't find method {}".format(func_name))

        func = getattr(self, func_name, func_not_found)
        return await func(*args, **kwargs)

    def validate_authorization(func):
        @functools.wraps(func)
        async def func_wrapper(self, request: Request, response: Response):
            try:
                if request.headers["CLIENTAUTH"] == self.client_auth_token:
                    for v in self.client_token_map.values():
                        if v == request.headers["AUTHTOKEN"]:
                            return await func(self, request, response)
            except:
                pass

            return self.errorCode("INVALID_AUTHORIZATION", 403)

        return func_wrapper

    def errorCode(self, message, status_code):
        return web.json_response({"errorCode": message}, status=status_code)

    # endregion

    # region home

    @validate_authorization
    async def post_hmip_home_getOAuthOTK(self, request: Request, response: Response):
        response.data = json.dumps(
            {"authToken": "C001ED", "expirationTimestamp": 1545568701680}
        )
        return response

    @validate_authorization
    async def post_hmip_home_getCurrentState(
        self, request: Request, response: Response
    ):
        response.data = json.dumps(self.data)
        return response

    @validate_authorization
    async def post_hmip_home_setLocation(self, request: Request, response: Response):

        js = json.loads(request.data)

        self.data["home"]["location"]["city"] = js["city"]
        self.data["home"]["location"]["latitude"] = js["latitude"]
        self.data["home"]["location"]["longitude"] = js["longitude"]

        return response

    @validate_authorization
    async def post_hmip_home_setPin(self, request: Request, response: Response):
        js = json.loads(request.data)

        if self.pin:
            if request.headers.get("PIN", None) != str(self.pin):
                response = self.errorCode("INVALID_PIN", 403)
                return response

        self.pin = js["pin"]
        if self.pin == "":
            self.pin = None
        return response

    async def post_hmip_home_getPin(self, request: Request, response: Response):
        js = {"pin": self.pin}
        response.data = json.dumps(js)
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_home_setTimezone(self, request: Request, response: Response):
        js = json.loads(request.data)
        self.data["home"]["timeZoneId"] = js["timezoneId"]
        return response

    @validate_authorization
    async def post_hmip_home_setPowerMeterUnitPrice(
        self, request: Request, response: Response
    ):
        js = json.loads(request.data)
        self.data["home"]["powerMeterUnitPrice"] = js["powerMeterUnitPrice"]
        return response

    # endregion

    # region home/security
    @validate_authorization
    async def post_hmip_home_security_setZonesActivation(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)

        external = js["zonesActivation"]["EXTERNAL"]
        internal = js["zonesActivation"]["INTERNAL"]

        for g_id in self.data["groups"]:
            g = self.data["groups"][g_id]
            if g["type"] == "SECURITY_ZONE":
                if g["label"] == "INTERNAL":
                    g["active"] = internal
                elif g["label"] == "EXTERNAL":
                    g["active"] = external

        return response

    @validate_authorization
    async def post_hmip_home_security_setIntrusionAlertThroughSmokeDetectors(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)

        activate = js["intrusionAlertThroughSmokeDetectors"]

        self.data["home"]["functionalHomes"]["SECURITY_AND_ALARM"][
            "intrusionAlertThroughSmokeDetectors"
        ] = activate

        return response

    @validate_authorization
    async def post_hmip_home_security_setZoneActivationDelay(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)

        delay = js["zoneActivationDelay"]

        self.data["home"]["functionalHomes"]["SECURITY_AND_ALARM"][
            "zoneActivationDelay"
        ] = delay

        return response

    @validate_authorization
    async def post_hmip_home_security_getSecurityJournal(
        self, request: Request, response: Response
    ):
        with open(
            Path(__file__).parent.joinpath("json_data/security_journal.json"),
            encoding="utf-8",
        ) as file:
            js = json.load(file, encoding="UTF-8")
            # going through json load + dumps. Maybe we have to alter the data in the future
            response.data = json.dumps(js)
            return response

    # endregion

    # region home/heating
    @validate_authorization
    async def post_hmip_home_heating_activateAbsenceWithDuration(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)

        minutes = js["duration"]
        absence_end = datetime.now() + timedelta(minutes=minutes)
        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"][
            "absenceEndTime"
        ] = absence_end.strftime("%Y_%m_%d %H:%M")
        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"]["absenceType"] = "PERIOD"

        return response

    @validate_authorization
    async def post_hmip_home_heating_activateAbsenceWithPeriod(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)

        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"]["absenceEndTime"] = js[
            "endTime"
        ]
        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"]["absenceType"] = "PERIOD"

        return response

    @validate_authorization
    async def post_hmip_home_heating_deactivateAbsence(
        self, request: Request, response: Response
    ):

        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"]["absenceEndTime"] = None
        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"][
            "absenceType"
        ] = "NOT_ABSENT"

        return response

    @validate_authorization
    async def post_hmip_home_heating_activateVacation(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)

        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"]["absenceEndTime"] = js[
            "endTime"
        ]
        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"][
            "absenceType"
        ] = "VACATION"

        return response

    @validate_authorization
    async def post_hmip_home_heating_deactivateVacation(
        self, request: Request, response: Response
    ):

        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"]["absenceEndTime"] = None
        self.data["home"]["functionalHomes"]["INDOOR_CLIMATE"][
            "absenceType"
        ] = "NOT_ABSENT"

        return response

    # endregion

    # region rule
    @validate_authorization
    async def post_hmip_rule_enableSimpleRule(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            rule = self.data["home"]["ruleMetaDatas"][js["ruleId"]]
            rule["active"] = js["enabled"]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_RULE", 404)
        return response

    @validate_authorization
    async def post_hmip_rule_setRuleLabel(self, request: Request, response: Response):

        js = json.loads(request.data)
        try:
            rule = self.data["home"]["ruleMetaDatas"][js["ruleId"]]
            rule["label"] = js["label"]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_RULE", 404)
        return response

    # endregion

    # region device

    @validate_authorization
    async def post_hmip_device_setDeviceLabel(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            d["label"] = js["label"]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setRouterModuleEnabled(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["routerModuleEnabled"] = js[
                "routerModuleEnabled"
            ]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_deleteDevice(self, request: Request, response: Response):

        js = json.loads(request.data)
        if js["deviceId"] in self.data["devices"]:
            self.data["devices"].pop(js["deviceId"])
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAcousticAlarmTiming(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["acousticAlarmTiming"] = js[
                "acousticAlarmTiming"
            ]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAcousticAlarmSignal(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["acousticAlarmSignal"] = js[
                "acousticAlarmSignal"
            ]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setInAppWaterAlarmTrigger(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["inAppWaterAlarmTrigger"] = js[
                "inAppWaterAlarmTrigger"
            ]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAcousticWaterAlarmTrigger(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["acousticWaterAlarmTrigger"] = js[
                "acousticWaterAlarmTrigger"
            ]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setSirenWaterAlarmTrigger(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["sirenWaterAlarmTrigger"] = js[
                "sirenWaterAlarmTrigger"
            ]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setClimateControlDisplay(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["display"] = js["display"]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setOperationLock(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["operationLockActive"] = js[
                "operationLock"
            ]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_control_resetEnergyCounter(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["energyCounter"] = 0
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_control_setSwitchState(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["on"] = js["on"]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_control_setDimLevel(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        try:
            d = self.data["devices"][js["deviceId"]]
            channelIndex = "{}".format(js["channelIndex"])
            d["functionalChannels"][channelIndex]["dimLevel"] = js["dimLevel"]
            response.status_code = 200
        except:
            response = self.errorCode("INVALID_DEVICE", 404)
        return response

    @validate_authorization
    async def post_hmip_device_control_setShutterLevel(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["shutterLevel"] = js["shutterLevel"]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_control_setSlatsLevel(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["shutterLevel"] = js["shutterLevel"]
        d["functionalChannels"][channelIndex]["slatsLevel"] = js["slatsLevel"]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_control_stop(self, request: Request, response: Response):
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_control_setSimpleRGBColorDimLevel(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["dimLevel"] = js["dimLevel"]
        d["functionalChannels"][channelIndex]["simpleRGBColorState"] = js[
            "simpleRGBColorState"
        ]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_control_setSimpleRGBColorDimLevelWithTime(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["dimLevel"] = js["dimLevel"]
        d["functionalChannels"][channelIndex]["simpleRGBColorState"] = js[
            "simpleRGBColorState"
        ]
        # not sure what to do with onTime and rampTime :/
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setNotificationSoundType(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        notificationSoundTypeKey = (
            "notificationSoundTypeHighToLow"
            if js["isHighToLow"]
            else "notificationSoundTypeLowToHigh"
        )
        d["functionalChannels"][channelIndex][notificationSoundTypeKey] = js[
            "notificationSoundType"
        ]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAccelerationSensorEventFilterPeriod(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex][
            "accelerationSensorEventFilterPeriod"
        ] = js["accelerationSensorEventFilterPeriod"]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAccelerationSensorTriggerAngle(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["accelerationSensorTriggerAngle"] = js[
            "accelerationSensorTriggerAngle"
        ]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAccelerationSensorSensitivity(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["accelerationSensorSensitivity"] = js[
            "accelerationSensorSensitivity"
        ]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAccelerationSensorNeutralPosition(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["accelerationSensorNeutralPosition"] = js[
            "accelerationSensorNeutralPosition"
        ]
        response.status_code = 200
        return response

    @validate_authorization
    async def post_hmip_device_configuration_setAccelerationSensorMode(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        d = self.data["devices"][js["deviceId"]]
        channelIndex = "{}".format(js["channelIndex"])
        d["functionalChannels"][channelIndex]["accelerationSensorMode"] = js[
            "accelerationSensorMode"
        ]
        response.status_code = 200
        return response

    # endregion

    # region auth
    # there is no 100% secure auth code here -> its a fake server...who cares =)

    async def post_hmip_auth_connectionRequest(
        self, request: Request, response: Response
    ):
        if request.headers["CLIENTAUTH"] != self.client_auth_token:
            response = self.errorCode("INVALID_AUTH_TOKEN", 403)  # pragma: no cover
        elif self.client_auth_waiting is not None:
            response = self.errorCode("AUTH_IN_PROCESS", 403)  # pragma: no cover
        else:
            pin = request.headers.get("PIN", None)
            if pin != self.pin:
                response = self.errorCode("INVALID_PIN", 403)  # pragma: no cover
            else:
                js = json.loads(request.data)
                # TODO: add sgtin check
                self.client_auth_waiting = js
                response.status_code = 200
        return response

    async def post_hmip_auth_isRequestAcknowledged(
        self, request: Request, response: Response
    ):
        if request.headers["CLIENTAUTH"] != self.client_auth_token:
            response = self.errorCode("INVALID_AUTH_TOKEN", 403)  # pragma: no cover
        else:
            js = json.loads(request.data)
            c_id = js["deviceId"]
            for c in self.data["clients"]:
                if c == c_id:
                    response = self.errorCode("", 200)
                    return response
        response = self.errorCode("INVALID_AUTH_CHALLANGE", 403)
        return response

    async def post_hmip_auth_simulateBlueButton(
        self, request: Request, response: Response
    ):
        client = {
            "homeId": self.home_id,
            "id": self.client_auth_waiting["deviceId"],
            "label": self.client_auth_waiting["deviceName"],
            "clientType": "APP",
        }
        self.data["clients"][self.client_auth_waiting["deviceId"]] = client
        self.client_auth_waiting = None
        return response

    async def post_hmip_auth_requestAuthToken(
        self, request: Request, response: Response
    ):
        if request.headers["CLIENTAUTH"] != self.client_auth_token:
            response = self.errorCode("INVALID_AUTH_TOKEN", 403)  # pragma: no cover
        else:
            js = json.loads(request.data)
            c_id = js["deviceId"]
            token = hashlib.sha512(c_id.encode("utf-8")).hexdigest().upper()
            self.client_token_map[c_id] = token
            response.data = json.dumps({"authToken": token})
            response.status_code = 200

        return response

    async def post_hmip_auth_confirmAuthToken(
        self, request: Request, response: Response
    ):
        if request.headers["CLIENTAUTH"] != self.client_auth_token:
            response = self.errorCode("INVALID_AUTH_TOKEN", 403)  # pragma: no cover
        else:
            js = json.loads(request.data)
            c_id = js["deviceId"]
            token = js["authToken"]
            if self.client_token_map[c_id] == token:
                response.data = json.dumps({"clientId": c_id})
                response.status_code = 200
            else:
                response = self.errorCode("INVALID_AUTH_TOKEN", 403)  # pragma: no cover
        return response

    # endregion

    # region Group
    @validate_authorization
    async def post_hmip_group_deleteGroup(self, request: Request, response: Response):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            self.data["groups"].pop(js["groupId"])
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_setGroupLabel(self, request: Request, response: Response):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["label"] = js["label"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_switching_setState(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["on"] = js["on"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_switching_setShutterLevel(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["shutterLevel"] = js["shutterLevel"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_heating_setSetPointTemperature(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["setPointTemperature"] = js["setPointTemperature"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_heating_setBoost(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["boostMode"] = js["boost"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_heating_setBoostDuration(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["boostDuration"] = js["boostDuration"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_heating_setActiveProfile(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["activeProfile"] = "PROFILE_{}".format(int(js["profileIndex"]) + 1)
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_heating_setControlMode(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["controlMode"] = js["controlMode"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_switching_alarm_testSignalAcoustic(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            assert js["signalAcoustic"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_switching_alarm_setSignalAcoustic(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["signalAcoustic"] = js["signalAcoustic"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_switching_alarm_testSignalOptical(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            assert js["signalOptical"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    @validate_authorization
    async def post_hmip_group_switching_alarm_setSignalOptical(
        self, request: Request, response: Response
    ):

        js = json.loads(request.data)
        if js["groupId"] in self.data["groups"]:
            g = self.data["groups"][js["groupId"]]
            g["signalOptical"] = js["signalOptical"]
            response.status_code = 200
        else:
            response = self.errorCode("INVALID_GROUP", 404)
        return response

    # endregion

    async def post_getHost(self, request: Request, response: Response):
        ws_url = self.url.replace("https", "wss")
        data = {"urlREST": self.url, "urlWebSocket": f"{ws_url}/ws", "apiVersion": "12"}
        return web.json_response(data)

    # region Fake Server settings
    async def post_hmip_fake_timeout(self, request: Request, response: Response):
        """this function forces a timeout on the request (2 seconds)"""
        time.sleep(2)
        response.data = json.dumps({"TIMEOUT": "TIMEOUT"})
        return response

    async def post_hmip_fake_loadConfig(self, request: Request, response: Response):
        js = json.loads(request.data)
        with open(Path(__file__).parent.joinpath("json_data", js["file"])) as file:
            self.data = json.load(file, encoding="UTF-8")
        return response

    # endregion

    # region websocket
    async def get_ws(self, request):
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(request)
        async for msg in self.ws:
            if msg.tp == web.WSMsgType.CLOSE:  # pragma: no cover
                await msg.close()

        return self.ws

    async def post_hmip_ws_send(self, request):
        """ this function will send specific data to the websocket """
        await self.ws.send_json(json.loads(request.data))
        return web.Response()

    async def post_hmip_ws_sleep(self, request):
        """ this function will send specific data to the websocket """
        js = json.loads(request.data)
        # the server thread must be blocked here to simulate a timeout for the client
        # NO AWAIT VERSION!
        time.sleep(js["seconds"])
        return web.Response()

    # endregion
