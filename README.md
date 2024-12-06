# Wakatime Add-in for Fusion 360
This add-in integrates Wakatime with Autodesk Fusion 360 to help track your design activity. Follow the steps below to install and use the add-in. ATM only tested in Windows, it should work on Mac, not tested.

## How to Use the Wakatime Add-in for Fusion 360

### 1. Download the Code
Download the ZIP file containing the add-in code.

### 2. Extract the Code
Extract the contents of the ZIP file to the following directory on your system:  
`%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\Wakatime for Fusion`  
You can navigate there directly via **File Explorer**.  
The folder structure should look like this:  
`AddIns > Wakatime for Fusion > (files)`

### 3. Install Dependencies

To install the required dependencies, follow these steps:

1. **Navigate to the Production Folder:**
   Open **File Explorer** and go to the following directory:  
   `%LOCALAPPDATA%\Autodesk\webdeploy\production\`

2. **Locate the Python Folder:**
   Inside the `production` folder, you'll find several subfolders. Look for the one containing a folder named `Python`. You can sort the folders by date to find the most recent one. The folder name will look like a random string of characters (e.g., `bce2902bbfcb27678033cbb9e17a3529631b97a7`).

3. **Get the Folder Path:**
   Once you find the correct folder, copy the random string from the folder path. For example, if your path is:  
   `C:\Users\<user>\AppData\Local\Autodesk\webdeploy\production\bce2902bbfcb27678033cbb9e17a3529631b97a7\Python`

   The random string would be something like:  
   `bce2902bbfcb27678033cbb9e17a3529631b97a7`

4. **Install the Requests Library:**
   Open **Windows PowerShell** and run the following command (replace `<RGS>` with the random string you copied):
   ` & "$($env:LOCALAPPDATA)\Autodesk\webdeploy\production\<RGS>\Python\python.exe" -m pip install requests ` 

### 4. Launch Fusion 360
Open Autodesk **Fusion 360**.

### 5. Run the Add-in
Press `Shift + S` to open the **Scripts and Add-ins** menu in Fusion 360.  
In the menu, go to the **Add-ins** tab.  
You should see **Wakatime for Fusion** listed there.  
Check mark the **Run on Start**
Click on **Run**.

### 6. Verify the Add-in is Running
After running the add-in, you should see a popup message that says:  
**"WakaTime tracking started!"**  
If you see a different message or encounter an issue, please contact **@Kunshpreet** on Slack for support.

### 7. Ensure Hackatime is Installed
**IMPORTANT:** Please make sure you have **Hackatime** already installed via the script option.  
If you haven't done so, you will need to install Hackatime first to ensure proper functionality of the add-in.

## Troubleshooting
If you encounter any issues during the installation or while using the add-in, check the following:
- Ensure that **Fusion 360** is running with administrator privileges.
- Verify that you have **Hackatime** installed before running the Wakatime add-in.
- If the add-in doesn't work as expected, please reach out on Slack and provide details of the issue.
