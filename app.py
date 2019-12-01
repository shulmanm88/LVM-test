#######################################
#Import functions
from can import *
from datetime import datetime, timedelta

##################################
# Test definitions:
wakeup_ctime = 0.3       #keep alive cycle time for the wakeup massage
test_time = 1          # test duration time ( minutes )
test_id = 140          # CAN sampling message I.D ( DEC )
test_avg = 2           # AVG Cycle time to pass the test

#########################################
#Variables definiton initiate
time_start = datetime.now()       #start time of the script
time_sent = datetime.now()- timedelta(seconds=(wakeup_ctime * 2))
counter = 0
delta_timestamp = 0
total_timestamp = 0
first_msg = True

###########################################################
#Message definitions
bus = Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)        #Define PCAN/CAN USBBUS# + BITRATE
wakeup_msg = Message(arbitration_id=320, is_extended_id=False, data=[0x45, 0x45, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
# Define keep.alive massage for the EOCM


while (datetime.now() - timedelta(minutes=test_time)) < time_start:

    if (datetime.now() - timedelta(seconds=wakeup_ctime)) > time_sent : # loop for wakeup msg cycling
        bus.send(wakeup_msg)
        time_sent = datetime.now()

    recv_msg = bus.recv(timeout = 0.0001)                                  # wait for msg no more than small amount of time
    if recv_msg != None :
        if (((recv_msg.arbitration_id)-test_id) == 0) :                   #check and filter for test msg
            if (first_msg == True) :
                roll_timestamp = recv_msg.timestamp                      # initiat roll_timestamp var
                first_msg = False
            delta_timestamp = recv_msg.timestamp - roll_timestamp        # calcs for avg
            total_timestamp += delta_timestamp
            roll_timestamp = recv_msg.timestamp
            counter += 1
##################for debugging######################################
            print (recv_msg)
            print (delta_timestamp)
            print (counter)
#######################################################

print (total_timestamp/counter)
if (total_timestamp/counter)< test_avg:
    print (True)
else:
    print (False)

##############  referances  ################
# bus.send_periodic(wakeup_msg, 1, 10)
# print(msg)
# print (hex(wakeup_msg.arbitration_id))
#for wakeup_msg in bus:
  #  print(wakeup_msg)
# print (msg.timestamp)
#tets_msg = bus.recv()
#print (bus.recv())



