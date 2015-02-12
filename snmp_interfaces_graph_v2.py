import snmp_helper
import time
import pygal

IP1 = '10.233.255.247'
IP2 = '10.233.255.237'
PORT1=7961
PORT2=8061
USER='pysnmp'
AUTH_KEY='galileo1'
ENCRYPT_KEY='galileo1'
 
SNMP_USER_V3=(USER,AUTH_KEY,ENCRYPT_KEY)
SNMP_V2='galileo'

pynet_rtr1= (IP1,SNMP_V2,161)
pynet_rtr2= (IP2,SNMP_V2,161)
#DEVICES=[pynet_rtr1,pynet_rtr2]
DEVICES=[pynet_rtr2]



SNMP_OIDS=(
('ifInOctets_ge2', '1.3.6.1.2.1.2.2.1.10.520',True),
('ifInUcastPkts_ge2', '1.3.6.1.2.1.2.2.1.11.520',True),
('ifOutOctets_ge2', '1.3.6.1.2.1.2.2.1.16.520',True),
('ifOutUcastPkts_ge2', '1.3.6.1.2.1.2.2.1.17.520',True),
)

OUTPUT={'ifInOctets_ge2':[],'ifInUcastPkts_ge2':[],'ifOutOctets_ge2':[],'ifOutUcastPkts_ge2':[]}
OIDS=['.1.3.6.1.2.1.1.5.0','.1.3.6.1.2.1.1.1.0','.1.3.6.1.2.1.2.2.1.2.509']
test=5
for DEV in DEVICES:
    while test>0: 
        #test=4# running for loop for 4 times
        for DESC,OID,BYTES in SNMP_OIDS:
            SNMP_DATA=snmp_helper.snmp_get_oid(DEV,oid=OID,display_errors=True)
            output=snmp_helper.snmp_extract(SNMP_DATA)
            print "%s %s" %(DESC,output)
            OUTPUT[DESC].append(output)           
        test=test-1
        time.sleep(10)#grabing statics for every 5minutes 
        
         
#print OUTPUT
fa4_in_packets=OUTPUT['ifInUcastPkts_ge2']
fa4_out_packets=OUTPUT['ifOutUcastPkts_ge2']
fa4_out_octets=OUTPUT['ifOutOctets_ge2']
fa4_in_octets=OUTPUT['ifInOctets_ge2']



fa4_in_packets=map(int,fa4_in_packets) # map()changing strings into int for pygal:Example
                                         #results = ['1', '2', '3'] into results = [1, 2, 3]
fa4_out_packets=map(int,fa4_out_packets)
fa4_out_octets=map(int,fa4_out_octets)
fa4_in_octets=map(int,fa4_in_octets)


"""
lline_chart = pygal.Line()
line_chart.title = 'Browser usage evolution (in %)'
line_chart.x_labels = map(str, range(2002, 2013))
line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
line_chart.render() """

line_chart = pygal.Line()

# Title
line_chart.title = 'Input/Output Packets and Bytes'

# X-axis labels (samples were every five minutes)
line_chart.x_labels =map(str, range(5,55,5))

"""range([start], stop[, step])

    start: Starting number of the sequence.
    stop: Generate numbers up to, but not including this number.
    step: Difference between each number in the sequence. """


# Add each one of the above lists into the graph as a line with corresponding title
line_chart.add('InPackets', fa4_in_packets)
line_chart.add('OutPackets',  fa4_out_packets)
line_chart.add('InBytes', fa4_out_octets)
line_chart.add('OutBytes', fa4_in_octets)

# Create an output image file from this
#line_chart.render_to_file('test.svg')
line_chart.render_in_browser()

