import configparser
import sys
import shutil
import csv
import os
import subprocess

if __name__ == "__main__":
    # Parse command line arguments
    _, projectPath, ssid, wifiPassword, hostAddress, hostSecret = sys.argv

    # Copy project to working directory, making a backup.
    try:
        os.mkdir("./PIO")
    except FileExistsError:
        pass

    shutil.rmtree("./PIO", ignore_errors=True)

    try:
        shutil.copytree(projectPath,"./PIO", dirs_exist_ok=True)
    except shutil.Error:
        # Most likely it couldn't copy read only git files.
        pass

    # CSV layout:
    # DeviceName, DeviceIP, CurrentOTAPasswod, NewOTAPassword, DOOR/INTERLOCK, RF125PS_READER/OLD_READER, RGBW/GRBW, N_LEDS, SKELETON_CARD

    # Parse csv file
    csvEntries = []
    with open("devices.csv", "r") as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        for row in reader:
            csvEntries.append(row)

    # Strip spaces
    csvEntries = [[entry.strip() for entry in row] for row in csvEntries]

    # Parse Platformio.ini
    platformIOConfig = configparser.ConfigParser()
    platformIOConfig.read("./PIO/platformio.ini")
    originalBuildFlags = platformIOConfig["env:ota"]["build_flags"]
    originalBuildFlags = originalBuildFlags.rstrip("\n") + "\n" # Ensure proper newline

    # Compile and upload firmware using PIO
    resultsSummary = []
    for device in csvEntries:
        print(f"Working on {device[0]}")

        print(device)

        # Make build flags
        buildFlags= originalBuildFlags + \
                    f"-DWIFI_PASSWORD=\"{wifiPassword}\"\n" + \
                    f"-DWIFI_SSID=\"{ssid}\"\n" + \
                    f"-DHOST_SECRET=\"{hostSecret}\"\n" + \
                    f"-DHOST_ADDRESS=\"{hostAddress}\"\n" + \
                    f"-DDEVICE_NAME=\"{device[0]}\"\n" + \
                    f"-DOTA_PASSWORD=\"{device[3]}\"\n" + \
                    f"-DSKELETON_CARD={device[8]}\n" + \
                    f"-DN_LEDS={device[7]}\n" + \
                    f"-D{device[4]}\n" + \
                    f"-D{device[5]}\n" + \
                    f"-D{device[6]}\n"

        print(buildFlags)

        # Edit platformio.ini
        platformIOConfig["env:ota"]["upload_port"] = device[1]
        platformIOConfig["env:ota"]["upload_flags"] = f"\n--port=8266\n--auth={str(device[2])}"
        platformIOConfig["env:ota"]["build_flags"] = buildFlags
        with open("./PIO/platformio.ini", "w") as platformIOConfigFile:
            platformIOConfig.write(platformIOConfigFile)

        # PIO run
        exitCode = subprocess.call(["pio", "run", "-t", "upload", "-d", "./PIO", "-e", "ota"])
        endc = '\033[0m'
        if exitCode == 0:
            color = '\033[92m'
            resultsSummary.append(f"{device[0]}{color} SUCCESS{endc}")
        else:
            color = '\033[91m'
            resultsSummary.append(f"{device[0]}{color} FAIL{endc}")

    # Display summary.
    print("\nSummary:\n")
    for result in resultsSummary:
        print(result)