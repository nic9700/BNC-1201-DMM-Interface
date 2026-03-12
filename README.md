# README

## Preface
This document was made for the purpose of recording voltage measurements from digital multimeters and other VISA devices.  It uses NI-VISA to connect the computer and the instrument.  You may have to download other packages and libraries based on your operating system.

## Instructions
Use the VISA_IDN_detector to find the IDN strip of the device you want to pull data from.  Copy part of the strip (a substring) and paste it into the "idn_substr" part of the config file.  You can now run main to view a live plot of the measured voltage, and the script will simultaneously write a CSV with timestamps, the time since the run began, and the measured voltage.  You can comment out PlotSaver if you do not wish to also save the plot of the run. 

## How It Works
### VISA_IDN_detector
This file uses NI-VISA to communicate with connected VISA devices to find there IDN strip, and prints the strip so that you may copy and paste a substring of the strip in the config file for the VISAAddressFinder.

### VISA_address_finder
This file creates the class VISAAddressFinder to find the instrument that you want to pull data from and communicate with the instrument.

### DMM_monitor
This file creates the DMMMonitor class which creates a live plot from a VISA instrument found VISAAddressFinder.  It also saves the data as a CSV with timestamps, the time since the run began, and the measured voltage.