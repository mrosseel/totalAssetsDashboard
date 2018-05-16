Gather current prices for a variety of assets and display them as one aggregate dollar/euro value

TODO:
- add main method + accept parameters to point to other asset file + change eur/usd?
- generate html file which shows the number

TIPS:
flash micropython using esptool:
esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART write_flash -z 0x1000 ~/Downloads/esp32-20171001-v1.9.2-274-g59ab4a22.bin

do stuff on esp32:
rshell --buffer-size=30 -p /dev/tty.SLAB_USBtoUART --wait 10
