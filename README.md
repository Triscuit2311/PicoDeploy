# RPiPicoPIODeployScript

Script for PlatformIO that adds two new build targets for Raspberry Pi Pico. This adds a Build/Deploy and the Deploy only target. We take advantage of the Pi Pico's 1200 Baud reset functionality to move the board into bootloader mode without needing to use the hard reset, or unplug/re-plug. Because of issues with the standard `raspberrypi-swd` loading method (where the loader will not force bootloader mode and/or fail to transfer the built UF2), the standard PlatformIO upload target will fail to upload the built binary. I am unsure if the problem lies in the build target setup, picotool, or elsewhere. While I work to find the root cause of this issue (which I believe to be a timing issue), this script has been a great interim help to me. This allows the programmer to just use the deploy target, which will build, force bootloader mode, copy the new firmware, then reset the Pi Pico to run the new firmware. Without the need to manually reset the device, the development flow is much simpler and user-friendly.

#
## Setup
1. You'll need to add the following three items to your `platformio.ini` file under the `pico` enviroment:
    ```py
    extra_scripts = picodeploy.py
    device_drive_letter = E # Change to whatever default drive you're development board is on
    bootload_verify_tries = 10
    ```
2. Copy over the `picodeploy.py` script into the same directory your platformio.ini file is in.
3. Build the project with `pio run`.

**NOTE:** *If using the VSCode integration, you may need to restart VSCode for the target to show up in the PIO Project Tasks*

#
## Using the new targets
You will now be able to use the two new build targets from the command line; or iF using VSCode, you can run the from the PIO Project Tasks where you'll find the new targets under the **CUSTOM** tab.

### Command Line:
Build + Deploy
```ps
> pio run -t deploy
```
Deploy Only
```ps
> pio run -t deployonly
```

### PlatformIO VSCode Integration:
![PIO-VSCODE](/piovscode.PNG "VSCode Integration")

