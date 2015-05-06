#$language = "Python"
#$interface = "1.0"

import os
import time
import filecmp
import difflib

def main():

	crt.Screen.Synchronous = True
	# Tells CRT Screen to ignore case. Useful since device names do not use a standard case!
	crt.Screen.IgnoreCase = True
    # Select whether this is a PRE or POST test. 
	test_type = crt.Dialog.Prompt("Please select test option:\n 1. PRE Test\n 2. POST Test", "Please Select Test Type", "1", False)
	
    # If cancel is pressed there will be no input and script will exit
	if test_type == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
	
	number_device = crt.Dialog.Prompt("Please select test option:\n 1. Single Device Test\n 2. Multiple Device", "Please Select Test Type", "2", False)

	if number_device == "2":
		crt.Dialog.MessageBox("ONLY AVAILABLE THROUGH HPNA!")
		use_jump = "1"
		# If cancel is pressed there will be no input and script will exit
		if use_jump == "1":
			# Process Devices - Call multi_device_jump()
			multi_device_jump(test_type)
		elif use_jump == "2":
			return
		elif use_jump == "":
			crt.Dialog.MessageBox("Script Cancelled!")
			return
	if number_device == "1":
		use_jump = crt.Dialog.Prompt("Will this test use a jump host? (Ex. HPNA):\n 1. Yes\n 2. No", "Please Select Yes or No", "1", False)
		# Test type input is turned all upper case
		use_jump = use_jump.upper()
	
		if use_jump == "1":
			# Process Devices - Call multi_device_jump()
			single_device_jump(test_type)
		elif use_jump == "2":
			single_device(test_type)
		elif use_jump == "":
			crt.Dialog.MessageBox("Script Cancelled!")
	elif number_device == "":
		crt.Dialog.MessageBox("Script Cancelled!")
	
	# After all devices are worked through the user will be alerted that the script is complete
    # Connection to HPNA will remain up
	crt.Dialog.MessageBox("COMPLETE!")
	crt.Screen.Synchronous = False

def multi_device_jump(test_type):
	# Opens dialog to select device list text file
	device_list = open(crt.Dialog.FileOpenDialog(title="Please select a Device List text file",
                                                 filter="Text Files (*.txt)|*.txt||")).read().splitlines()
	if device_list == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
		
	# Opens dialog to select command list text file
	command_list = open(crt.Dialog.FileOpenDialog(title="Please select a Command List text file",
                                                  filter="Text Files (*.txt)|*.txt||")).read().splitlines()
	if command_list == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
	
	# Set jump box prompt.  NA> for HPNA Proxy
	jump_prompt = crt.Dialog.Prompt("What is the base prompt for jump box?:", "Please enter prompt as shown on Jump Box",
                                    "NA>", False)
	for n, elem in enumerate(device_list):
        # Set file name for PRE or POST test. Files are saved to same directory that script is using.
		timestr = time.strftime("%Y%m%d-%H%M%S")
		
		filename = name_file(test_type, elem)

		# Set prompt for script to expect
		promptStr = ( elem + "#")

        # Send return to for NA> that script is waiting for...
		crt.Screen.Send( '\r' )
		crt.Screen.WaitForString( jump_prompt )

        # Connect to element from device list
		crt.Screen.Send( "connect " + elem + " " + '\r' )

		# Wait for connection
		crt.Screen.WaitForString( promptStr )
		crt.Screen.Send( 'terminal width 100 \r' )
		crt.Screen.WaitForString( 'terminal width 100' )
		
        # Work through command list file - Call command()
		command(filename, command_list, promptStr)

        # After all commands are parsed thhe script exits device and for loop continues through device list
        # crt.Sleep(2000) <- Leftover Test Piece
		crt.Screen.Send( "exit " + '\r' )
	if test_type == "2":
		multi_compare(device_list)

def single_device_jump(test_type):
	# Opens dialog to select device list text file
	elem = crt.Dialog.Prompt("What is the name of the device?:", "Enter Device Name", "SNUlbMUSalpdc01", False)
	elem = elem.rstrip('\r\n')
	# Opens dialog to select command list text file
	command_list = open(crt.Dialog.FileOpenDialog(title="Please select a Command List text file", filter="Text Files (*.txt)|*.txt||")).read().splitlines()
	if command_list == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
	# Set jump box prompt.  NA> for HPNA Proxy
	jump_prompt = crt.Dialog.Prompt("What is the base prompt for jump box?:", "Please enter prompt as shown on Jump Box",
                                    "NA>", False)
    # Set file name for PRE or POST test. Files are saved to same directory that script is using.
	timestr = time.strftime("%Y%m%d-%H%M%S")
	
	filename = name_file(test_type, elem)

	# Set prompt for script to expect
	promptStr = ( elem + "#")

    # Send return to for NA> that script is waiting for...
	crt.Screen.Send( '\r' )
	crt.Screen.WaitForString( jump_prompt )

    # Connect to element from device list
	crt.Screen.Send( "connect " + elem + " " + '\r' )

	# Wait for connection
	crt.Screen.WaitForString( promptStr )
	crt.Screen.Send( 'terminal width 100 \r' )
	crt.Screen.WaitForString( 'terminal width 100' )

    # Work through command list file - Call command()
	command(filename, command_list, promptStr)

    # After all commands are parsed thhe script exits device and for loop continues through device list
    # crt.Sleep(2000) <- Leftover Test Piece
	crt.Screen.Send( "exit " + '\r' )
	if test_type == "2":
		single_compare(elem)

def single_device(test_type):
	# Opens dialog to select device list text file
	# elem = crt.Dialog.Prompt("What is the name of the device? Use same for PRE and POST for DIFF:", "Enter Device Name", "SNUlbMUSalpdc01", False)
	
	crt.Screen.Send( '\r' )
	crt.Screen.WaitForString( '#' )
	crt.Screen.Send( '\r' )
	crt.Screen.WaitForString( '#' )
	screenrow = crt.Screen.CurrentRow - 1
	elem = crt.Screen.Get(screenrow, 1, screenrow, 40)
	elem = elem.replace("#", "")
	elem = elem.rstrip('\r\n')
	elem = elem.strip()
	
	# Opens dialog to select command list text file
	command_list = open(crt.Dialog.FileOpenDialog(title="Please select a Command List text file",
                                                  filter="Text Files (*.txt)|*.txt||")).read().splitlines()
	if command_list == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
	
	# Set file name for PRE or POST test. Files are saved to same directory that script is using.
	timestr = time.strftime("%Y%m%d-%H%M%S")
	filename = name_file(test_type, elem)

	# Set prompt for script to expect
	promptStr = ( elem + "#")
    # Send return to for NA> that script is waiting for...
	crt.Screen.Send( '\r' )
	crt.Screen.WaitForString( promptStr )
	crt.Screen.Send( 'terminal width 100 \r' )
	crt.Screen.WaitForString( 'terminal width 100' )

    # Work through command list file - Call command()
	command(filename, command_list, promptStr)

    # After all commands are parsed thhe script exits device and for loop continues through device list
    # crt.Sleep(2000) <- Leftover Test Piece
	if test_type == "2":
		single_compare(elem)
	
def command(filename, command_list, promptStr):
	# Open output file in append binary mode.  File will be created if it does not exist then appended
    # to with ever command that is run
	for m, command in enumerate(command_list):
		fileobj = open(filename, "ab")
		command = command.strip()
		crt.Screen.Send( command + " \r" )
		trunc_command = command[-10:]
		# crt.Dialog.MessageBox(command)
		crt.Screen.WaitForString( trunc_command + " \r" )
		result = crt.Screen.ReadString( promptStr )
		fileobj.write( command )
		fileobj.write( result )
		fileobj.close()
	
def multi_compare(device_list):
	Compare_Request = crt.Dialog.Prompt("Would you like to compare PRE and POST files?:\n 1. Yes\n 2. No", "Please Make Selection", "1", False)
	
	# If cancel is pressed there will be no input and script will exit
	if Compare_Request == "1":
		for n, elem in enumerate(device_list):
			prefilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PRE_TEST_" + elem +'.txt')
			postfilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "POST_TEST_" + elem +'.txt')
			difffilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DIFF_" + elem +'.txt')
		
			with open(prefilename,'r') as f:
				d=f.readlines()
		
			with open(postfilename,'r') as f:
				e=f.readlines()

			open(difffilename,'w').close() #Create the file

			with open(difffilename,'a') as f:
				diff = difflib.unified_diff( d, e, fromfile=prefilename, tofile=postfilename )
				f.writelines(diff)
				#for line in list(d-e):
				#	f.write(line)
		crt.Dialog.MessageBox("DIFF COMPLETE!")
	elif Compare_Request == "2":
		crt.Dialog.MessageBox("No DIFF Requested...SCRIPT COMPLETE!")

def single_compare(elem):
	Compare_Request = crt.Dialog.Prompt("Would you like to compare PRE and POST files?:\n 1. Yes\n 2. No", "Please Make Selection", "1", False)
	
	# If cancel is pressed there will be no input and script will exit
	if Compare_Request == "1":
		prefilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PRE_TEST_" + elem +'.txt')
		postfilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "POST_TEST_" + elem +'.txt')
		difffilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DIFF_" + elem +'.txt')
		
		with open(prefilename,'r') as f:
			d=f.readlines()
		
		with open(postfilename,'r') as f:
			e=f.readlines()

		open(difffilename,'w').close() #Create the file

		with open(difffilename,'a') as f:
			diff = difflib.unified_diff( d, e, fromfile=prefilename, tofile=postfilename )
			f.writelines(diff)
			#for line in list(d-e):
			#	f.write(line)
		crt.Dialog.MessageBox("DIFF COMPLETE!")
	elif Compare_Request == "2":
		crt.Dialog.MessageBox("No DIFF Requested...SCRIPT COMPLETE!")		

def name_file(test_type, elem):
	if test_type == "1":
		filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PRE_TEST_" + elem +'.txt')
		return filename
	elif test_type == "2":
		filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "POST_TEST_" + elem +'.txt')
		return filename
	else:
		crt.Dialog.MessageBox("INVALID TEST TYPE!")
		return
main()
