# Parser Swagger's json to burp's Site Map
## Discription:
This script is used as an extension for BurpSuite. It downloads the json from the provided link and prepares the data for the BurpSuite format that will be used to create the Site Map.

## Instructions for use:
The file to be loaded into BurpSuite is called - **api_to_burp.py**

You should also use the file - **jython-standalone-2.7.3.jar** as a **Python environment** (BurpSuit -> Extensions -> Options) which is in the folder named "resources".

It is very **important** that the two folders named **"bin"** and **"Lib/site-packages"** remain next to jython-standalone-2.7.3.jar, as they contain additional libraries needed for the script.
