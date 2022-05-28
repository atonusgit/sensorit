from ruuvitag_sensor.ruuvi import RuuviTagSensor
import json
import datetime
import os
import os.path
from os import path
from os import system
from dotenv import load_dotenv

load_dotenv()

pistorasiat_root = os.getenv('PISTORASIAT_ROOT_DIRECTORY')
pistorasiat_user = os.getenv('PISTORASIAT_USERNAME')
pistorasiat_address=os.getenv('PISTORASIAT_ADDRESS')

# List of macs of sensors which data will be collected
# If list is empty, data will be collected for all found sensors
macs = ['00:00:00:00:00:00', 'EE:1B:38:69:04:A5', 'F0:A2:43:0F:F8:F3', 'F4:06:DB:A1:07:83', 'E6:FB:19:D6:DD:09', 'C6:45:03:0B:5F:4F', 'E0:50:B9:86:15:BF', 'F1:31:71:E6:A4:B6']
names = ['kello', 'kuisti', 'saunan_putket', 'keittion_putket', 'vessan_putket', 'sisalla', 'vessa', 'kasvihuone']
sockets = ['0', '0', '0', 'A', '0', '0', '0', '0']
temperatures_alert_thresholds = [0, -50, -50, -50, -50, -50, -50, -50]
temp_switch_on_thresholds = [-100, -100, -100, 5, -100, -100, -100, -100]
temp_switch_off_thresholds = [100, 100, 100, 17, 100, 100, 100, 100]

logsfolder = os.getenv('ROOT_DIRECTORY') + "/sensor_logs/"
tmp = {"data_format": 0, "humidity": 0, "temperature": 0, "pressure": 0, "acceleration": 0, "acceleration_x": 0, "acceleration_y": 0, "acceleration_z": 0, "tx_power": 0, "battery": 0, "movement_counter": 0, "measurement_sequence_number": 0, "mac": "-"}

# get_data_for_sensors will look data for the duration of timeout_in_sec
timeout_in_sec = 10

# function to add to JSON
def write_json(data, filename='data.json'):
	with open(logsfolder + filename, 'w') as f:
		json.dump(data, f, indent=4)

def read_json(filename=os.getenv('ROOT_DIRECTORY') + "/status_files/all_status.json"):
	with open(filename, encoding='utf-8') as json_file:
		return json.load(json_file)

all_status = read_json()

# error logging
log_date = datetime.datetime.now()
print(log_date.strftime("%m.%d %H:%M:%S start"))

datas = RuuviTagSensor.get_data_for_sensors(macs[1:], timeout_in_sec)
timestamp = datetime.datetime.now().strftime("%d.%m.%Y %X")

# error logging
log_date = datetime.datetime.now()
print(log_date.strftime("%m.%d %H:%M:%S process"))

for i, mac in enumerate(macs, start=0):
	if mac in datas:
		datas[mac]['timestamp'] = timestamp
		inputdata = datas[mac]
	else:

		# get data from tmp
		try:
			with open(logsfolder + names[i] + "_tmp.json", "r") as file_data:
				tmp = json.load(file_data)
		except:
			pass

		if names[i] == 'kello':
			tmp = {}

		tmp['timestamp'] = timestamp
		inputdata = tmp

	# error logging
	print("inputdata:")
	print(inputdata)

	filename = datetime.datetime.now().strftime("%y%m%d_" + names[i] + ".json")
	try:
		with open(logsfolder + filename) as json_file:
			data = json.load(json_file)
			data.append(inputdata)
	except:
		data = [inputdata]

	write_json(data, filename)
	write_json(inputdata, names[i] + "_tmp.json")

	# send alert
	if (names[i] != 'kello') and (inputdata['temperature'] < temperatures_alert_thresholds[i]):
		if not path.exists(logsfolder + 'alert_' + names[i] + '.json'):
			write_json(names[i] + '_under_' + str(temperatures_alert_thresholds[i]), 'alert_' + names[i] + '.json')

	if (names[i] != 'kello'):
		print('switch of ' + names[i] + ' and its temp is')
		print(inputdata['temperature'])
		print('threshold')
		print(temp_switch_on_thresholds[i])

	# switch on
	if (names[i] != 'kello') and (inputdata['temperature'] < temp_switch_on_thresholds[i]) and all_status[sockets[i]]["status"] == 'is_read_off':
		print(names[i] + ' - on')
		os.system("ssh " + pistorasiat_user + "@" + str(pistorasiat_address) + " 'python3 " + pistorasiat_root + "/remote_control.py " + sockets[i] + " on'")
		write_json({"status": 1}, names[i] + "_switch.json")

	# switch off
	if (names[i] != 'kello') and (inputdata['temperature'] > temp_switch_off_thresholds[i]) and all_status[sockets[i]]["status"] == 'is_read_on':
		print(names[i] + ' - off')
		os.system("ssh " + pistorasiat_user + "@" + str(pistorasiat_address) + " 'python3 " + pistorasiat_root + "/remote_control.py " + sockets[i] + " off'")
		write_json({"status": 2}, names[i] + "_switch.json")

log_date = datetime.datetime.now()
print(log_date.strftime("%m.%d %H:%M:%S done"))
