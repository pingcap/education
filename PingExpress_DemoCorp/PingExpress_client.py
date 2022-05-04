## ==============================================
## main
## ==============================================
import time
from datetime import datetime, timedelta
import random
import argparse
import multiprocessing
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.sql import text


## ==============================================
## load
## ==============================================
def load(num_records, connection_string):
	engine = create_engine(connection_string, echo = False)

	sender_list = ["sender_1", "sender_2", "sender_3", "sender_4", "sender_5"]
	courier_list = ["courier_1", "courier_2", "courier_3", "courier_4", "courier_5"]
	receiver_list = ["receiver_1", "receiver_2", "receiver_3", "receiver_4", "receiver_5"]
	start_state_list = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", 
				"Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", 
				"Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", 
				"Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", 
				"Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", 
				"Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", 
				"Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", 
				"South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", 
				"Washington", "Wisconsin", "West Virginia", "Wyoming"]
	destination_state_list = start_state_list.copy()
	transaction_kind_list = ["1_pkg_in", "2_ori", "3_des", "4_pkg_out"]

	data_packages = []

	# generate records
	for i in range(num_records):
		one_package = {}
		time_delta = random.randint(0, 365)
		one_package["start_time"] = (datetime.now() - timedelta(time_delta)).strftime('%Y-%m-%d %H:%M:%S')
		one_package["update_time"] = one_package["start_time"]
		one_package["sender"] = sender_list[random.randint(0, 4)]
		one_package["courier"] = courier_list[random.randint(0, 4)]
		one_package["receiver"] = receiver_list[random.randint(0, 4)]
		one_package["start_state"] = start_state_list[random.randint(0, len(start_state_list) - 1)]
		one_package["destination_state"] = destination_state_list[random.randint(0, len(destination_state_list) - 1)]
		one_package["transaction_kind"] = transaction_kind_list[random.randint(0, 3)]
		data_packages.append(one_package)

	# load data
	with engine.connect() as con:
		statement_create_table = """CREATE TABLE IF NOT EXISTS packages (
	                package_id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	                start_time TIMESTAMP NOT NULL,
	                update_time TIMESTAMP NOT NULL,
	                sender TINYTEXT NOT NULL,
	                courier TINYTEXT NOT NULL,
	                receiver TINYTEXT NOT NULL,
	                start_state TINYTEXT NOT NULL,
	                destination_state TINYTEXT NOT NULL,
	                transaction_kind TINYTEXT NOT NULL);"""
		con.execute(statement_create_table)
		
		statement_insert_data = text("""INSERT INTO packages (start_time, update_time, sender, courier, receiver, start_state, destination_state, transaction_kind)
										VALUES(:start_time, :update_time, :sender, :courier, :receiver, :start_state, :destination_state, :transaction_kind)""")
		
		for line in data_packages:
			con.execute(statement_insert_data, **line)


## ==============================================
## execute
## ==============================================
def execute(duration, connection_string):
	engine = create_engine(connection_string, echo = False)

	transaction_kind_list = ["1_pkg_in", "2_ori", "3_des", "4_pkg_out"]

	start_time, current_time = time.time(), time.time()

	with engine.connect() as con:
		renew_record_num_counter = 0
		res_package_num = con.execute("SELECT count(*) from packages")

	while current_time - start_time <= duration:
		prob = random.random()

		# insert
		if prob <= 0.90:
			sender_list = ["sender_1", "sender_2", "sender_3", "sender_4", "sender_5"]
			courier_list = ["courier_1", "courier_2", "courier_3", "courier_4", "courier_5"]
			receiver_list = ["receiver_1", "receiver_2", "receiver_3", "receiver_4", "receiver_5"]
			start_state_list = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", 
						"Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", 
						"Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", 
						"Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", 
						"Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", 
						"Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", 
						"Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", 
						"South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", 
						"Washington", "Wisconsin", "West Virginia", "Wyoming"]
			destination_state_list = start_state_list.copy()
			transaction_kind_list = ["1_pkg_in", "2_ori", "3_des", "4_pkg_out"]

			data_packages = []

			# generate records
			for i in range(1):
				one_package = {}
				one_package["start_time"] = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
				one_package["update_time"] = one_package["start_time"]

				one_package["sender"] = sender_list[random.randint(0, 4)]
				one_package["courier"] = "courier_4"
				one_package["receiver"] = receiver_list[random.randint(0, 4)]
				one_package["start_state"] = start_state_list[random.randint(0, len(start_state_list) - 1)]
				one_package["destination_state"] = destination_state_list[random.randint(0, len(destination_state_list) - 1)]
				one_package["transaction_kind"] = transaction_kind_list[random.randint(0, 3)]
				data_packages.append(one_package)

			# load data
			with engine.connect() as con:
				statement_create_table = """CREATE TABLE IF NOT EXISTS packages (
			                package_id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
			                start_time TIMESTAMP NOT NULL,
			                update_time TIMESTAMP NOT NULL,
			                sender TINYTEXT NOT NULL,
			                courier TINYTEXT NOT NULL,
			                receiver TINYTEXT NOT NULL,
			                start_state TINYTEXT NOT NULL,
			                destination_state TINYTEXT NOT NULL,
			                transaction_kind TINYTEXT NOT NULL);"""
				con.execute(statement_create_table)
				
				statement_insert_data = text("""INSERT INTO packages (start_time, update_time, sender, courier, receiver, start_state, destination_state, transaction_kind)
												VALUES(:start_time, :update_time, :sender, :courier, :receiver, :start_state, :destination_state, :transaction_kind)""")
				
				for line in data_packages:
					con.execute(statement_insert_data, **line)

		# update
		else:
			with engine.connect() as con:
				# transaction start
				with con.begin():
					# find the package to update
					if renew_record_num_counter < 50:

						for row in res_package_num:
							package_id_to_update = random.randint(0, int(row[0]))
						renew_record_num_counter += 1
					else:
						renew_record_num_counter = 0
						res_package_num = con.execute("SELECT count(*) from packages")
						for row in res_package_num:
							package_id_to_update = random.randint(0, int(row[0]))			

					# get transaction_kind 0, 1, 2, or 3 
					statement = "SELECT transaction_kind FROM packages WHERE package_id=" + str(package_id_to_update) + ";"
					res_transaction_kind = con.execute(statement)
					for row in res_transaction_kind:
						transaction_kind = row[0]

					# update transaction kind
					if transaction_kind_list.index(transaction_kind) < 3:
						statement_update = "UPDATE packages set transaction_kind=\""+ str(transaction_kind_list[transaction_kind_list.index(transaction_kind) + 1]) + "\" WHERE package_id=" + str(package_id_to_update) + ";"
						con.execute(statement_update)

						time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
						statement_update_time = "UPDATE packages set update_time=\"" + str(time_now) + "\" WHERE package_id=" + str(package_id_to_update) + ";"
						con.execute(statement_update_time)
		time.sleep(0.1)
		current_time = time.time()

## ==============================================
## update timestamp
## ==============================================
def update_timestamp(connection_string):
	engine = create_engine(connection_string, echo = False)

	date_time_str = '21/12/15 00:00:00'
	date_time_obj = datetime.strptime(date_time_str, '%y/%m/%d %H:%M:%S')

	time_delta = datetime.now() - date_time_obj
	#print(time_delta.days)

	if time_delta.days == 0:
		print("no update needed")
	else:
		with engine.connect() as con:
			for i in range(1, 27):
				statement_update = "UPDATE packages set start_time = date_add(start_time, interval " + str(int(time_delta.days)) + " day) where package_id between " + str((i - 1) * 500000 + 1) + " and " + str(500000 * i);
				con.execute(statement_update)
				print(str(i) + " out of 26 finished.")


if __name__ == '__main__':
	aparser = argparse.ArgumentParser(description='Python implementation of the PingExpress_DemoCorp app')
	aparser.add_argument('--load', default=0, type=int, help='How many records to load')
	aparser.add_argument('--duration', default=10, type=int, metavar='D',help='How long to run the app in seconds')
	aparser.add_argument('--clients', default=1, type=int, metavar='N', help='The number of blocking clients to fork')
	aparser.add_argument('--execute', action='store_true', help='Executing the workload')
	aparser.add_argument('--update_timestamp', action='store_true', help='Update to latest timestamp')
	aparser.add_argument('--connection_string', type=str, help='connection string')
	args = vars(aparser.parse_args())
	# print(args)
	
	connection_string = args['connection_string']
	# connection_string = "tidb://PingExpress_client:123@<connection-string>:4000/PingExpressDB"
	
	if args['update_timestamp']:
		print("starts updating timestamp")
		update_timestamp(connection_string)
		print("updating timestamp finished")

	
	if args['load']:
		print("starts loading")
		pool = multiprocessing.Pool(args['clients'])
		for i in range(args['clients']):
			pool.apply_async(load, (int(args['load'] / args['clients']), connection_string,))      			
		pool.close()
		pool.join()
		print("data loading finished")
	
	if args['execute']:
		print("starts execution")
		pool = multiprocessing.Pool(args['clients'])
		for i in range(args['clients']):
			pool.apply_async(execute, (args['duration'], connection_string,))
		
		pool.close()
		pool.join()
		print("execute finished")
