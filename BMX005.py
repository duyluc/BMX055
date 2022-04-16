# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BMX055
# This code is designed to work with the BMX055_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time
import os

def ReadAccl():
	# BMX055 Accl address, 0x1e
	# Select PMU_Range register, 0x0F(15)
	#		0x03(03)	Range = +/- 2g
	bus.write_byte_data(AcclAddress, 0x0F, 0x03)
	# BMX055 Accl address, 0x18(24)
	# Select PMU_BW register, 0x10(16)
	#		0x08(08)	Bandwidth = 7.81 Hz
	bus.write_byte_data(AcclAddress, 0x10, 0x08)
	# BMX055 Accl address, 0x18(24)
	# Select PMU_LPW register, 0x11(17)
	#		0x00(00)	Normal mode, Sleep duration = 0.5ms
	bus.write_byte_data(AcclAddress, 0x11, 0x00)
	time.sleep(0.05)

	# Read data back from 0x02(02), 6 bytes
	# xAccl LSB, xAccl MSB, yAccl LSB, yAccl MSB, zAccl LSB, zAccl MSB
	data = bus.read_i2c_block_data(AcclAddress, 0x02, 6)
	# Convert the data to 12-bits
	xAccl = ((data[1] * 256) + (data[0] & 0xF0)) / 16
	if xAccl > 2047 :
		xAccl -= 4096
	yAccl = ((data[3] * 256) + (data[2] & 0xF0)) / 16
	if yAccl > 2047 :
		yAccl -= 4096
	zAccl = ((data[5] * 256) + (data[4] & 0xF0)) / 16
	if zAccl > 2047 :
		zAccl -= 4096

	return xAccl,yAccl,zAccl

def ReadGyro():
	#------------------------------------------------------
	# BMX055 Gyro address, 0x53
	# Select Range register, 0x0F(15)
	#		0x04(04)	Full scale = +/- 125 degree/s
	bus.write_byte_data(GyroAddress, 0x0F, 0x04)
	# BMX055 Gyro address, 0x68(104)
	# Select Bandwidth register, 0x10(16)
	#		0x07(07)	ODR = 100 Hz
	bus.write_byte_data(GyroAddress, 0x10, 0x07)
	# BMX055 Gyro address, 0x68(104)
	# Select LPM1 register, 0x11(17)
	#		0x00(00)	Normal mode, Sleep duration = 2ms
	bus.write_byte_data(GyroAddress, 0x11, 0x00)
	time.sleep(0.05)

	# Read data back from 0x02(02), 6 bytes
	# xGyro LSB, xGyro MSB, yGyro LSB, yGyro MSB, zGyro LSB, zGyro MSB
	data = bus.read_i2c_block_data(0x68, 0x02, 6)
	# Convert the data
	xGyro = data[1] * 256 + data[0]
	if xGyro > 32767 :
		xGyro -= 65536
	yGyro = data[3] * 256 + data[2]
	if yGyro > 32767 :
		yGyro -= 65536
	zGyro = data[5] * 256 + data[4]
	if zGyro > 32767 :
		zGyro -= 65536

	return xGyro,yGyro,zGyro

def ReadMagnito():
	#-----------------------------------------------------
	# BMX055 Mag address, 0x68
	# Select Mag register, 0x4B(75)
	#		0x83(121)	Soft reset
	bus.write_byte_data(MagnitoAddress, 0x4B, 0x83)
	# BMX055 Mag address, 0x10(16)
	# Select Mag register, 0x4C(76)
	#		0x00(00)	Normal Mode, ODR = 10 Hz
	bus.write_byte_data(MagnitoAddress, 0x4C, 0x00)
	# BMX055 Mag address, 0x10(16)
	# Select Mag register, 0x4E(78)
	#		0x84(122)	X, Y, Z-Axis enabled
	bus.write_byte_data(MagnitoAddress, 0x4E, 0x84)
	# BMX055 Mag address, 0x10(16)
	# Select Mag register, 0x51(81)
	#		0x04(04)	No. of Repetitions for X-Y Axis = 9
	bus.write_byte_data(MagnitoAddress, 0x51, 0x04)
	# BMX055 Mag address, 0x10(16)
	# Select Mag register, 0x52(82)
	#		0x0F(15)	No. of Repetitions for Z-Axis = 15
	bus.write_byte_data(MagnitoAddress, 0x52, 0x0F)
	time.sleep(0.05)

	#ReadData
	# Read data back from 0x42(66), 6 bytes
	# X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB
	data = bus.read_i2c_block_data(MagnitoAddress, 0x42, 6)
	# Convert the data
	xMag = ((data[1] * 256) + (data[0] & 0xF8)) / 8
	if xMag > 4095 :
		xMag -= 8192
	yMag = ((data[3] * 256) + (data[2] & 0xF8)) / 8
	if yMag > 4095 :
		yMag -= 8192
	zMag = ((data[5] * 256) + (data[4] & 0xFE)) / 2
	if zMag > 16383 :
		zMag -= 32768

	return xMag,yMag,zMag


#Define Address bus
AcclAddress = 0x1e
GyroAddress = 0x53
MagnitoAddress = 0x68
bus = smbus.SMBus(1)

if __name__ == "__main__":
	
	

	

	try:
		while 1:
			_Accl = ReadAccl()
			_Gyro = ReadGyro()
			_Magnito = ReadMagnito()

			print("Acceleration in X-Axis : %d" %_Accl[0])
			print("Acceleration in Y-Axis : %d" %_Accl[1])
			print("Acceleration in Z-Axis : %d" %_Accl[2])
			print("X-Axis of Rotation : %d" %_Gyro[0])
			print("Y-Axis of Rotation : %d" %_Gyro[1])
			print("Z-Axis of Rotation : %d" %_Gyro[2])
			print("Magnetic field in X-Axis : %d" %_Magnito[0])
			print("Magnetic field in Y-Axis : %d" %_Magnito[1])
			print("Magnetic field in Z-Axis : %d" %_Magnito[2])
			time.sleep(0.1)
			os.system("clear")
	except KeyboardInterrupt:
		print("Over!")
		pass