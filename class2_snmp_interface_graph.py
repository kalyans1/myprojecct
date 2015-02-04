import snmp_helper
import pygal
import time
line_chart = pygal.Line()
IP = '50.242.94.227'
PORT1=7961
PORT2=8061
USER='pysnmp'
AUTH_KEY='galileo1'
ENCRYPT_KEY='galileo1'

SNMP_USER=(USER,AUTH_KEY,ENCRYPT_KEY)

pynet_rtr1= (IP,7961)
pynet_rtr2= (IP,8061)
DEVICES=((pynet_rtr1,"pynet_rtrA"), (pynet_rtr2,"pynet_rtrB"))
OIDS=['1.3.6.1.2.1.1.5.0','1.3.6.1.2.1.1.1.0','1.3.6.1.2.1.2']

"""for DEV in DEVICES:
    for OID in OIDS:
        SNMP_DATA=snmp_helper.snmp_get_oid_v3(DEV,SNMP_USER,oid=OID)
        output=snmp_helper.snmp_extract(SNMP_DATA)
        
        print output"""


SNMP_OIDS=(
('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5',True),
('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5',True),
('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5',True),
('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5',True),
)


OIDS=['.1.3.6.1.2.1.1.5.0','.1.3.6.1.2.1.1.1.0','.1.3.6.1.2.1.2.2.1.2.509']
#test=5

for DEV,NAME in DEVICES:
     OUTPUT={'ifInOctets_fa4':[],'ifInUcastPkts_fa4':[],'ifOutOctets_fa4':[],'ifOutUcastPkts_fa4':[]}
     test=5
     while test>0:
        for DESC,OID,BYTES in SNMP_OIDS:
            SNMP_DATA=snmp_helper.snmp_get_oid_v3(DEV,SNMP_USER,oid=OID,display_errors=True)
            output=snmp_helper.snmp_extract(SNMP_DATA)
            print "%s %s" %(DESC,output)
            OUTPUT[DESC].append(output)           
        test=test-1
        time.sleep(300)#grabing statics for every 5minutes 
        
     print DEV     
     print OUTPUT

 
 
 
     fa4_in_packets=OUTPUT['ifInUcastPkts_fa4']
     fa4_out_packets=OUTPUT['ifOutUcastPkts_fa4']
     fa4_out_octets=OUTPUT['ifOutOctets_fa4']
     fa4_in_octets=OUTPUT['ifInOctets_fa4']



     fa4_in_packets=map(int,fa4_in_packets) # map()changing strings into int for pygal:Example
                                         #results = ['1', '2', '3'] into results = [1, 2, 3]
     fa4_out_packets=map(int,fa4_out_packets)
     fa4_out_octets=map(int,fa4_out_octets)
     fa4_in_octets=map(int,fa4_in_octets)



     line_chart = pygal.Line()

   # Title
     line_chart.title = 'Input/Output Packets and Bytes' + NAME

   # X-axis labels (samples were every five minutes)
     line_chart.x_labels =map(str, range(5,55,5))

    # Add each one of the above lists into the graph as a line with corresponding title
     line_chart.add('InPackets', fa4_in_packets)
     line_chart.add('OutPackets', fa4_out_packets)
     line_chart.add('InBytes', fa4_out_octets)
     line_chart.add('OutBytes', fa4_in_octets)

    # Create an output image file from this
     line_chart.render_to_file(NAME+".svg")

