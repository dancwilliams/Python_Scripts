#$language = "Python"
#$interface = "1.0"

import os, time, filecmp, difflib

def main():

	crt.Screen.Synchronous = True
	# Tells CRT Screen to ignore case. Useful since device names do not use a standard case!
	crt.Screen.IgnoreCase = True
    # Select whether this is a PRE or POST test. 
	Test_Type = crt.Dialog.Prompt("Is the the PRE or POST test?:", "Please Select Test Type", "PRE or POST", False)
	
	# Test type input is turned all upper case
	Test_Type = Test_Type.upper()
	
    # If cancel is pressed there will be no input and script will exit
	if Test_Type == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
	
	Number_Device = crt.Dialog.Prompt("Will this test be run on one or multiple devices?:", "Please Select SINGLE or MULTI", "MULTI", False)
	# Test type input is turned all upper case
	Number_Device = Number_Device.upper()

	if Number_Device == "MULTI":
		Use_Jump = crt.Dialog.Prompt("Will this test use a jump host? (Ex. HPNA):", "Please Select Yes or No", "YES or NO", False)
		# Test type input is turned all upper case
		Use_Jump = Use_Jump.upper()
		# If cancel is pressed there will be no input and script will exit
		if Use_Jump == "YES":
			# Process Devices - Call multi_device_jump()
			multi_device_jump(Test_Type)
		elif Use_Jump == "NO":
			continue
		elif Use_Jump == "":
			crt.Dialog.MessageBox("Script Cancelled!")
	elif Number_Device == "SINGLE":
		Use_Jump = crt.Dialog.Prompt("Will this test use a jump host? (Ex. HPNA):", "Please Select Yes or No", "YES or NO", False)
		# Test type input is turned all upper case
		Use_Jump = Use_Jump.upper()
	
		if Use_Jump == "YES":
			# Process Devices - Call multi_device_jump()
			single_device_jump(Test_Type)
		elif Use_Jump == "NO":
			single_device(Test_Type)
		elif Use_Jump == "":
			crt.Dialog.MessageBox("Script Cancelled!")
	elif Number_Device == "":
		crt.Dialog.MessageBox("Script Cancelled!")
	
	Use_Jump = crt.Dialog.Prompt("Will this test use a jump host? (Ex. HPNA):", "Please Select Yes or No", "YES or NO", False)
	# Test type input is turned all upper case
	Use_Jump = Use_Jump.upper()
	
	# If cancel is pressed there will be no input and script will exit
	if Use_Jump == "YES":
		# Process Devices - Call multi_device_jump()
		multi_device_jump(Test_Type)
	elif Use_Jump == "":
		crt.Dialog.MessageBox("Script Cancelled!")
	
	# After all devices are worked through the user will be alerted that the script is complete
    # Connection to HPNA will remain up
	if Test_Type == "POST":
		compare(Device_List)
	else:
		crt.Dialog.MessageBox("COMPLETE!")
		crt.Screen.Synchronous = False

def multi_device_jump(Test_Type):
	# Opens dialog to select device list text file
	Device_List = open(crt.Dialog.FileOpenDialog(title="Please select a Device List text file",
                                                 filter="Text Files (*.txt)|*.txt||")).read().splitlines()
	if Device_List == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
		
	# Opens dialog to select command list text file
	Command_List = open(crt.Dialog.FileOpenDialog(title="Please select a Command List text file",
                                                  filter="Text Files (*.txt)|*.txt||")).read().splitlines()
	if Command_List == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
	
	# Set jump box prompt.  NA> for HPNA Proxy
	Jump_Prompt = crt.Dialog.Prompt("What is the base prompt for jump box?:", "Please enter prompt as shown on Jump Box",
                                    "NA>", False)
	for n, elem in enumerate(Device_List):
        # Set file name for PRE or POST test. Files are saved to same directory that script is using.
		timestr = time.strftime("%Y%m%d-%H%M%S")
		if Test_Type == "PRE":
			filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PRE_TEST_" + elem +'.txt')
		elif Test_Type == "POST":
			filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "POST_TEST_" + elem +'.txt')
		else:
			crt.Dialog.MessageBox("INVALID TEST TYPE!")
			return

		# Set prompt for script to expect
		promptStr = ( elem + "#")

        # Send return to for NA> that script is waiting for...
		crt.Screen.Send( '\r' )
		crt.Screen.WaitForString( Jump_Prompt )

        # Connect to element from device list
		crt.Screen.Send( "connect " + elem + " " + '\r' )

		# Wait for connection
		crt.Screen.WaitForString( promptStr )

        # Work through command list file - Call command()
		command(filename, Command_List, promptStr)

        # After all commands are parsed thhe script exits device and for loop continues through device list
        # crt.Sleep(2000) <- Leftover Test Piece
		crt.Screen.Send( "exit " + '\r' )
	
def single_device_jump(Test_Type):
	# Opens dialog to select device list text file
	elem = crt.Dialog.Prompt("What is the name of the device?:", "Enter Device Name", "SNUlbMUSalpdc01", False)
			
	# Opens dialog to select command list text file
	Command_List = open(crt.Dialog.FileOpenDialog(title="Please select a Command List text file",
                                                  filter="Text Files (*.txt)|*.txt||")).read().splitlines()
	if Command_List == "":
		crt.Dialog.MessageBox("Script Cancelled!")
		return
	
	# Set jump box prompt.  NA> for HPNA Proxy
	Jump_Prompt = crt.Dialog.Prompt("What is the base prompt for jump box?:", "Please enter prompt as shown on Jump Box",
                                    "NA>", False)
	
    # Set file name for PRE or POST test. Files are saved to same directory that script is using.
	timestr = time.strftime("%Y%m%d-%H%M%S")
	if Test_Type == "PRE":
		filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PRE_TEST_" + elem +'.txt')
	elif Test_Type == "POST":
		filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "POST_TEST_" + elem +'.txt')
	else:
		crt.Dialog.MessageBox("INVALID TEST TYPE!")
		return

	# Set prompt for script to expect
	promptStr = ( elem + "#")

    # Send return to for NA> that script is waiting for...
	crt.Screen.Send( '\r' )
	crt.Screen.WaitForString( Jump_Prompt )

    # Connect to element from device list
	crt.Screen.Send( "connect " + elem + " " + '\r' )

	# Wait for connection
	crt.Screen.WaitForString( promptStr )

    # Work through command list file - Call command()
	command(filename, Command_List, promptStr)

    # After all commands are parsed thhe script exits device and for loop continues through device list
    # crt.Sleep(2000) <- Leftover Test Piece
	crt.Screen.Send( "exit " + '\r' )
	
def command(filename, command_list, promptStr):
	# Open output file in append binary mode.  File will be created if it does not exist then appended
    # to with ever command that is run
	for m, command in enumerate(command_list):
		fileobj = open(filename, "ab")
		crt.Screen.Send( command + " \r" )
		crt.Screen.WaitForString( command + " \r" )
		result = crt.Screen.ReadString( promptStr )
		fileobj.write( result )
		fileobj.close()
	
def compare(Device_List):
	Compare_Request = crt.Dialog.Prompt("Would you like to compare PRE and POST files?:", "Please Select Y or N", "Y", False)
	Compare_Request = Compare_Request.upper()
	
	# If cancel is pressed there will be no input and script will exit
	if Compare_Request == "Y":
		for n, elem in enumerate(Device_List):
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
		crt.Dialog.MessageBox("COMPLETE!")
	elif Compare_Request == "N":
		crt.Dialog.MessageBox("No DIFF Requested...SCRIPT COMPLETE!")
	
main()
