# snmp simple plugin
#
# Author: Gerardvs
#
"""
<plugin key="Tonq" name="Simple snmp reader plugin" author="gerardvs" version="0.1.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="http://github.com/seventer/tonq">
    <params>
        <param field="Address" label="Server IP" width="200px" required="true" default="192.168.14.100"/>
        <param field="Mode1" label="Community" width="200px" required="true" default="public"/>
        <param field="Mode2" label="OID" width="200px" required="true" default="iso.3.6.1.4.1.6574.2.1.1.6.0"/>
        <param field="Mode3" label="Domoticz TypeName" width="200px">
            <options>
                <option label="Custom" value="Custom"/>
                <option label="Text" value="Text"/>
                <option label="Temperature" value="Temperature"  default="true" />
            </options>
        </param>
        <param field="Mode4" label="Emulate" width="75px">
            <options>
                <option label="True" value="Emulate"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
        <param field="Mode5" label="interval minutes" width="75px" required="true" default="5"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""


import Domoticz
from tonq import Tonq
from datetime import datetime, timedelta

lastUpdate = datetime.now()


def onStart():
    global lastUpdate
    if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            Domoticz.Debug("onStart called")
            DumpConfigToLog()
    lastUpdate = datetime.now()
    CreateSensor()
    #DumpSettingsToLog()
    UpdateSensor()
    Domoticz.Heartbeat(30)
    return True


def onStop():
    Domoticz.Debug("onStop called")
    return True

def onConnect(Status, Description):
    Domoticz.Debug("onConnect called:")
    return True

def onMessage(Data, Status, Extra):
    Domoticz.Debug("onMessage called")
    return True

def onCommand(Unit, Command, Level, Hue):
    Domoticz.Debug("onCommand called")
    return True

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    Domoticz.Debug("onNotification called")
    return True

def onDisconnect():
    Domoticz.Debug("onDisconnect called")
    return True

def onHeartbeat():
    Domoticz.Debug("onHeartbeat called")
    interval = int(Parameters["Mode5"])
    if isActionTime(interval):
       UpdateSensor()



# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device Idx:      '" + str(Devices[x].ID) + "'")
#        Domoticz.Debug("Device ID:       '" + Devices[x].DeviceID + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def DumpSettingsToLog():
    for x in Settings:
        if Settings[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Settings[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    return


def CreateSensor():
    if (len(Devices) == 0):
        # Domoticz.Device(Name="jodelo", Unit=1, TypeName="Custom",Used=1, DeviceID=devID).Create()
        Domoticz.Device(Name="Tonq-snmp", Unit=1, TypeName=Parameters["Mode3"], ,Used=1).Create()
        Domoticz.Log("Tonq sensor created")

def UpdateSensor():
    nVal=0
    sVal=255
    
    if Parameters["Mode4"] == "Emulate":
        nVal = Devices[1].nValue
        nVal += 5
        if nVal>255:
            nVal=0
        sVal = 255 - nVal
        Devices[1].Update(nVal,str(sVal))
    else:
        #if Parameters["Mode6"] == "Debug":
        #    r.debug=True
        t = Tonq()
        response = t.getOid(Parameters["Address"], Parameters["Mode1"], Parameters["Mode2"])
        if response["isOK"]==True:
            Devices[1].Update(0,str(response["value"]))
            Domoticz.Log("value=" + str(response["value"])) 
        else:
            Domoticz.Log("Sensor not updated. Err=" + str(response["value"]))


    lastUpdate = datetime.now()


def isActionTime(minutes):
    nextUpdate = lastUpdate + timedelta(minutes=minutes)
    Domoticz.Debug("isActionTime:nextUpdate=" + str(nextUpdate))
    return datetime.now() > nextUpdate


