"""Total Connect Client."""

import zeep
import logging
import time

from TotalConnectZone import TotalConnectZone

ARM_TYPE_AWAY = 0
ARM_TYPE_STAY = 1
ARM_TYPE_STAY_INSTANT = 2
ARM_TYPE_AWAY_INSTANT = 3
ARM_TYPE_STAY_NIGHT = 4

ZONE_STATUS_NORMAL = 0
ZONE_STATUS_BYPASSED = 1
ZONE_STATUS_FAULT = 2
ZONE_STATUS_TAMPER = 8
ZONE_STATUS_TROUBLE_LOW_BATTERY = 72
ZONE_STATUS_TRIGGERED = 256

ZONE_BYPASS_SUCCESS = 0
GET_ALL_SENSORS_MASK_STATUS_SUCCESS = 0

class AuthenticationError(Exception):
    """Authentication Error class."""
    
    def __init__(self,*args,**kwargs):
        """Initialize."""
        Exception.__init__(self,*args,**kwargs)

class TotalConnectClient:
    """Client for Total Connect."""
    
    DISARMED = 10200
    DISARMED_BYPASS = 10211
    ARMED_AWAY = 10201
    ARMED_AWAY_BYPASS = 10202
    ARMED_AWAY_INSTANT = 10205
    ARMED_AWAY_INSTANT_BYPASS = 10206
    ARMED_CUSTOM_BYPASS = 10223
    ARMED_STAY = 10203
    ARMED_STAY_BYPASS = 10204
    ARMED_STAY_INSTANT = 10209
    ARMED_STAY_INSTANT_BYPASS = 10210
    ARMED_STAY_NIGHT = 10218
    ARMING = 10307
    DISARMING = 10308
    ALARMING = 10207
    ALARMING_FIRE_SMOKE = 10212
    ALARMING_CARBON_MONOXIDE = 10213

    INVALID_SESSION = -102
    SUCCESS = 0
    ARM_SUCCESS = 4500
    DISARM_SUCCESS = 4500
    CONNECTION_ERROR = 4101
    BAD_USER_OR_PASSWORD = -50004

    def __init__(self, username, password, usercode='-1'):
        """Initialize."""
        self.soapClient = zeep.Client('https://rs.alarmnet.com/TC21api/tc2.asmx?WSDL')

        self.applicationId = "14588"
        self.applicationVersion = "1.0.34"
        self.username = username
        self.password = password
        self.usercode = usercode
        self.token = False
        self._panel_meta_data = []
        self._ac_loss = False
        self._low_battery = False
        self._is_cover_tampered = False

        self.locations = []
        self.zones = {}

        self.authenticate()
        self.get_panel_meta_data()

    def authenticate(self):
        """Login to the system."""
        response = self.soapClient.service.LoginAndGetSessionDetails(self.username, self.password, self.applicationId, self.applicationVersion)
        if response.ResultCode == self.SUCCESS:
            logging.info('Login Successful')
            self.token = response.SessionID
            self.populate_details(response)
            return self.SUCCESS
        elif response.ResultCode == self.BAD_USER_OR_PASSWORD:
            raise AuthenticationError('Unable to authenticate with Total Connect. Bad username or password.')
        else:
            raise AuthenticationError('Unable to authenticate with Total Connect. ResultCode: ' +
                                      str(response.ResultCode) + '. ResultData: ' + str(response.ResultData))

    def get_session_details(self):
        """Get Details for the given session."""
        logging.info('Getting session details')

        response = self.soapClient.service.GetSessionDetails(self.token, self.applicationId, self.applicationVersion)

        if response.ResultCode == self.INVALID_SESSION:
            self.authenticate()
            response = self.soapClient.service.GetSessionDetails(self.token, self.applicationId, self.applicationVersion)

        if response.ResultCode != self.SUCCESS:
            Exception('Unable to retrieve session details. ResultCode: ' + str(response.ResultCode) +
                            '. ResultData: ' + str(response.ResultData))

        return response

    def populate_details(self, response):
        """Populate system details."""
        logging.info('Populating locations')

        self.locations = zeep.helpers.serialize_object(response.Locations)['LocationInfoBasic']

    def keep_alive(self):
        """Keep the token alive to avoid server timeouts."""
        logging.info('Initiating Keep Alive')

        response = self.soapClient.service.KeepAlive(self.token)

        if response.ResultCode != self.SUCCESS:
            self.authenticate()

        return response.ResultCode

    def arm_away(self, location_name=False):
        """Arm the system (Away)."""
        self.arm(ARM_TYPE_AWAY, location_name)

    def arm_stay(self, location_name=False):
        """Arm the system (Stay)."""
        self.arm(ARM_TYPE_STAY, location_name)

    def arm_stay_instant(self, location_name=False):
        """Arm the system (Stay - Instant)."""
        self.arm(ARM_TYPE_STAY_INSTANT, location_name)

    def arm_away_instant(self, location_name=False):
        """Arm the system (Away - Instant)."""
        self.arm(ARM_TYPE_AWAY_INSTANT, location_name)

    def arm_stay_night(self, location_name=False):
        """Arm the system (Stay - Night)."""
        self.arm(ARM_TYPE_STAY_NIGHT, location_name)

    def arm(self, arm_type, location_name=False):
        """Arm the system."""
        location = self.get_location_by_location_name(location_name)
        deviceId = self.get_security_panel_device_id(location)

        response = self.soapClient.service.ArmSecuritySystem(self.token, location['LocationID'], deviceId, arm_type, self.usercode)

        if response.ResultCode == self.INVALID_SESSION:
            self.authenticate()
            response = self.soapClient.service.ArmSecuritySystem(self.token, location['LocationID'], deviceId, arm_type, self.usercode)

        logging.info("Arm Result Code:" + str(response.ResultCode))

        if (response.ResultCode == self.ARM_SUCCESS) or (response.ResultCode == self.SUCCESS):
            logging.info('System Armed')
        else:
            raise Exception('Could not arm system. ResultCode: ' + str(response.ResultCode) +
                            '. ResultData: ' + str(response.ResultData))

        return self.SUCCESS

    def get_security_panel_device_id(self, location):
        """Find the device id of the security panel."""
        deviceID = location.get('SecurityDeviceID')

        if deviceID is False:
            raise Exception('No security panel found')

        return deviceID

    def get_location_by_location_name(self, location_name=False):
        """Get the location object for a given name (or the default location if none is provided)."""
        location = False

        for loc in self.locations:
            if location_name is False and location is False:
                location = loc
            elif loc['LocationName'] == location_name:
                location = loc

        if location is False:
            raise Exception('Could not select location. Try using default location.')

        return location

    def get_panel_meta_data(self, location_name=False):
        """Get all meta data about the alarm panel."""
        location = self.get_location_by_location_name(location_name)

        response = self.soapClient.service.GetPanelMetaDataAndFullStatus(self.token, location['LocationID'], 0, 0, 1)

        if response.ResultCode == self.INVALID_SESSION:
            self.authenticate()
            response = self.soapClient.service.GetPanelMetaDataAndFullStatus(self.token, location['LocationID'], 0, 0, 1)

        if response.ResultCode != self.SUCCESS:
            raise Exception('Could not retrieve panel meta data. ResultCode: ' + str(response.ResultCode) +
                            '. ResultData: ' + str(response.ResultData))

        self._panel_meta_data = zeep.helpers.serialize_object(response)

        if self._panel_meta_data is not None:
            self.ac_loss = self._panel_meta_data['PanelMetadataAndStatus'].get('IsInACLoss')
            self.low_battery = self._panel_meta_data['PanelMetadataAndStatus'].get('IsInLowBattery')
            self.is_cover_tampered = self._panel_meta_data['PanelMetadataAndStatus'].get('IsCoverTampered')

            zones = self._panel_meta_data['PanelMetadataAndStatus'].get('Zones')
            if zones is not None:
                zone_info = zones.get('ZoneInfo')
                if zone_info is not None:
                    self.zones.clear()
                    for zone in zone_info:
                        if zone is not None:
                            self.zones[zone.get('ZoneID')] = TotalConnectZone(zone)               

        else:
            self.ac_loss = None
            self.low_battery = None
            self.is_cover_tampered = None
            self.zones = {}

        return response

    @property
    def ac_loss(self):
        """Get status of AC Loss."""
        return self._ac_loss

    @ac_loss.setter
    def ac_loss(self, new_state):
        """Set state of AC Loss flag."""
        if new_state == 'False' or new_state == False:
            self._ac_loss = False
        else:
            self._ac_loss = True

    @property
    def low_battery(self):
        """Get status of low battery."""
        return self._low_battery

    @low_battery.setter
    def low_battery(self, new_state):
        """Set state of Low Battery flag."""
        if new_state == 'False' or new_state == False:
            self._low_battery = False
        else:
            self._low_battery = True

    @property
    def is_cover_tampered(self):
        """Get status of cover tamper."""
        return self._is_cover_tampered

    @is_cover_tampered.setter
    def is_cover_tampered(self, new_state):
        """Set state of IsCoverTampered flag."""
        if new_state == 'False' or new_state == False:
            self._is_cover_tampered = False
        else:
            self._is_cover_tampered = True

    def zone_status(self, location_id, zone_id):
        """Get status of a zone."""
        z = self.zones.get(zone_id)
        if z is None:
            logging.error('Zone {} does not exist.'.format(zone_id))
            return None

        return z.status

    def connect_to_panel(self, location_name=False, attempts=3):
        """Connect to the panel."""
        location = False
        location = self.get_location_by_location_name(location_name)
        deviceId = self.get_security_panel_device_id(location)
        attempt =  0
        while ( attempt < attempts ):
            response = self.soapClient.service.ConnectToPanel(self.token, location['LocationID'], deviceId )
            if response.ResultCode != self.SUCCESS:
                attempt += 1
                logging.error('Could not connect to panel, retrying ' + str(attempt) + '/' + str(attempts) + '.')
                time.sleep(3)
            else:
                break
        return response

    def get_armed_status(self, location_name=False):
        """Get the status of the panel."""
        self.get_panel_meta_data(location_name)

        alarm_code = self._panel_meta_data['PanelMetadataAndStatus']['Partitions']['PartitionInfo'][0]['ArmingState']

        return alarm_code

    def is_armed(self, location_name=False):
        """Return True or False if the system is armed in any way."""
        alarm_code = self.get_armed_status(location_name)

        if alarm_code == self.ARMED_AWAY:
            return True
        elif alarm_code == self.ARMED_AWAY_BYPASS:
            return True
        elif alarm_code == self.ARMED_AWAY_INSTANT:
            return True
        elif alarm_code == self.ARMED_AWAY_INSTANT_BYPASS:
            return True
        elif alarm_code == self.ARMED_STAY:
            return True
        elif alarm_code == self.ARMED_STAY_BYPASS:
            return True
        elif alarm_code == self.ARMED_STAY_INSTANT:
            return True
        elif alarm_code == self.ARMED_STAY_INSTANT_BYPASS:
            return True
        elif alarm_code == self.ARMED_STAY_NIGHT:
            return True
        elif alarm_code == self.ARMED_CUSTOM_BYPASS:
            return True
        else:
            return False

    def is_arming(self, location_name=False):
        """Return true or false is the system is in the process of arming."""
        alarm_code = self.get_armed_status(location_name)

        if alarm_code == self.ARMING:
            return True
        else:
            return False

    def is_disarming(self, location_name=False):
        """Return true or false is the system is in the process of disarming."""
        alarm_code = self.get_armed_status(location_name)

        if alarm_code == self.DISARMING:
            return True
        else:
            return False

    def is_pending(self, location_name=False):
        """Return true or false is the system is pending an action."""
        alarm_code = self.get_armed_status(location_name)

        if alarm_code == self.ARMING or alarm_code == self.DISARMING:
            return True
        else:
            return False

    def disarm(self, location_name=False):
        """Disarm the system."""
        location = self.get_location_by_location_name(location_name)
        deviceId = self.get_security_panel_device_id(location)

        response = self.soapClient.service.DisarmSecuritySystem(self.token, location['LocationID'], deviceId, self.usercode)

        if response.ResultCode == self.INVALID_SESSION:
            self.authenticate()
            response = self.soapClient.service.DisarmSecuritySystem(self.token, location['LocationID'], deviceId, self.usercode)

        logging.info("Disarm Result Code:" + str(response.ResultCode))

        if (response.ResultCode == self.DISARM_SUCCESS) or (response.ResultCode == self.SUCCESS):
            logging.info('System Disarmed')
        else:
            raise Exception('Could not disarm system. ResultCode: ' + str(response.ResultCode) +
                            '. ResultData: ' + str(response.ResultData))

        return self.SUCCESS

    def zoneBypass(self, zoneID, location_name=False):
        """Bypass a zone."""
        location = self.get_location_by_location_name(location_name)
        deviceId = self.get_security_panel_device_id(location)

        response = self.soapClient.service.Bypass(self.token, location['LocationID'], deviceId, zoneID, self.usercode)

        if response.ResultCode == self.INVALID_SESSION:
            self.authenticate()
            response = self.soapClient.service.Bypass(self.token, location['LocationID'], deviceId, zoneID, self.usercode)

        logging.info("Bypass Result Code:" + str(response.ResultCode))

        if response.ResultCode == ZONE_BYPASS_SUCCESS:
            logging.info('Zone ' + str(zoneID) + ' bypassed.')
        else:
            raise Exception('Could not bypass zone. ResultCode: ' + str(response.ResultCode) +
                            '. ResultData: ' + str(response.ResultData))

        return self.SUCCESS
