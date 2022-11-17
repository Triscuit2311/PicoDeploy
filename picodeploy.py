# Dante Trisciuzzi 2022
#
## platformio.ini defines, use pico enviroment ##
# extra_scripts = picodeploy.py
# device_drive_letter = E # Change to whatever default drive you're development board is on
# bootload_verify_tries = 10

Import("env")

from concurrent.futures import thread
import os
from time import sleep
from platformio.builder.tools.pioupload import AutodetectUploadPort
import serial
import shutil

drive_letter = env.GetProjectOption("device_drive_letter")
device_volume_path = os.path.join(F"{drive_letter}:")

def is_device_in_bootload() -> bool:
    global device_volume_path
    if os.path.exists(device_volume_path):
        return True
    return False


def force_reset_cb(*args, **kwargs) -> None:

    if is_device_in_bootload():
        print("Device already in bootloader mode.")
        return
        
    AutodetectUploadPort(env)
    force_port = env.subst('$UPLOAD_PORT')

    print(F"Trying force bootloader mode on device at port [{force_port}]")
    ser = serial.Serial(force_port,1200)
    ser.close()

    print(F"Port [{force_port}] reset triggered, verifying bootloader")
    tries = int(env.GetProjectOption("bootload_verify_tries"))
    while not is_device_in_bootload():
        if tries <= 0:
            raise Exception("Device not entering bootloader mode on reset.")
        tries -= 1
        sleep(1)

def load_firmware() -> None:
    print("Loading Firmware..")

    firmware_path = env.subst("$BUILD_DIR\${PROGNAME}.uf2")

    if not os.path.exists(firmware_path):
        print(F"\033[93m> Firmware not found at [{firmware_path}]")
        return False

    global device_volume_path
    
    print("Waiting for device to connect")
    # TODO: Actually check device instead of static delay
    sleep(3000)

    if not is_device_in_bootload():
        print(F"\033[93m> Device not located at [{device_volume_path}]")
        return False

    shutil.copy(firmware_path,device_volume_path)
    return True


def run_loader_cb(*args, **kwargs) -> None:
    if load_firmware():
        print("\033[92m> Firmware Loaded successfully.")
    else:
        print("\033[91m> Firmware Not Loaded.")


env.AddCustomTarget(
    name="deploy",
    dependencies=None,
    actions=[
        "pio run",
        force_reset_cb,
        run_loader_cb
    ],
    title="Build/Deploy",
    description="Build, manually reset RP2040 to BL mode, upload firmware."
)


env.AddCustomTarget(
    name="deployonly",
    dependencies="$BUILD_DIR\${PROGNAME}.uf2",
    actions=[
        force_reset_cb,
        run_loader_cb
    ],
    title="Deploy Only",
    description="Manually reset RP2040 to BL mode, upload firmware."
)
