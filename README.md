
run usb_test.py to collect data

to run usb_test.py:
  mpremote connect /dev/ttyACM0 run usb_test.py | tee battery{i}_test.txt
where i = # of battery being tested
