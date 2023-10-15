import os
import os.path
import json
import piexif
import mutagen
import shutil
from mutagen.mp4 import MP4
from os import scandir
from exif import Image
from datetime import datetime
from PIL import Image
from tkinter import filedialog


# FUNCTION FOR CONVERTING TIME FROM .JSON FILE TO TIME FOR EXIF FILE
def parsed_time(time):
  input_date_string = time
  input_format = "%b %d, %Y, %I:%M:%S %p %Z"
  output_format = "%Y:%m:%d %I:%M:%S"
  # Parsing the input date string
  parsed_date = datetime.strptime(input_date_string, input_format)
  # Convert the parsed date to the desired output format
  output_date_string = parsed_date.strftime(output_format)
  return(output_date_string)
#----------------------------------------------------------------------------------------------------
# FUNCION FOR ADDING "ORIGINAL_DATE_TIME" IN METAFILES // PICTURES//
def picture_modification(date,img_path,route2):
  # Open the image
  img = Image.open(img_path)
  # Create EXIF metadata
  exif_dict = {"Exif": {piexif.ExifIFD.DateTimeOriginal: date,}}
  # Convert EXIF metadata to bytes
  exif_bytes = piexif.dump(exif_dict)
  # Add EXIF metadata to the image
  img_with_exif = img.copy()
  img_with_exif.save(route2, exif=exif_bytes)
#----------------------------------------------------------------------------------------------------
# FUNCION FOR ADDING "ORIGINAL_DATE_TIME" IN METAFILES // VIDEOS (MP4)//
def video_modification(datum,ruta):
    file_path = ruta   # Full path to the file
    file = MP4(file_path)   # Open the MP4 file for editing
    file['©day'] = datum  # Set the album
    file.pprint()
    file.save()

# FUNCTUION FOR COPYING (ADDING IN FOLDER) MODIFIED MP4 FILES
def video_copy(file_path, output_folder):
    # Create a path to save the copied video in another folder
    output_path = os.path.join(output_folder, os.path.basename(file_path))
    # Copy the file
    shutil.copy(file_path, output_path)
#----------------------------------------------------------------------------------------------------

# SELECTING ROOT DIR
rootDir = filedialog.askdirectory()

# HERE, THE NUMBER OF SUBDIRECTORIES IN THE MAIN DIRECTORY IS BEING COUNTED AND STORED IN THE "M" VARIABLE, WHICH IS USED FOR ITERATING THE MAIN LOOP. ;; LOOP FOR COUNTING DIRS WITH PHOTOS
file_count = 0
file_count2=0
for root, dirs, files in os.walk(rootDir):
    for dir in dirs:
        file_count += 1
        file_count2 +=1

if (file_count) == 0:
    file_count =1

# SELECTING WRITING DIR
main_writing_dir = filedialog.askdirectory()

# MAIN LOOP
for n in range(file_count):
    # IF ONLY ONE DIRECTORY WITH PHOTOS IS CHOSEN
   if (file_count2) == 0:
       file_path = rootDir
       for root, dirs, files in os.walk(file_path):
           for file in files:
               # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
               # FOR ALL FILES THAT ARE NOT .JPEG ;;
               if (file[-5:]) != '.jpeg':
                   fileP = file
                   fileJson = file + '.json'
                   # FINDING AND PRINTING THE CREATION TIME OF PHOTOS FROM .JSON FILES; ALSO PRINTING THE IMAGE NAME AND THE CORRESPONDING .JSON FILE FOUND IN THIS LOOP
                   for root, dirs, files in os.walk(file_path):
                       if (fileJson) in files:
                           file_route = rootDir + f"\\{file}"
                           writing_route = main_writing_dir + f"\\modified.{file}"
                           copying_route = main_writing_dir
                           # CREATING "time_for_write" TAKEN FROM .JSON FILES AND CONVERTING IT INTO A FORMAT TO BE PUT INTO EXIF
                           with open(rootDir + "\\" + fileJson) as f:
                               data = json.load(f)
                           time = data["photoTakenTime"]["formatted"]
                           time_for_write = (parsed_time(time))
                           if (fileP[-4:] != ".mp4"):
                               picture_modification(time_for_write, file_route, writing_route)
                           elif (fileP[-4:] == ".mp4"):
                               video_modification(time_for_write, file_route)  # WRITING DATE IN METADATA
                               video_copy(file_route, copying_route)  # SAVING A COPY TO A FILE WITH OTHER IMAGES
               # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
               # THIS IS ONLY FOR .JPEG FILES;; BECAUSE THEY ARE A LITTLE TRICKY
               elif (file[-5:]) == '.jpeg':
                   fileJPEGJ = file[:-5] + '.json'
                   fileJPEGJJ = file + '.json'
                   # FINDING AND PRINTING THE CREATION TIME OF PHOTOS FROM .JSON FILES; ALSO PRINTING THE IMAGE NAME AND THE CORRESPONDING .JSON FILE FOUND IN THIS LOOP; HERE WE HAVE TWO LOOPS BECAUSE .JSON.JPEG FILES CAN SOMETIMES BE ALONE OR WITH .JSON
                   for root, dirs, files in os.walk(file_path):
                       # IF THERE IS .JPEG AND .JSON IN ONE ;;
                       if (fileJPEGJ) in files:
                           # CREATING "time_for_write" TAKEN FROM .JSON FILES AND CONVERTING IT INTO A FORMAT TO BE PUT INTO EXIF
                           file_route= rootDir + f"\\{file}"
                           writing_route = main_writing_dir + f"\\modified.{file}"
                           with open(rootDir + "\\" + fileJPEGJ) as f:
                               data = json.load(f)
                           time = data["photoTakenTime"]["formatted"]
                           time_for_write = (parsed_time(time))
                           picture_modification(time_for_write, file_route, writing_route)
                       # IF THERE IS ONLY .JSON ;;
                       elif (fileJPEGJJ) in files:
                           file_route= rootDir + f"\\{file}"
                           writing_route = main_writing_dir + f"\\modified.{file}"
                           with open(rootDir  + "\\" + fileJPEGJJ) as f:
                               data = json.load(f)
                           time = data["photoTakenTime"]["formatted"]
                           time_for_write = (parsed_time(time))
                           picture_modification(time_for_write, file_route, writing_route)
   # IF IS CHOSEN DIRECTORY WITH MORE FOLDERS WITH PICTURES
   elif (file_count) >= 0:
       file_path = rootDir +"\\" + os.listdir(rootDir)[n]
       for root, dirs, files in os.walk(file_path):
           for file in files:
               # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
               # THIS IS FOR ALL FILES THAT ARE NOT .JPEG;;
               if (file[-5:]) != '.jpeg':
                   fileP = file
                   fileJson = file + '.json'
                   # FINDING AND PRINTING THE CREATION TIME OF PHOTOS FROM .JSON FILES; ALSO PRINTING THE IMAGE NAME AND THE CORRESPONDING .JSON FILE FOUND IN THIS LOOP
                   for root, dirs, files in os.walk(file_path):
                       if (fileJson) in files:
                           file_route= rootDir + f"\\{os.listdir(rootDir)[n]}\\{file}"
                           writing_route = main_writing_dir + f"\\modified.{file}"
                           copying_route = main_writing_dir
                           # CREATING "time_for_write" TAKEN FROM .JSON FILES AND CONVERTING IT INTO A FORMAT TO BE PUT INTO EXIF
                           with open(rootDir + "\\" + os.listdir(rootDir)[n] + "\\" + fileJson) as f:
                               data = json.load(f)
                           time = data["photoTakenTime"]["formatted"]
                           time_for_write = (parsed_time(time))
                           if (fileP[-4:] != ".mp4"):
                               picture_modification(time_for_write, file_route, writing_route)
                           elif (fileP[-4:] == ".mp4"):
                               video_modification(time_for_write, file_route)  # WRITING DATE IN METADATA
                               video_copy(file_route, copying_route)  # SAVING A COPY TO A FILE WITH OTHER IMAGES
               # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
               # THIS IS ONLY FOR .JPEG FILES;; BECAUSE THEY ARE A LITTLE TRICKY
               elif (file[-5:]) == '.jpeg':
                   fileJPEGJ = file[:-5] + '.json'
                   fileJPEGJJ = file + '.json'
                   # FINDING AND PRINTING THE CREATION TIME OF PHOTOS FROM .JSON FILES; ALSO PRINTING THE IMAGE NAME AND THE CORRESPONDING .JSON FILE FOUND IN THIS LOOP; HERE WE HAVE TWO LOOPS BECAUSE .JSON.JPEG FILES CAN SOMETIMES BE ALONE OR WITH .JSON
                   for root, dirs, files in os.walk(file_path):
                       #  IF THERE IS .JPEG AND .JSON IN ONE ;;
                       if (fileJPEGJ) in files:
                           # CREATING "time_for_write" TAKEN FROM .JSON FILES AND CONVERTING IT INTO A FORMAT TO BE PUT INTO EXIF
                           file_route= rootDir + f"\\{os.listdir(rootDir)[n]}\\{file}"
                           writing_route = main_writing_dir + f"\\modified.{file}"
                           with open(rootDir + "\\" + os.listdir(rootDir)[n] + "\\" + fileJPEGJ) as f:
                               data = json.load(f)
                           time = data["photoTakenTime"]["formatted"]
                           time_for_write = (parsed_time(time))
                           picture_modification(time_for_write, file_route, writing_route)
                       # IF THERE IS ONLY .JSON ;;
                       elif (fileJPEGJJ) in files:
                           file_route= rootDir + f"\\{os.listdir(rootDir)[n]}\\{file}"
                           writing_route = main_writing_dir + f"\\modified.{file}"
                           with open(rootDir + "\\" + os.listdir(rootDir)[n] + "\\" + fileJPEGJJ) as f:
                               data = json.load(f)
                           time = data["photoTakenTime"]["formatted"]
                           time_for_write = (parsed_time(time))
                           picture_modification(time_for_write, file_route, writing_route)

print("done")















