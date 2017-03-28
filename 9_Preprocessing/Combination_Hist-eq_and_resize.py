#!/usr/local/bin/python


##########################################
# Coded by M.C.SHIN
# Last Modified : 2016.10.11
# Requirements : OpenCV 3.1
# Histogram-equalization and resize image source code.
# Usage : python Hist-eq_and_resize.py [Image_path] [Output_path] [size]
##########################################

import os, sys, glob
import cv2



def Save_resize_and_Hist(db_name, img_path, output_path, size):
	for infile in glob.glob( os.path.join(img_path, "*.jpg") ):
		im = cv2.imread(infile)
		
		# RGB to Gray
		im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		# Resize image
		im = cv2.resize(im, (size, size))
		# Apply Histogram-equalization
		cv2.equalizeHist(im,im);

		file_name = db_name+'-'+infile.split('/')[-1]
		file_path = output_path+'/'+ file_name
		cv2.imwrite(file_path, im)
		print '[Preprocessing...] %s' % file_name



if __name__=="__main__":

	# input error handling.
	argc = len(sys.argv)
	if argc!=5:
		print "[ERROR] Usage : python Hist-eq_and_resize.py [db_name] [Image_path] [Output_path] [size]"
		exit()

	# arguments.
	db_name = sys.argv[1]
	img_path = sys.argv[2]
	output_path = sys.argv[3]
	size = int(sys.argv[4])

	print img_path
	print output_path
	print size

	train_input = img_path

	train_output = output_path
	
	Save_resize_and_Hist(db_name, train_input, train_output, size)




