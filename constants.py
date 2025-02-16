#General Settings
HOST = '127.0.0.1'  #Moonraker IP. Use 127.0.0.1 if using local machine.
WS_PORT = 7125      #Moonraker Websocket port. Default is 7125.



#   ██████╗  █████╗ ████████╗████████╗███████╗██████╗ ███╗   ██╗
#   ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗████╗  ██║
#   ██████╔╝███████║   ██║      ██║   █████╗  ██████╔╝██╔██╗ ██║
#   ██╔═══╝ ██╔══██║   ██║      ██║   ██╔══╝  ██╔══██╗██║╚██╗██║
#   ██║     ██║  ██║   ██║      ██║   ███████╗██║  ██║██║ ╚████║
#   ╚═╝     ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
#█████████████████████████████████████████████████████████████████


PA_START_VALUE = 0                          # Set at runtime with PA_START=
PA_STOP_VALUE = 0.06                        # Set at runtime with PA_STOP=
PATTERN_START = (30, 30)                    # Set at runtime with PATTERN_START=
PATTERN_SPACING = 10                        # Set at runtime with PATTERN_SPACING=
PATTERN_WIDTH = 30                          # Set at runtime with PATTERN_WIDTH=
NUM_LINES = 10                              # Set at runtime with NUM_LINES=
VALIDATE_RESULTS = False                    # Set at runtime with VALIDATE=


#   ██████╗ ██████╗ ██╗███╗   ██╗████████╗
#   ██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝
#   ██████╔╝██████╔╝██║██╔██╗ ██║   ██║   
#   ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║   
#   ██║     ██║  ██║██║██║ ╚████║   ██║   
#   ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝  
#████████████████████████████████████████████

BUILD_PLATE_TEMPERATURE = 110               # Set at runtime with BED_TEMP=
HOTEND_TEMPERATURE = 250                    # Set at runtime with EXTRUDER_TEMP
HOTEND_IDLE_TEMP = 200              
TOOL = 0                                    # Set at runtime with TOOL=               
FINISHED_X = 80                             # Set at runtime with FINISHED_X=   
FINISHED_Y = 350                            # Set at runtime with FINISHED_Y=
NOZZLE_DIAMETER = 0.6                       # Set at runtime with NOZZLE_DIAMETER=
SPEED = 150                                 # Set at runtime with SPEED=
ACCELERATION = 3000                         # Set at runtime with ACCELERATION=
MULTIPLIER = 1                              # Set at runtime with FLOW=
Z_HOP_HEIGHT = 0.75                         # Set at runtime with HOP=
LAYER_HEIGHT = 0.25                         # Set at runtime with LAYER_HEIGHT=
RETRACTION_DISTANCE = 0.5                  # Set at runtime with RETRACTION_DISTANCE=
BOUNDING_BOX_LINE_WIDTH = NOZZLE_DIAMETER  # May need adjustment. 
STANDALONE = True 

# Calculate the area that the print will cover.
if VALIDATE_RESULTS:
    AREA_END = (PATTERN_START[0] + PATTERN_WIDTH*3 + BOUNDING_BOX_LINE_WIDTH*12, PATTERN_START[1] + NUM_LINES * PATTERN_SPACING + BOUNDING_BOX_LINE_WIDTH*4)
else:
    AREA_END = (PATTERN_START[0] + PATTERN_WIDTH + BOUNDING_BOX_LINE_WIDTH*4, PATTERN_START[1] + NUM_LINES * PATTERN_SPACING + BOUNDING_BOX_LINE_WIDTH*4)


PRINT_START = f"""
M104 S{HOTEND_IDLE_TEMP}; preheat nozzle while waiting for build plate to get to temp
M140 S{BUILD_PLATE_TEMPERATURE};
MMU_START_SETUP INITIAL_TOOL={TOOL} 
MMU_START_CHECK;
START_PRINT  EXTRUDER_TEMP={HOTEND_TEMPERATURE} BED_TEMP={BUILD_PLATE_TEMPERATURE}
MMU_START_LOAD_INITIAL_TOOL
START_PRINT_2 AREA_START={PATTERN_START[0]},{PATTERN_START[1]} AREA_END={AREA_END[0]},{AREA_END[1]}
SET_PRINT_STATS_INFO TOTAL_LAYER=1
"""


#    ██████╗ █████╗ ███╗   ███╗███████╗██████╗  █████╗     
#   ██╔════╝██╔══██╗████╗ ████║██╔════╝██╔══██╗██╔══██╗    
#   ██║     ███████║██╔████╔██║█████╗  ██████╔╝███████║   
#   ██║     ██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║    
#   ╚██████╗██║  ██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║    
#    ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   
#██████████████████████████████████████████████████████████
# 
#  Information about the USB camera mounted to the hotend.
VIDEO_DEVICE = "/dev/v4l/by-id/usb-3DO_3DO_USB_CAMERA_V2_3DO-video-index0"
VIDEO_WIDTH = "1920"
VIDEO_HEIGHT = "1080"
FRAMERATE = "30"
# The camera's distance from the nozzle.
# This tells the recording code how to center the line within the camera's field of view.
# The offsets are in mm.
CAMERA_OFFSET_X = 0
CAMERA_OFFSET_Y = 3
# The height of the laser above the bed. This is used to focus the camera.
LASER_FOCUS_HEIGHT = 8.3 # mm

# How the processing code finds the area of interest. Units are in pixels.
# The crop offsets specify the pixel that the box should be centered on.
CROP_X_OFFSET = 1500
# In my case, the crop Y offset should be zero, but my offset Y value above is slightly off.
# You can kind of tweak these if you find that things aren't quite right.
CROP_Y_OFFSET = 1500
# How big the area around the laser should be cropped to.
CROP_FRAME_SIZE_X = 250
CROP_FRAME_SIZE_Y = 250

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
# Use SAVE=1 to save the values to this file.
import sys
handled_args = set()
save_flag = False
for arg in sys.argv[1:]:
    if arg.startswith('BED_TEMP='):
        BUILD_PLATE_TEMPERATURE = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('EXTRUDER_TEMP='):
        HOTEND_TEMPERATURE = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('VALIDATE='):
        VALIDATE_RESULTS = arg.split('=')[1].lower() in ['true', '1', 't']
        handled_args.add(arg)
    elif arg.startswith('TOOL='):
        TOOL = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('FINISHED_X='):
        FINISHED_X = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('FINISHED_Y='):
        FINISHED_Y = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('NOZZLE_DIAMETER='):
        NOZZLE_DIAMETER = float(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('ACCELERATION='):
        ACCELERATION = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('SPEED='):
        SPEED = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('HOP='):
        Z_HOP_HEIGHT = float(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('LAYER_HEIGHT='):
        LAYER_HEIGHT = float(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('RETRACTION_DISTANCE='):
        RETRACTION_DISTANCE = float(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('START='):
        PA_START_VALUE = float(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('STOP='):
        PA_STOP_VALUE = float(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('FLOW='):
        MULTIPLIER = float(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('SAVE='):
        save_flag = arg.split('=')[1] == '1'
        handled_args.add(arg)
    elif arg.startswith('NUM_LINES='):
        NUM_LINES = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('PATTERN_START='):
        PATTERN_START = tuple(map(int, arg.split('=')[1].split(',')))
        handled_args.add(arg)
    elif arg.startswith('PATTERN_SPACING='):
        PATTERN_SPACING = int(arg.split('=')[1])
        handled_args.add(arg)
    elif arg.startswith('PATTERN_WIDTH='):
        PATTERN_WIDTH = int(arg.split('=')[1])
        handled_args.add(arg)

# Check for unhandled arguments
unhandled_args = set(sys.argv[1:]) - handled_args
if unhandled_args:
    raise ValueError(f"Unhandled command line arguments: {unhandled_args}")

# Write the file if SAVE=1 is present
if save_flag:
    with open(__file__, 'r') as file:
        lines = file.readlines()
    
    with open(__file__, 'w') as file:
        skip = False
        for line in lines:
            if line.strip().startswith('for arg in sys.argv:'):
                skip = True
            if skip and line.strip().startswith('EXTRUSION_DISTANCE_PER_MM ='):
                skip = False
                file.write(line)
                continue
            if not skip:
                if line.startswith('BUILD_PLATE_TEMPERATURE ='):
                    file.write(f'BUILD_PLATE_TEMPERATURE = {BUILD_PLATE_TEMPERATURE}\n')
                elif line.startswith('HOTEND_TEMPERATURE ='):
                    file.write(f'HOTEND_TEMPERATURE = {HOTEND_TEMPERATURE}\n')
                elif line.startswith('VALIDATE_RESULTS ='):
                    file.write(f'VALIDATE_RESULTS = {VALIDATE_RESULTS}\n')
                elif line.startswith('TOOL ='):
                    file.write(f'TOOL = {TOOL}\n')
                elif line.startswith('FINISHED_X ='):
                    file.write(f'FINISHED_X = {FINISHED_X}\n')
                elif line.startswith('FINISHED_Y ='):
                    file.write(f'FINISHED_Y = {FINISHED_Y}\n')
                elif line.startswith('NOZZLE_DIAMETER ='):
                    file.write(f'NOZZLE_DIAMETER = {NOZZLE_DIAMETER}\n')
                elif line.startswith('ACCELERATION ='):
                    file.write(f'ACCELERATION = {ACCELERATION}\n')
                elif line.startswith('SPEED ='):
                    file.write(f'SPEED = {SPEED}\n')
                elif line.startswith('Z_HOP_HEIGHT ='):
                    file.write(f'Z_HOP_HEIGHT = {Z_HOP_HEIGHT}\n')
                elif line.startswith('LAYER_HEIGHT ='):
                    file.write(f'LAYER_HEIGHT = {LAYER_HEIGHT}\n')
                elif line.startswith('RETRACTION_DISTANCE ='):
                    file.write(f'RETRACTION_DISTANCE = {RETRACTION_DISTANCE}\n')
                elif line.startswith('PA_START_VALUE ='):
                    file.write(f'PA_START_VALUE = {PA_START_VALUE}\n')
                elif line.startswith('PA_STOP_VALUE ='):
                    file.write(f'PA_STOP_VALUE = {PA_STOP_VALUE}\n')
                elif line.startswith('MULTIPLIER ='):
                    file.write(f'MULTIPLIER = {MULTIPLIER}\n')
                elif line.startswith('NUM_LINES ='):
                    file.write(f'NUM_LINES = {NUM_LINES}\n')
                elif line.startswith('PATTERN_START ='):
                    file.write(f'PATTERN_START = {PATTERN_START}\n')
                elif line.startswith('PATTERN_SPACING ='):
                    file.write(f'PATTERN_SPACING = {PATTERN_SPACING}\n')
                elif line.startswith('PATTERN_WIDTH ='):
                    file.write(f'PATTERN_WIDTH = {PATTERN_WIDTH}\n')
                else:
                    file.write(line)

# Calculate extrusion distance per mm. Needs to be calculated after the command line arguments are processed.
EXTRUSION_DISTANCE_PER_MM = 0.28686875 * NOZZLE_DIAMETER * NOZZLE_DIAMETER * MULTIPLIER