import numpy as np
import csv
import cv2
import pandas as pd
import os
txt_path = "./-----.txt"
data_in_txt = {'a_frame': [], 'b_xmin': [], 'c_ymin': [], 'd_xmax' : [], 'e_ymax' : []}
with open(txt_path, "r") as txt_file:
	for line in txt_file:
		if line.split() != []:
			data_in_txt['a_frame'].append(int(line.split(" ")[0].split(",")[0]))
			data_in_txt['b_xmin'].append(int(float(line.split(" ")[-4])))
			data_in_txt['c_ymin'].append(int(float(line.split(" ")[-3])))
			data_in_txt['d_xmax'].append(int(float(line.split(" ")[-2])))
			data_in_txt['e_ymax'].append(int(float(line.split(" ")[-1].split("\n")[0])))
data=pd.DataFrame(data_in_txt)
data=data.reset_index()
data.columns=['ix0','frame','xmin','ymin','xmax','ymax']
data['ID']=0

img_path = "./-----"
files = []
exts = ["jpg", "png", "PNG", "JPG"]
for parent, dirnames, filenames in os.walk(img_path):
	for filename in filenames:
		for ext in exts:
			if filename.endswith(ext):
				files.append(os.path.join(parent, filename))
				break
files.sort()
print(files)
def iou(bb_test,bb_gt):
	xx1 = np.maximum(float(bb_test[2]),float(bb_gt[2]))
	yy1 = np.maximum(float(bb_test[3]),float(bb_gt[3]))
	xx2 = np.minimum(float(bb_test[4]),float(bb_gt[4]))
	yy2 = np.minimum(float(bb_test[5]),float(bb_gt[5]))
	ww = np.maximum(0., xx2 - xx1)
	hh = np.maximum(0., yy2 - yy1)
	wh = ww * hh
	o = wh / ((float(bb_test[4])-float(bb_test[2]))*(float(bb_test[5])-float(bb_test[3]))+ (float(bb_gt[4])-float(bb_gt[2]))*(float(bb_gt[5])-float(bb_gt[3]))- wh)
	return(o)


framenum=max(data.values[:,1])
cv2.namedWindow('current frame unmarked')
cv2.resizeWindow('current frame unmarked', 1280, 720)
cv2.namedWindow('last frame marked')
cv2.resizeWindow('last frame marked', 1280, 720)
i = 0
check_points_frame_q = []
while(i < framenum):
	break_flag = 0
	i = i + 1
	# print('frame:',i)
	# stri='00000'+str(i)
	# stri=stri[-6:]
	path = files[i - 1]
	img = cv2.imread(path)
	print('path:',path)
	
	if i > 1:
		cv2.imshow('last frame marked',cv2.resize(check_points_frame_q[-1], (700, 400)))
		cv2.waitKey(100)
	else:
		the_first_frame = img.copy()
		cv2.putText(the_first_frame,"First frame", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 4, 8)
		cv2.imshow('last frame marked',cv2.resize(the_first_frame, (700, 400)))
		cv2.waitKey(100)
	image =[]
	index =[] 
	detect = data[data['frame']==i].values[:,0]
	num_of_box = 0
	check_points_frame = []
	continue_flag = 0
	while(num_of_box < len(detect)):
		j = int(detect[num_of_box])
		print('frame :', i)
		print("num_of_box ", num_of_box)
		data_j5 = data.values[j,2] * 1920 / 1000
		data_j6 = data.values[j,3] * 1080 / 562
		data_j7 = data.values[j,4] * 1920 / 1000
		data_j8 = data.values[j,5] * 1080 / 562	
		a = 0
		ID = 0
		if i >1:
			laframe = data[data['frame'] == i - 1].values[:,0]
			for l in laframe:       #simple iou predict ID
				l = int(l)
				# print('iou test detect:',l)		
				IOU = iou(data.values[int(float(j))],data.values[int(float(l))])
				if IOU > a :
					a = IOU 
					ID = data.values[l,6]
		if continue_flag == 0:
			check_points_frame.append(img.copy())
		img = check_points_frame[-1].copy()
		preimg = img.copy()
		cv2.putText(img, str(ID), (int(data_j5-1), int(data_j6-1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 4, 8)
		cv2.rectangle(img, (int(data_j5), int(data_j6)), (int(data_j7), int(data_j8)), (0, 0, 255), 2)
		cv2.imshow('current frame unmarked',cv2.resize(img, (700, 400)))
		cv2.waitKey(100)
		if i == 1:
			ans = input("ID = ")
			break_flag = 0
			continue_flag = 0
			if ans == "q" and i > 1:
				i = i - 2
				del(check_points_frame_q[-1])
				break_flag = 1
				break
			if ans == "z" and num_of_box > 0:
				num_of_box = num_of_box - 1
				del(check_points_frame[-1])
				print(len(check_points_frame))	
				print("cancel")
				continue_flag = 1
				continue
			if ans :
				while(not ans.isdigit()):
					ans = input("input number ,ID = ")
				ID = int(ans)
			else:
				ID = num_of_box
		else:
			ans = input('ID = %s?'%str(ID))
			break_flag = 0
			continue_flag = 0
			if ans == "q" and i > 1:
				i = i - 2
				del(check_points_frame_q[-1])
				break_flag = 1
				break
			if ans == "z" and num_of_box > 0:
				num_of_box = num_of_box - 1
				del(check_points_frame[-1])
				img = check_points_frame[-1].copy()		
				print("cancel")
				continue_flag = 1
				continue
			if ans :
				while(not ans.isdigit()):
					ans = input("input number ,ID = ")
				ID = int(ans)	
		img = preimg.copy()
		cv2.putText(img,str(ID),(int(data_j5-1), int(data_j6-1)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),4,8)
		cv2.rectangle(img, (int(data_j5), int(data_j6)), (int(data_j7), int(data_j8)),(255, 0, 0),2)
		cv2.imshow('current frame unmarked',cv2.resize(img, (700, 400)))
		cv2.waitKey(100)
		data.iat[j,6] = int(ID)
		print("\nFII")
		print("-------------------------")
		num_of_box = num_of_box + 1
	if break_flag == 0:
		check_points_frame_q.append(img.copy())

cv2.destroyAllWindows()
data.to_csv('-----.csv',header= True,index = False)


		

