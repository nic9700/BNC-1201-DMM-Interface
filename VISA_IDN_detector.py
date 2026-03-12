# This script detects and lists all VISA instruments connected to the system, and attempts to query 
# their identification string (IDN). It uses the PyVISA library to interface with the VISA resources.

# Make sure to install the PyVISA library and have the appropriate VISA backend (like NI-VISA) 
# installed on your system.
import pyvisa

# Initialize the VISA resource manager
rm = pyvisa.ResourceManager()

# List all available VISA resources
resources = rm.list_resources()

print("Detected VISA resources:\n")

if len(resources) == 0:
    print("No VISA instruments found.")

# Iterate through each detected resource and attempt to query its IDN string
for r in resources:

    print("Testing:", r)

    try:
        inst = rm.open_resource(r) # Open the VISA resource
        inst.timeout = 2000.       # Set a timeout for the query (in milliseconds)

        idn = inst.query("*IDN?")  # Query the instrument for its identification string
        print("  IDN:", idn.strip())

    except Exception as e:
        print("  Could not query:", e)

    print()