# this file saves the plot of the DMM voltage readings from the DMM_monitor.py script once the run ends.
#  It uses the same configuration YAML file to determine the plot window size and the IDN substring for
#  finding the VISA address of the DMM. The plot is saved as a PNG file with a timestamp in the filename.

# import necessary libraries
import os
import pyvisa
import matplotlib.pyplot as plt
from VISA_address_finder import VISAAddressFinder
import yaml
from datetime import datetime

class PlotSaver:
    def __init__(self, config_file="config.yaml"):
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

    def save_plot(self, fig=None, times=None, voltages=None, filename=None):
        """Save a matplotlib figure or a set of data points.

        Either provide an existing ``fig`` object (e.g. from the live plot in
        ``DMMMonitor``) or supply ``times``/``voltages`` sequences and the
        method will create a new figure from them.  An optional ``filename``
        may be passed; otherwise a timestamped PNG name is generated.
        """
        if fig is None:
            # build a simple plot from numeric data
            fig, ax = plt.subplots()
            if times is not None and voltages is not None:
                ax.plot(times, voltages, '-o')
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Voltage (V)")
            ax.set_title("BNC 1201 Voltage Reading")
        else:
            ax = fig.axes[0] if fig.axes else None

        if filename is None:
            filename = f"dmm_voltage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        # make sure directory exists if user provided one
        dirname = os.path.dirname(filename)
        if dirname and not os.path.isdir(dirname):
            os.makedirs(dirname, exist_ok=True)
        fig.savefig(filename)
        print(f"Plot saved as {filename}")
