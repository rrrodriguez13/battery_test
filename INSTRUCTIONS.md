
1. run usb_test.py to collect data

to run usb_test.py:

mpremote connect /dev/ttyACM0 run usb_test.py | tee battery{i}_out.txt
  
where i = # of battery being tested

2. run battery_summary.py to show table of all battery data and calculations

3. run master_Ah_plotter.py , master_voltage_plotter.py , or master_battery%_plotter.py to see all data plotted

4. run plot_voltage.py or plot_battery%.py (and specify the battery #, e.g. plot_voltage.py 3 to plot battery3 voltage) to plot specific battery
