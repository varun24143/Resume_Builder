import os
import subprocess
import sys

root = "/home/ubuntu/yolov4"

os.chdir(os.path.join(root,"darknet"))

command = "make"
process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True,stderr=subprocess.STDOUT)
for line in process.stdout:
  sys.stdout.write(line.decode('utf-8'))

#Access to darknet
os.system("chmod +x ./darknet")

#Train the model
command = "./darknet detector train data/obj.data cfg/yolov4-custom.cfg yolov4.conv.137 -dont_show -map | tee output.log"
process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True,stderr=subprocess.STDOUT)
for line in process.stdout:
  sys.stdout.write(line.decode('utf-8'))

#Get the best saved model to yolov4-custom-functions
os.chdir(root)
p = os.system("cp ./darknet/backup/yolov4-custom_best.weights ./yolov4-custom-functions/data/custom.weights")
print(p)
print("Moved the weights")

#change dir to yolov4-custom-functions
os.chdir(os.path.join(root,"yolov4-custom-functions"))

#Change darknet model to tensorflow model
command = "python3 save_model.py --weights ./data/custom.weights --output ./checkpoints/custom-416 --input_size 416 --model yolov4"
process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True,stderr=subprocess.STDOUT)
for line in process.stdout:
  sys.stdout.write(line.decode('utf-8'))

#Crop detected portions
print("Cropping test images")
image_paths_file = os.path.join(root,'darknet/data/test.txt')
im_paths = open(image_paths_file, "r").readlines()

for i in im_paths:
  i = str(i).replace("\n","")
  cmd = "python3 detect.py --weights ./checkpoints/custom-416 --size 416 --model yolov4 --images "+i+" --crop"
  p = os.system(cmd)
  print("Cropped Image")