# Problem

This is a short description on how I got to read the SOC data on my Tewaycell battery.

The supplier could not give me any information with regards to the communications, and my Inverter did not natively talk to the battery.

I have a https://tewaycell.com/collections/home-energy-storage-system/products/48v-100ah-lifepo4-wall-mounted-battery-storage-system?variant=40439721427001 - 10Kwh version

I communicate with the BMS via a RS485 USB convertor straight from the terminal.

See attached samples where I poll all 125 registers on the memory of the BMS. Clean unprocessed data (in the case of SOC) seemd to be the best.

Node-Red flow:
<img width="906" alt="image" src="https://user-images.githubusercontent.com/13587376/210770682-07103b57-474e-4ccd-8139-617ac1da50e4.png">


Here is a sample on my Homeassistant dashboard:
<img width="473" alt="image" src="https://user-images.githubusercontent.com/13587376/210770498-d6fbcb7e-cc68-4b43-9f3b-0a3501baedbb.png">
