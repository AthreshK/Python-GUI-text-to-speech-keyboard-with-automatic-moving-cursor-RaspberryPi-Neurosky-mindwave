import serial
c=0
values=[]
ser = serial.Serial('/dev/ttyACM0', 57600)
while 1:
	string_data = ser.readline()
	for char in string_data:
		c = c+1
		if (char == '$'):
			for i in range(3):
				values.append(string_data[c+i])
def sun(values):
	val=""
	for value in values:
		val = val+value
	return val

attention = int(sum(values[0:3]))
meditation = int(sum(values[3:6]))
blink = int(sum(values[6:9]))

print (attention)
print (meditation)
print (blink)
	
