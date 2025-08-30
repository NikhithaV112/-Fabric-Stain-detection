import numpy as np
import argparse
# import imutils
import time
import cv2
import os
from tkinter import *
import tkinter.filedialog
import tkinter as tk
from PIL import ImageTk, Image

ap = argparse.ArgumentParser()

ap.add_argument("-o", "--output", required=False,
	help="path to output video")
ap.add_argument("-y", "--yolo", required=False,default="yolo_model",
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")  
args = vars(ap.parse_args())


labelsPath = os.path.sep.join([args["yolo"], "classes.names"])
LABELS = open(labelsPath).read().strip().split("\n")
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")
weightsPath = os.path.sep.join([args["yolo"], "custom.weights"])
configPath = os.path.sep.join([args["yolo"], "custom.cfg"])
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


(W, H) = (None, None)

def select_file():
	global file_selected,path,H, W, stain
	print("selecting file")
	path = tkinter.filedialog.askopenfilename()
	if len(path) > 0:
		frame=cv2.imread(path)
		frame=cv2.resize(frame,(480,360))
		if W is None or H is None:
			(H, W) = frame.shape[:2]

		blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
			swapRB=True, crop=False)
		net.setInput(blob)
		start = time.time()
		layerOutputs = net.forward(ln)
		end = time.time()
		boxes = []
		confidences = []
		classIDs = []
		area=0
		for output in layerOutputs:
			for detection in output:
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]
				if confidence > args["confidence"]:

					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)


		idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
			args["threshold"])

		if len(idxs) > 0:
			for i in idxs.flatten():
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])
				area = area+(w*h)
				color = [int(c) for c in COLORS[classIDs[i]]]
				cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(LABELS[classIDs[i]],
					confidences[i])
				cv2.putText(frame, text, (x, y - 5),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

		print(area)
		if(area<500):
			stain="Low"
		elif(area>500 and area<3000):
			stain="Medium"
		elif(area>3000):
			stain="High"

		cv2.putText(frame, stain, (10,50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
		cv2.imshow("video",frame)


root = tk.Tk()

# Load and display the image
image = Image.open("c.jpg")
# Resize the image if desired
image = image.resize((1400, 700), Image.ANTIALIAS)
tk_image = ImageTk.PhotoImage(image)

label = tk.Label(root, image=tk_image)
label.pack()

# Create and place the frame
frame = tk.Frame(root, bg="white", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# Create and place the heading label
heading = tk.Label(frame, text="FABRIC STAIN DETECTION", font=('Helvetica', 18, 'bold'), bg="black", fg="white")
heading.place(relwidth=1, relheight=1)



button = tk.Button(root, text="SELECT IMAGE", font=('Helvetica', 14),bg="black", fg="white", command=select_file)
button.place(relx=0.5, rely=0.5, anchor='center')
# Start the Tkinter event loop
root.mainloop()