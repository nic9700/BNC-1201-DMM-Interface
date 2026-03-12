# this script runs the DMM monitor. It reads the configuration from a YAML file, finds the VISA address 
# of the DMM, and then continuously reads voltage from the DMM, plots it in real-time, and logs the 
# data to a CSV file.

if __name__ == "__main__":
    from DMM_monitor import DMMMonitor
    monitor = DMMMonitor(config_file="config.yaml")
    monitor.run()

    # once the run ends, you can use the PlotSaver class to save the final plot of the voltage readings

    from plt_saver import PlotSaver
    saver = PlotSaver(config_file="config.yaml")
    saver.save_plot()




    # this is the main entry point of the script. It creates an instance of the DMMMonitor class, passing 
    # the path to the configuration YAML file. Then it calls the run() method of the monitor, which starts 
    # the continuous reading, plotting, and logging of the DMM data.

    # To stop the script gracefully, you can use a keyboard interrupt (Ctrl+C) in the terminal where 
    # it's running. This will allow the script to exit cleanly and close any open resources.