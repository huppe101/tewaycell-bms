import struct
import serial

# Set up the serial connection to the BMS
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

# Print the data
print(data)
