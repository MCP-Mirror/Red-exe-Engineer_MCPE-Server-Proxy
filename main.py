#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Set the IP here, make sure to incase it with quotes
# Example: "ip": "pbptanarchy.tk"
address = {
    "ip": None,
    "port": "19132" # 19132 is default
}

"""
    proxy.py

    Copyright 2021 Alvarito050506 <donfrutosgomez@gmail.com>
  
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; version 2 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
  
    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA 02110-1301, USA.
  
    Modified by Wallee#834/Red-exe-Engineer
"""

# Imports
import sys
import socket
import threading
from time import sleep

# Define a thread function to get input so the user can properly stop the program
def inputThread():

    # Declare run as a global variable
    global run

    # Assign True to run
    run = True

    # Tell the user to press enter to stop the proxy and use BOLD text to tell the to not stop the program while the proxy is running
    # Doing so will cause the port to be taken up and you will need to restart your device
    input("\nPress enter to stop the proxy\nDo \033[37;40;1mNOT\033[37;40;0m stop the program ")

    # Assing False to run
    run = False

    # Return
    return

# Big brain stuffs
class Proxy:

    # Define an __init__ function to fun the the class is called
    def __init__(self):

        # Set the options
        self.__options = {
            "src_addr": None,
            "src_port": 19132,
            "dst_port": 19133
        };

        # Some threading stuffs I don't understand
        self.__running_lock = threading.Lock();
        self.__running = 0;

    # Define a method to set variables in the class
    def set_option(self, name, value):

        # Checl if name is in the options
        if name in self.__options:

            # Set the name of options to the value provided
            self.__options[name] = value;

        # Else name is not in options
        else:

            # Raise an error
            raise NameError(name);

        # Return the options
        return self.__options;

    # Define a method to get an option
    def get_options(self):

        # Return options
        return self.__options;

    # Define a method to run
    def run(self):

        # IDK what is going on here
        self.__running_lock.acquire();
        self.__running += 1;
        self.__running_lock.release();

        # Set the dst address
        dst_addr = ("0.0.0.0", self.__options["dst_port"]);

        # Try something that may cause an error
        try:

            # Set proc address to the host address? Alvarito sure knows how to make people feel dumb :p
            proc_addr = socket.gethostbyname_ex(self.__options["src_addr"])[2][0]

        # Something went wrong
        except socket.gaierror:

            # Tell the user there was an error
            print("Error: Invalid address.");

            # Return
            return 1;

        # Set src address to proc addess and scr port from options
        src_addr = (proc_addr, self.__options["src_port"]);

        # Set cliend address to None
        client_addr = None;

        # Fancy socket stuffs I don't understand
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);
        self.__socket.bind(dst_addr);
        self.__socket.setblocking(False);

        # Repeat until the global variable run is not True, used to just run forever
        while run:

            # I don't know what this does but it seems important
            self.__running_lock.acquire();
            condition = self.__running < 1;
            self.__running_lock.release();

            # Check if condition is True
            if condition:

                # End Loop
                break;

            # Try something else that may cause an error
            try:

                # Assign data and addrress
                data, addr = self.__socket.recvfrom(4096);

                # Check if addr is equal to scr addr
                if addr == src_addr:

                    # Send some data do the server, I think
                    self.__socket.sendto(data, client_addr);

                # Else addr is not equal to scr addr
                else:

                    # Check if the client addr is None of cliend addr index 0 is equal to addr index 0
                    if client_addr is None or client_addr[0] == addr[0]:

                        # Set the client address to addr
                        client_addr = addr;

                        # Send some data to the server
                        self.__socket.sendto(data, src_addr);

            # An error has occured
            except:

                # No Data Available
                pass

        # Close the socket
        self.__socket.close();

        # Return
        return 0;

    # Define a mothod to stop
    def stop(self):

        # Set some internal variables to some random network stuffs I still don't get
        self.__running_lock.acquire();
        self.__running -= 1;
        self.__running_lock.release();

        # Return
        return 0;

# Check if the IP is None
if address["ip"] == None:

    # Set preset to False
    preset = False

# Else an IP has been provided
else:

    # Set preset to an empty string
    preset = ""

    # Repeat until preset is a bool
    while type(preset) == str:

        # Ask the user if they want to use the preset
        preset = input("Use preset server [Yes/no] ")

        # Chexk if the user said yes
        if preset.lower()[0] == "y":

            # Set presey to True
            preset = True

        # Else the user said no
        else:

            # Set preset to False
            preset = False

# Check if preset is False
if preset == False:

    # Check if thr IP is None
    if address["ip"] == None:

        # Tell the user they don't have a preset and tell them how to set it using ansi text
        print("No preset found: \033[34;40;5mOpen the file to set one\033[37;40;0m")

    # Set addresses to some inputed data
    address = {
        "ip": input("\nServer address: "),
        "port": input("Port (leave blank for default): ")
    }

    # Print a blank line
    print("")

    # Check if the port is empty
    if address["port"] == "":
        
        # Set the port to 19132 (default)
        address["port"] = "19132"

# Set args to address' vaules
args = [
    address["ip"],
    address["ip"],
    address["port"],
    address["port"]
]

proxy = Proxy();
proxy.set_option("src_addr", args[1]);

if len(args) > 2:
    proxy.set_option("src_port", int(args[2]));

if len(args) > 3:
    proxy.set_option("dst_port", int(args[3]));
    options = proxy.get_options();

print(options["src_addr"] + ":" + str(options["src_port"]) + " --> 0.0.0.0:" + str(options["dst_port"]));

# Assign the inputThread to a variable
wait = threading.Thread(target=inputThread)
wait.start()

try:
    proxy.run();

    # Wait until the input thread changes run to False
    while run == True:
        sleep(1)

    # Stop the proxy
    proxy.stop()

    # Tell the user the proxy has stopped
    input("\nThe proxy has stopped, press enter to return ")

    # Exit the program
    sys.exit(0)

except KeyboardInterrupt:
    proxy.stop();
    print("");
    sys.exit(0);
