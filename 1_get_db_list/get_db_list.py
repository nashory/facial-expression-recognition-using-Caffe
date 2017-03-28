#!/usr/local/bin/python
# - *- coding: utf- 8 - *-

######################################
# Coded by MCM.SHIN
# Last Modified : 2016.09.14
# Get file list
######################################


import sys, os, pprint
from os import walk

def write(file_name, contents):

	# make sure txt file exists.
	if not os.path.exists(file_name):
		print "Creating txt file ... %s" % file_name
		try:
			file = open(file_name,'w')  			 # Trying to create a new file or open one
			file.close()
 		except:
        		print "[ERROR] : Can not create %s file." % file_name
        		sys.exit(0)				 # quit Python

	# write on txt files.
	f = open(file_name, 'a')				# continue
	f.write(contents + "\n")				# write
	f.close()
	print "[Read from db] : %s" % contents


def __main__(argv):

	## Error exception ##
	argc = len(argv)	
	if (argc<3):
		print "[ERROR] Wrong input arguments. \
		       \n[USAGE] : get_db_list [db_folder] [output_folder]"
		return
	elif (argc>3):
		print "[ERROR] Too many input arguments. \
		       \n[USAGE] : get_db_list [db_folder] [output_folder]"
		return

	## set path ##
	db_path = argv[1]
	output_path = argv[2]




	if os.path.isdir(db_path) == False:
		print "[ERROR] db_folder directory does not exist."
		return
	if os.path.isdir(output_path) == False:			# make sure output directory exist.
		try:
			os.makedirs(output_path)
		except OSError as exc: 						# Guard against race condition
        		if exc.errno != errno.EEXIST:
            			raise

	## Create db_list.txt and db_label.txt
	db_list_path = output_path + "/db_list.txt"
	if os.path.exists(db_list_path):
		os.remove(db_list_path)


	# Write on txt file.
	total=0
	for (dir_path, dir_name, file_name) in os.walk(db_path, topdown=True):
		if len(file_name)!=0:					# if file exist.
			for th in file_name:
				if not (th.find(' ') == -1):			# if ' ' exists in file name
					prev = th.replace(" ", "\ ")
					th = th.replace(" ", "_")
					cmd = 'mv %s %s' % (dir_path+"/"+prev, dir_path+"/"+th)
					os.system(cmd)
					print "[File name changed] %s ===> %s" % (prev, th)
				
				label = th.split('_')[1]
				buf_str = th + ' ' + label
				write(db_list_path, buf_str)
				total = total+1
					

	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "Total # of files precessed : %d" % total
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
# Run.
__main__(sys.argv)
















