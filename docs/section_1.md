# Overview
This documentation covers everything related to creating, setting up and programming a server for OnlineClicker. I recommend going through all sections from beginning to end.

The server is programmed in Python. All libraries used can be found in the `requirements.txt` file.

The server also requires a Discord bot for account creating, which is included in the module and can be run along with the server.

**If you don't know how to program in Python (or any language), that's fine! Read all sections to the end except programming! These sections assume that you have no programming experience.**

Configuration steps (like installing Python or Python libraries) aren't listed for Linux users, as it's assumed that you have more experience with this stuff. However, the steps are very similar, so feel free to follow the Windows guide!

I can't help you with Mac because I don't have experience with it. If you would like to add your suggestion for Mac steps, feel free to contact me!

## Need help? Want to suggest something?
You can contact me on Discord if you need any help, want to suggest something or just anything else. I don't bite! :D

# Creating the server
## Installing Python
Before you download the server, you need to install the Python interpreter. Without it, the server cannot run.

To install Python (Windows):
1. Go to https://python.org.
2. Click on "Downloads".
3. Click on "Download Python".
4. Open the installation .exe file.
5. **Check "Add python.exe to PATH"!**
6. Click on "Install Now" and close the window.

## Verify installation
Type `cmd` in the search bar. This will open a command prompt. Type `python --version` in the terminal and it should list the version of Python you downloaded.

## Downloading the server
Now that you have Python installed, you can download the server files! You can download the latest version of the server by going to the [GitHub page of OnlineClicker](https://github.com/glitchedlime/onlineclicker), clicking the green "Code" button and downloading the ZIP file.

Don't forget to extract the ZIP file after downloading it!

## Installing Python libraries
Server scripts require certain Python libraries that are necessary for the server to function (e.g. communication with players).

To install all the libraries (Windows):
1. Open your server folder and find `requirements.txt` file.
2. In the file explorer window, type `cmd` in the path bar (next to the search bar) and press ENTER. This will open a command prompt.
3. In the command prompt, type `pip install -r requirements.txt`. This will install all libraries needed for the server to run.
4. Close the command prompt.

## Renaming example files
You will find example files when you download the server (like "server.example.py"). Just remove ".example" from all these files. Make sure to check all folders!

## Configuring the server
Your server itself should be fully functional, but it's not ready yet. You can set it up and customize it!

You should look at and edit all files in the `config/` folder.

The `config.ini` file sets basic server properties, such as name, port, admins, etc. The `.env` file sets values ​​that should only be private, such as the database password (if MySQL) and the Discord bot token.

All the values ​​you can edit are already in the files and you can overwrite them. However, some files have comments that tell you how to write the values. **Please read them!**

## Running the server
On Windows, you can execute the script by double-clicking the `start.bat` file.
On Linux, you can execute the script by opening the terminal in the server directory and typing `bash ./start.sh`.

