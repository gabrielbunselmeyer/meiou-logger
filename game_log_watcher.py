import os, re, time

os.chdir(os.path.dirname(__file__))

LINE_HEADER = ":era_statistics_logging::"
GAME_LOG_DIR = "C:\\Users\\Gabriel\\Documents\\Paradox Interactive\\Europa Universalis IV\\logs\\game.log"
SCRIPT_LOG_NAME = "./script_log.txt" 

def follow(file):
    file.seek(0,2)
    while True:
        line = file.readline()

        if LINE_HEADER in line:
            yield line
        else:
            continue

try:
    with open(GAME_LOG_DIR) as game_log_file, open(SCRIPT_LOG_NAME, "a+", newline="") as script_log_file:
        print("Watching game.log.")

        for line in follow(game_log_file):
            print("Writing line to log: ", line)
            script_log_file.write(line)
            script_log_file.flush()

except Exception as e:
    print(e)
    script_log_file.close()
