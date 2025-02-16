#!/usr/bin/python3
from processing import *
from analysis import pa_score_from_video_file
from pattern_info import PatternInfo
from record import record_pattern
from pa_result import PaResult
from pa import *
from constants import *

import klipper.gcode as g

import tempfile
from pprint import pprint



def generate_pa_results_for_pattern(pattern_info: PatternInfo)-> list[PaResult]:
    results = []

    # Hardcoding a buffer distance of 3mm here for now.  Adjust if needed.
    with tempfile.TemporaryDirectory("pa_videos") as dir:
        video_files = record_pattern(pattern_info, 4, dir)

        for video_file in video_files:
            results.append(
                pa_score_from_video_file(video_file)
            )
    return results


def main():  
    calibration_pattern = PatternInfo(
        PA_START_VALUE, PA_STOP_VALUE,
        PATTERN_START[0], PATTERN_START[1],
        NUM_LINES,
        PATTERN_WIDTH, PATTERN_SPACING
    )
    g.send_gcode("RESPOND TYPE=command MSG='Running Rubedo Pressure Advance Calibration:'")
    g.send_gcode(f"RESPOND TYPE=command MSG='Testing Range: {PA_START_VALUE} to {PA_STOP_VALUE}'")
    g.send_gcode(f"RESPOND TYPE=command MSG='Validating Results: {VALIDATE_RESULTS}'")
    g.send_gcode(f"RESPOND TYPE=command MSG='Standalone: {STANDALONE}'")
    
    if STANDALONE:
        g.send_gcode("RESPOND TYPE=command MSG='Executing START_PRINT Gcode'")
        g.send_gcode(PRINT_START)
    g.send_gcode("RESPOND TYPE=command MSG='Executing START_PRINT Gcode'")
    g.send_gcode(generate_pa_tune_gcode(calibration_pattern))
    g.wait_until_printer_at_location(FINISHED_X, FINISHED_Y)
    if STANDALONE and not VALIDATE_RESULTS:
        g.send_gcode(f"M104 S{HOTEND_IDLE_TEMP}; let the hotend cool")

    results = generate_pa_results_for_pattern(calibration_pattern)
        
    sorted_results = list(sorted(zip(results, calibration_pattern.pa_values), key=lambda x: x[0].score))
    sorted_results = list([(x.score, y) for x, y in sorted_results])

    best_pa_value = sorted_results[0][1]
    print()
    pprint(sorted_results)
    print()
    print(f"Recommended PA Value: {best_pa_value}, with a score of {sorted_results[0][0]}")
    print()
    g.send_gcode(f"RESPOND TYPE=command MSG='{sorted_results}'")
    g.send_gcode(f"RESPOND TYPE=command MSG='Recommended PA Value: {best_pa_value}, with a score of {sorted_results[0][0]}'")

    g.send_gcode(f"SET_PRESSURE_ADVANCE ADVANCE={best_pa_value}")

    if not VALIDATE_RESULTS:
        g.send_gcode("MMU_END")
        g.send_gcode("END_PRINT")
        return

    control = PatternInfo(
        0, 0,
        PATTERN_START[0] + PATTERN_WIDTH + PATTERN_SPACING + BOUNDING_BOX_LINE_WIDTH*4, PATTERN_START[1],
        NUM_LINES,
        PATTERN_WIDTH, PATTERN_SPACING
    )

    calibrated = PatternInfo(
        best_pa_value, best_pa_value,
        PATTERN_START[0] + PATTERN_WIDTH*2 + PATTERN_SPACING*2 + BOUNDING_BOX_LINE_WIDTH*8, PATTERN_START[1],
        NUM_LINES,
        PATTERN_WIDTH, PATTERN_SPACING
    )


    gcode = f"""
    M109 S{HOTEND_TEMPERATURE};
    BLOBIFIER_CLEAN
    """
    gcode += generate_pa_tune_gcode(control, False)
    gcode += generate_pa_tune_gcode(calibrated)
    g.send_gcode(gcode)
    if STANDALONE:
        g.send_gcode(f"M104 S{HOTEND_IDLE_TEMP}; let the hotend cool")
    g.wait_until_printer_at_location(FINISHED_X, FINISHED_Y)

    control_results = generate_pa_results_for_pattern(control)
    calibrated_results = generate_pa_results_for_pattern(calibrated)

    control_scores = list([x.score for x in control_results])
    calibrated_scores = list([x.score for x in calibrated_results])

    control_average = np.average(control_scores)
    calibrated_average = np.average(calibrated_scores)

    print("Control")
    pprint(control_scores)
    print("Calibrated")
    pprint(calibrated_scores)
    print()
    print(f"Average Control Score: {control_average}")
    print(f"Average Calibrated Score: {calibrated_average}")
    print()
    g.send_gcode(f"RESPOND TYPE=command MSG='Control:{control_scores} Calibrated:{calibrated_scores}'")
    g.send_gcode(f"RESPOND TYPE=command MSG='Average Control Score:{control_average} Average Calibrated Score:{calibrated_average}'")
    g.send_gcode("MMU_END")
    g.send_gcode("END_PRINT")
    
if __name__=="__main__":
    main()
