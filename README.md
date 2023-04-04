# Burp Extension Swagger's JSON parser

## Discription:
Swagger's JSON parser is used as an extension for BurpSuite. It downloads the json from the provided link and prepares the data for the BurpSuite format that will be used to create the Site Map.

## Instructions for use:
The following steps are required to install the application:
1. Download the project: https://github.com/DmytroPetrushenko/Burp_Extension_Swagger_JSON_parser

2. Open BurpSuite, go to **Extensions > Extensions settings > Extensions**, in the **Python environment** section select the file **jython-standalone-2.7.3.jar**. It is located in the folder, named resources, of the loaded project. 
It is very important that the two folders named **"bin"** and **"Lib/site-packages"** remain next to **jython-standalone-2.7.3.jar**, as they contain additional libraries needed for the script. Don’t delete them.

![](/Users/dpetrushenko/Documents/Screenshot 2023-04-03 at 18.07.30.png)

3. Open **BurpSuite**, go to **Extensions > Installed > Add**, in the window that opens in the **Extension details** section select **Python** in the **Extension type** field and in the **Extension file** field select the file **api_to_burp.py**. And push the button > ***Next***.

![](/Users/dpetrushenko/Documents/Screenshot 2023-04-03 at 17.36.06.png)

4. A tab called **Swagger to SiteMap** appears in the upper panel. Click it! Our window looks like this:

![](/Users/dpetrushenko/Documents/Screenshot 2023-04-03 at 18.21.33.png)

5. If you have **a link to a JSON file**, then paste it into the box labeled **"Enter the url of swagger"** and click **Apply**, if you have **a linked file**, then click **UPLOAD** and select your file and click **OPEN**.

6. If **Basic authentication** is used, then fill in the **Login** and **Password** fields.

**Now You can check your Site Map!**
