# this script runs the DMM monitor. It reads the configuration from a YAML file, finds the VISA address 
# of the DMM, and then continuously reads voltage from the DMM, plots it in real-time, and logs the 
# data to a CSV file.

if __name__ == "__main__":
    from DMM_monitor import DMMMonitor
    from plt_saver import PlotSaver
    saver = PlotSaver(config_file="config.yaml")
    monitor = DMMMonitor(config_file="config.yaml")
    monitor.run()

    # if the user interrupts the script (e.g., by pressing Ctrl+C), we want to save the current plot before exiting.
    if KeyboardInterrupt:
        saver.save_plot(fig=monitor.fig)
        print("Exiting gracefully.")




    # this is the main entry point of the script. It creates an instance of the DMMMonitor class, passing 
    # the path to the configuration YAML file. Then it calls the run() method of the monitor, which starts 
    # the continuous reading, plotting, and logging of the DMM data.

    # To stop the script gracefully, you can use a keyboard interrupt (Ctrl+C) in the terminal where 
    # it's running. This will allow the script to exit cleanly and close any open resources.