import sys
# Connection details for communicating with the printer's moonraker API.
HOST = '127.0.0.1'
WS_PORT = 7125

# This will print a calibrated + control pattern and measure the % improvement after tuning
VALIDATE_RESULTS = False

# Print settings
BUILD_PLATE_TEMPERATURE = 110
HOTEND_TEMPERATURE = 250
HOTEND_IDLE_TEMP = 200
TOOL = 0
FINISHED_X = 80
FINISHED_Y = 350
NOZZLE_DIAMETER = 0.6
ACCELERATION = 3000

# These are the values that are passed in from the command line. If they aren't set, the defaults above are used.
for arg in sys.argv:
    if arg.startswith('BED_TEMP='):
        BUILD_PLATE_TEMPERATURE = arg.split('=')[1]
        break
    if arg.startswith('NOZZLE_TEMP='):
        HOTEND_TEMPERATURE = arg.split('=')[1]
        break
    if arg.startswith('VALIDATE='):
        if arg.split('=')[1].startswith('T'):
            VALIDATE_RESULTS = True
        break
    if arg.startswith('TOOL='):
        TOOL = arg.split('=')[1]
        break
    if arg.startswith('FINISHED_X='):
        FINISHED_X = arg.split('=')[1]
        break
    if arg.startswith('FINISHED_Y='):
        FINISHED_Y = arg.split('=')[1]
        break
    if arg.startswith('NOZZLE_DIAMETER='):
        NOZZLE_DIAMETER = arg.split('=')[1]
        break
    if arg.startswith('ACCELERATION='):
        ACCELERATION = arg.split('=')[1]
        break


# The area of the bed that the pattern will be printed in.
AREA_START = (30, 30)
AREA_END = (320, 180)

# Any gcode you want to be sent before the pattern is printed.
# You could just have this call PRINT_START if you've configured
# that for your printer.
PRINT_START = f"""
M104 S{HOTEND_IDLE_TEMP}; preheat nozzle while waiting for build plate to get to temp
M140 S{BUILD_PLATE_TEMPERATURE};
MMU_START_SETUP INITIAL_TOOL={TOOL} 
MMU_START_CHECK;
START_PRINT  EXTRUDER_TEMP={HOTEND_TEMPERATURE} BED_TEMP={BUILD_PLATE_TEMPERATURE}
MMU_START_LOAD_INITIAL_TOOL
START_PRINT_2 AREA_START={AREA_START[0]},{AREA_START[1]} AREA_END={AREA_END[0]},{AREA_END[1]}
SET_PRINT_STATS_INFO TOTAL_LAYER=1
"""

# Information about the USB camera mounted to the hotend.
VIDEO_DEVICE = "/dev/video2"
VIDEO_WIDTH = "1920"
VIDEO_HEIGHT = "1080"
FRAMERATE = "30"
# The camera's distance from the nozzle.
# This tells the recording code how to center the line within the camera's field of view.
# The offsets are in mm.
CAMERA_OFFSET_X = 3
CAMERA_OFFSET_Y = 3

# This is the height where the camera and laser are in focus.
LASER_FOCUS_HEIGHT = 5

# How the processing code finds the area of interest. Units are in pixels.
# The crop offsets specify the pixel that the box should be centered on.
CROP_X_OFFSET = 220
# In my case, the crop Y offset should be zero, but my offset Y value above is slightly off.
# You can kind of tweak these if you find that things aren't quite right.
CROP_Y_OFFSET = 11
# How big the area around the laser should be cropped to.
CROP_FRAME_SIZE_X = 45
CROP_FRAME_SIZE_Y = 60

# Sometimes ffmpeg is slow to close. If we start moving too early, 
# we might accidentally record stuff we don't want to.
# I would like to eliminate these eventually by improving the video recording code.
FFMPEG_START_DELAY = 0.5
FFMPEG_STOP_DELAY = 0.6

# Pressure Advance Pattern Configuration
# This changes how the gcode for the pressure advance pattern is generated.
# Only edit this if you need to.
Z_HOP_HEIGHT = 0.75
LAYER_HEIGHT = 0.25
RETRACTION_DISTANCE = 0.25
EXTRUSION_DISTANCE_PER_MM = 0.28686875*NOZZLE_DIAMETER*NOZZLE_DIAMETER
BOUNDING_BOX_LINE_WIDTH = 0.6 # May need adjustment. 

# TODO: implement support for these.
# If we know the FOV, we can attach actual units
# to the values that are calculated.
# CAMERA_FOV_X = 0
# CAMERA_FOV_Y = 0

# These were used earlier on in development, but I need to re-implement 
# them, as the refactor I did removed the code that made them work.
# OUTPUT_GRAPH = False
# OUTPUT_FRAMES = True
# OUTPUT_HEIGHT_MAPS = False
