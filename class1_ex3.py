from snmp_helper import snmp_get_oid,snmp_extract

# Uptime when running config last changed    
RunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   
# Uptime when running config last saved (note any 'write' constitutes a save)    
RunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
# Uptime when startup config last saved   
StartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'
#the sysUptime timestamp
sysUptime = '1.3.6.1.2.1.1.3.0'
OIDS=(sysUptime,RunningLastChanged,RunningLastSaved,StartupLastChanged)
port='7961'
port1='8061'
string='****'
devices=[('50.242.94.227',string,port),('50.242.94.227',string,port1)]
for device in devices:
    data=snmp_get_oid(device,oid=sysUptime, display_errors=True)
    uptime=snmp_extract(data)
    data1=snmp_get_oid(device,oid=RunningLastChanged, display_errors=True)
    RunLastChanged=snmp_extract(data1)
    data2=snmp_get_oid(device,oid=RunningLastSaved, display_errors=True)
    RunLastSaved=snmp_extract(data2)
    data3=snmp_get_oid(device,oid=StartupLastChanged, display_errors=True)
    StartLastChanged=snmp_extract(data3)
    print uptime
    print RunLastChanged
    print RunLastSaved
    print StartLastChanged
    
    if RunLastChanged > RunLastSaved:
        print "Running config changed but NOT saved"
    elif StartLastChanged==0:
        print "The startup-config has not been saved since the last boot"
    else:
        print "Config saved"
