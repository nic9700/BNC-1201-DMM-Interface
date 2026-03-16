# This script continuously reads voltage from the BNC 1201 DMM and plots it in real-time. 
# It also logs the data to a CSV file with timestamps. Make sure to install the required 
# libraries (usbtmc, matplotlib) and adjust the vendor/product ID if needed. Run this script 
# in an environment where you have access to the DMM and the necessary permissions. The plot 
# will update every 0.2 seconds, and the data will be saved in a CSV file named with the 
# current date and time.

import os
import pyvisa
import matplotlib.pyplot as plt
import time
import csv
from collections import deque
from datetime import datetime
from VISA_address_finder import VISAAddressFinder
import yaml
import pyvisa
import pytz

class DMMMonitor:
    def __init__(self, config_file="config.yaml"):
        # remember path for later use
        self.config_file = config_file
        # Load configuration from YAML file
        with open(config_file, "r") as f:
            self.config = yaml.safe_load(f)

        self.VISA_ADDRESS = VISAAddressFinder(idn_substr=self.config["idn_substr"]).find_address()
        if self.VISA_ADDRESS is None:
            raise RuntimeError("could not locate DMM – check connection/IDN substring")
        self.rm = pyvisa.ResourceManager()
        self.dmm = self.rm.open_resource(self.VISA_ADDRESS)

        # Configure measurement once
        self.dmm.write("CONF:VOLT:DC")

        # Plot settings
        self.window = self.config.get("plot_window_size", 200)  # Number of points to display in the plot
        self.times = deque(maxlen=self.window)
        self.voltages = deque(maxlen=self.window)

        # logging/plot directory information
        self.log_dir = self.config.get("log_directory", "./")
        self.log_prefix = self.config.get("log_filename_prefix", "dmm_log")
        os.makedirs(self.log_dir, exist_ok=True)

    def run(self):
        plt.ion()
        fig, ax = plt.subplots()
        # # some backends (tkAgg, qt) default to keeping a new figure on top;
        # # try to clear the 'topmost' flag so it behaves like a normal window.
        # try:
        #     mgr = plt.get_current_fig_manager()
        #     # TkAgg
        #     if hasattr(mgr, 'window') and hasattr(mgr.window, 'attributes'):
        #         mgr.window.attributes('-topmost', False)
        #     # Qt backends
        #     if hasattr(mgr, 'window') and hasattr(mgr.window, 'setWindowFlags'):
        #         from matplotlib import QtCore
        #         flags = mgr.window.windowFlags()
        #         mgr.window.setWindowFlags(flags & ~QtCore.Qt.WindowStaysOnTopHint)
        #     # draw manager changes
        #     mgr.canvas.draw()
        # except Exception:
        #     pass

        line, = ax.plot([], []) 

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title("BNC 1201 Live Voltage")

        start = time.time()

        timestamp = datetime.now().strftime(self.config.get("log_filename_timestamp_format", "%Y%m%d_%H%M%S"))
        filename = os.path.join(self.log_dir, f"{self.log_prefix}_{timestamp}.csv")

        # Open the CSV file for writing and log the data in real-time
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "time (s)", "voltage (V)"])

            try:
                while True:
                    t = time.time() - start
                    timestamp = datetime.now().isoformat()
                    timestamp = timestamp.astimezone(pytz.utc)

                    v = float(self.dmm.query("READ?"))

                    writer.writerow([timestamp, t, v])

                    self.times.append(t)
                    self.voltages.append(v)

                    line.set_data(self.times, self.voltages)

                    ax.relim()
                    ax.autoscale_view()

                    plt.draw()
                    plt.pause(self.config["plot_pause_time"])

                    time.sleep(self.config["plot_update_interval"])
            except KeyboardInterrupt:
                # user requested termination; save the final plot
                plt.ioff()
                try:
                    from plt_saver import PlotSaver
                    saver = PlotSaver(config_file=self.config_file)
                    # direct the saver to use the same log directory/prefix
                    saver.save_plot(fig=fig, times=self.times, voltages=self.voltages,
                                    filename=os.path.join(self.log_dir,
                                        f"{self.log_prefix}_{timestamp}.png"))
                except Exception as e:
                    # fallback: just save the figure directly if something goes wrong
                    fallback_name = os.path.join(self.log_dir,
                                        f"{self.log_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    fig.savefig(fallback_name)
                    print(f"(fallback) plot saved as {fallback_name} due to: {e}")
                print("Stopped by user, exiting.")
