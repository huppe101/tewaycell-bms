import struct
import serial
import homeassistant.remote as remote
import time

while True:

# Set up the serial connection to the BMS
# here we need the serial to be imported.
ser = serial.Serial('/dev/tty.usbserial-A50285BI', 9600, timeout=1)

# Define the Modbus function code and starting register address
function_code = 3
starting_address = 1

# Calculate the number of registers to read
num_registers = 120  - starting_address + 1

# Pack the request into a bytearray
request = bytearray()
request.append(1)  # slave address
request.append(function_code)  # function code
request.append(starting_address >> 8)  # starting address (high byte)
request.append(starting_address & 0xFF)  # starting address (low byte)
request.append(num_registers >> 8)  # number of registers (high byte)
request.append(num_registers & 0xFF)  # number of registers (low byte)

# Calculate the CRC for the request
crc = 0xFFFF
for b in request:
    crc ^= b
    for i in range(8):
        if crc & 0x0001:
            crc = (crc >> 1) ^ 0xA001
        else:
            crc = crc >> 1
request.append(crc & 0xFF)  # CRC (low byte)
request.append(crc >> 8)  # CRC (high byte)

# Send the request to the BMS
ser.write(request)

# Read the response from the BMS
response = ser.read(num_registers * 2 + 5)

# Check the response to make sure it is valid
if response[0] != 1:
    raise Exception("Invalid slave address")
if response[1] != function_code:
    raise Exception("Invalid function code")
if len(response) != num_registers * 2 + 5:
    raise Exception("Invalid response length")

# Extract the data from the response
data = []
for element in response:
    data.append(element)

# Extract SOC value
soc = data[44]

# Use the python-homeassistant library to update the state of the sensor entity
# This seems to be a legacy way of doing things, and if we go this route, we need to import the password...

api = remote.API('http://localhost:8123', 'Kartoffels!#%')
remote.update_entity(api,'sensor.bms-soc', 'state', soc)

# Extract the cell values
cell1 = (data[75] * 255) + data[76]
cell2 = (data[77] * 255) + data[78]
cell3 = (data[227] * 255) + data[228]
cell4 = (data[229] * 255) + data[230]
cell5 = (data[231] * 255) + data[232]
cell6 = (data[233] * 255) + data[234]
cell7 = (data[235] * 255) + data[236]
cell8 = (data[237] * 255) + data[238]
cell9 = (data[239] * 255) + data[240]
cell10 = (data[241] * 255) + data[242]
cell11 = (data[243] * 255) + data[244]
cell12 = (data[245] * 255) + data[246]
cell13 = (data[247] * 255) + data[248]
cell14 = (data[249] * 255) + data[250]
cell15 = (data[251] * 255) + data[252]


# Use the python-homeassistant library to update the state of the sensor entities
remote.update_entity(api,'sensor.bms-cell1', 'state', cell1)
remote.update_entity(api,'sensor.bms-cell2', 'state', cell2)
remote.update_entity(api,'sensor.bms-cell3', 'state', cell3)
remote.update_entity(api,'sensor.bms-cell4', 'state', cell4)
remote.update_entity(api,'sensor.bms-cell5', 'state', cell5)
remote.update_entity(api,'sensor.bms-cell6', 'state', cell6)
remote.update_entity(api,'sensor.bms-cell7', 'state', cell7)
remote.update_entity(api,'sensor.bms-cell8', 'state', cell8)
remote.update_entity(api,'sensor.bms-cell9', 'state', cell9)
remote.update_entity(api,'sensor.bms-cell10', 'state', cell10)
remote.update_entity(api,'sensor.bms-cell11', 'state', cell11)
remote.update_entity(api,'sensor.bms-cell12', 'state', cell12)
remote.update_entity(api,'sensor.bms-cell13', 'state', cell13)
remote.update_entity(api,'sensor.bms-cell14', 'state', cell14)
remote.update_entity(api,'sensor.bms-cell15', 'state', cell15)


# Close the serial connection
ser.close()
   
 # Wait for 10 seconds before the next iteration of the while loop
    time.sleep(10)
