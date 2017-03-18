#
# Tonq class 
# The old network query (Snmp+1)
# By: gerardvs
#
# Find OID through smtpwalk.
# Example to get temperature of Synology disks
# snmpwalk -v 2c -c public 192.168.14.100 .1.3.6.1.4.1.6574.2
# iso.3.6.1.4.1.6574.2.1.1.2.0 = STRING: "Disk 1"
# iso.3.6.1.4.1.6574.2.1.1.2.1 = STRING: "Disk 2"
# iso.3.6.1.4.1.6574.2.1.1.3.0 = STRING: "ST2000DM001-sn-removed  "
# iso.3.6.1.4.1.6574.2.1.1.3.1 = STRING: "WD20EFRX-sn-removed     "
# iso.3.6.1.4.1.6574.2.1.1.4.0 = STRING: "SATA"
# iso.3.6.1.4.1.6574.2.1.1.4.1 = STRING: "SATA"
# iso.3.6.1.4.1.6574.2.1.1.5.0 = INTEGER: 1
# iso.3.6.1.4.1.6574.2.1.1.5.1 = INTEGER: 1
# iso.3.6.1.4.1.6574.2.1.1.6.0 = INTEGER: 28
# iso.3.6.1.4.1.6574.2.1.1.6.1 = INTEGER: 26
#

import sys
sys.path.append('/usr/lib/python3/dist-packages/')
from pysnmp.entity.rfc3413.oneliner import cmdgen

class Tonq:
    
    def __init__(self):
        self.debug=False

    #
    # getOid
    # returns dict with boolean and value
    #
    def getOid(self,sIP,sCommunity,sOID):
        retVal = ""
        valOK = True
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex,varBinds = cmdGen.getCmd(cmdgen.CommunityData(sCommunity),
                                                                          cmdgen.UdpTransportTarget((sIP, 161)),
                                                                          sOID)

        # Check for errors and print out results
        if errorIndication:
            valOK = False
            retVal = errorIndication                
        else:
            if errorStatus:
                valOK = False
                retVal =('%s at %s' % (errorStatus.prettyPrint(),
                                       errorIndex and 
                                       varBinds[int(errorIndex)-1] or '?'))
            else:
                for name, val in varBinds:
                    if self.debug:
                        print('%s = %s' % (name, val))
                    retVal = val
        if self.debug:
                print("retVal=" + retVal)
                
        return {'isOK': valOK , 'value': retVal}

    
    #
    # getOidValue
    # returns: snmp value
    #
    def getOidValue(self,sIP, sCommunity, sOID):
        response = self.getOid(sIP, sCommunity, sOID)    
        return response["value"]
     
     
#
# Example usage for testing only
#
#t = Tonq()
#t.debug=False
#tIP = '192.168.14.100'
#cmnty = 'public'

#oid = "iso.3.6.1.4.1.6574.2.1.1.6.0"
#response = t.getOid(tIP, cmnty, oid)
#if response["isOK"]==True:
#    print("value=" + str(response["value"]))
#else:
#    print("Error=" + str(response["value"]))


#oid = "iso.3.6.1.4.1.6574.2.1.1.6.1"
#response = t.getOidValue(tIP, cmnty, oid)
#print("response=" + str(response))


