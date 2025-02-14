import sys
# Connection details for communicating with the printer's moonraker API.
HOST = '127.0.0.1'
WS_PORT = 7125

# This will print a calibrated + control pattern and measure the % improvement after tuning
VALIDATE_RESULTS = False 


#   ██████╗ ██████╗ ██╗███╗   ██╗████████╗
#   ██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝
#   ██████╔╝██████╔╝██║██╔██╗ ██║   ██║   
#   ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║   
#   ██║     ██║  ██║██║██║ ╚████║   ██║   
#   ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝  
#████████████████████████████████████████████

#Default Bed Temperature: Set this on runtime with BED_TEMP=
BUILD_PLATE_TEMPERATURE = 110
#Default Hotend Temperature: Set this on runtime with NOZZLE_TEMP=       
HOTEND_TEMPERATURE = 250
# The temperature to set the hotend to when the print is finished.            
HOTEND_IDLE_TEMP = 200              
# The tool to use for the print. Set this on runtime with TOOL=
TOOL = 0
# The X and Y coordinates to move to after the print is finished. Slicer can set this with FINISHED_X= and FINISHED_Y=
FINISHED_X = 80                     
FINISHED_Y = 350
# Default diameter of the nozzle in mm. Set this on runtime with NOZZLE_DIAMETER=
NOZZLE_DIAMETER = 0.6
SPEED = 150
ACCELERATION = 3000
MULTIPLIER = 1
Z_HOP_HEIGHT = 0.75
LAYER_HEIGHT = 0.25
RETRACTION_DISTANCE = 0.25
BOUNDING_BOX_LINE_WIDTH = NOZZLE_DIAMETER # May need adjustment. 
PA_START_VALUE = 0
PA_STOP_VALUE = 0.06
AREA_START = (30, 30)
AREA_END = (320, 180)
STANDALONE = True #TODO: Implement this
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
# These are the values that are passed in from the command line. If they aren't set, the defaults above are used.



#    ██████╗ █████╗ ███╗   ███╗███████╗██████╗  █████╗     
#   ██╔════╝██╔══██╗████╗ ████║██╔════╝██╔══██╗██╔══██╗    
#   ██║     ███████║██╔████╔██║█████╗  ██████╔╝███████║   
#   ██║     ██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║    
#   ╚██████╗██║  ██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║    
#    ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   
#██████████████████████████████████████████████████████████
# 
#  Information about the USB camera mounted to the hotend.
VIDEO_DEVICE = "/dev/video2"
VIDEO_WIDTH = "1920"
VIDEO_HEIGHT = "1080"
FRAMERATE = "30"
# The camera's distance from the nozzle.
# This tells the recording code how to center the line within the camera's field of view.
# The offsets are in mm.
CAMERA_OFFSET_X = 3
CAMERA_OFFSET_Y = 3
# The height of the laser above the bed. This is used to focus the camera.
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



#   ███████╗██╗   ██╗███████╗    █████╗ ██████╗  ██████╗ ███████╗
#   ██╔════╝╚██╗ ██╔╝██╔════╝   ██╔══██╗██╔══██╗██╔════╝ ██╔════╝
#   ███████╗ ╚████╔╝ ███████╗   ███████║██████╔╝██║  ███╗███████╗
#   ╚════██║  ╚██╔╝  ╚════██║   ██╔══██║██╔══██╗██║   ██║╚════██║
#   ███████║   ██║   ███████║██╗██║  ██║██║  ██║╚██████╔╝███████║
#   ╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
#██████████████████████████████████████████████████████████████████████

# These are the values that are passed in from the command line. If they aren't set, the defaults above are used.
for arg in sys.argv:
    STANDALONE = False
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
    if arg.startswith('SPEED='):
        SPEED = arg.split('=')[1]
        break
    if arg.startswith('Z_HOP_HEIGHT='):
        Z_HOP_HEIGHT = arg.split('=')[1]
        break
    if arg.startswith('LAYER_HEIGHT='):
        LAYER_HEIGHT = arg.split('=')[1]
        break
    if arg.startswith('RETRACTION_DISTANCE='):
        RETRACTION_DISTANCE = arg.split('=')[1]
        break
    if arg.startswith('START='):
        PA_START_VALUE = arg.split('=')[1]
        break
    if arg.startswith('STOP='):
        PA_STOP_VALUE = arg.split('=')[1]
        break
    if arg.startswith('MULTIPLIER='):
        MULTIPLIER = arg.split('=')[1]
        break
    if arg.startswith('VALIDATE='):
        if arg.startswith('T'):
            VALIDATE_RESULTS = True
        elif arg.startswith('t'):
            VALIDATE_RESULTS = True
        break
    
EXTRUSION_DISTANCE_PER_MM = 0.28686875*NOZZLE_DIAMETER*NOZZLE_DIAMETER * MULTIPLIER