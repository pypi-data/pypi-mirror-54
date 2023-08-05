TurnonModbusTCP



Python3.X :  import TurnonModbusTCP



clear_print()

	type: < Operation >
	request type: {}
	result type: {}

	Explanation: Clear the command lines.


get_my_IP()

	type: < Event >
	request type: {}
	result type: { [string] }

	Explanation:  Get your IP.


set_client()  # 

	type: < Operation >
	request type: { ServerIP= [string] , ServerPORT= [int] }
	result type: {}

	Explanation: Set up for connect to Modbus server.


client_start()

	type: < Operation >
	request type: {}
	result type: {}

	Explanation: Connect to Modbus server.


visual_command_Read()

	type: < Event >
	request type: {}
	result type: { [string] }

	Explanation: Get command from Franka apps br Modbus.


visual_output_Write()

	type: < Operation >
	request type: { [string] }
	result type: {}

	Explanation: Send the information to Franka arm by Modbus.


mode()

	type: < Event >
	request type: {}
	result type: { [int] }

	Explanation: It will return Franka arm's mode which are working.








