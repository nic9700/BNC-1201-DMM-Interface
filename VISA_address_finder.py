# this script will find the VISA address of a USB instrument.
#
# The VISAAddressFinder class can be used to search for a VISA resource by matching a substring in 
# the instrument's IDN string. The find_address() method will return the first 
# matching VISA resource name, or None if no match is found.
#
#  - pass ``idn_substr`` to open each resource and query ``*IDN?``
#
# Example: you can call
#
#   finder = VISAAddressFinder(idn_substr="MyDMM")
#
# and then ``finder.find_address()`` will return the first matching
# resource name (or ``None`` if nothing was found).

import pyvisa


class VISAAddressFinder:
    def __init__(self, idn_substr=None, timeout=2000):
        """Create a finder.

        This works by opening each resource and
        querying ``*IDN?`` to see if the returned string contains the
        provided substring.

        Args:
            idn_substr (str or None): substring to look for in the
                instrument identity string (returned by ``*IDN?``).
            timeout (int): VISA timeout (ms) to use when talking to
                devices during the IDN search.
        """

        self.idn_substr = idn_substr
        self.timeout = timeout
        self.rm = pyvisa.ResourceManager()

    def find_address(self):
        """Return the first matching VISA resource or ``None``.

        If an ``idn_substr`` was given we attempt to open
        each candidate and query ``*IDN?``.
        """
        resources = self.rm.list_resources()
        
        # IDN search
        if self.idn_substr is not None:
            for resource in resources:
                try:
                    instr = self.rm.open_resource(resource)
                    instr.timeout = self.timeout
                    idn = instr.query("*IDN?")
                    if self.idn_substr in idn:
                        instr.close()
                        return resource
                    instr.close()
                except Exception:
                    # ignore any resource we can't talk to
                    continue

        return None

