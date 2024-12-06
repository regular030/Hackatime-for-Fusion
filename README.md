# Wakatime Add-in for Fusion 360
This add-in integrates Wakatime with Autodesk Fusion 360 to help track your design activity. Follow the steps below to install and use the add-in.

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
Open **Windows PowerShell** and run the following command (ensure the quotation marks are included):  

`& "$($env:LOCALAPPDATA)\Autodesk\webdeploy\production\13b1dce62fc3204647ade625f7b4cb3f8d542a09\Python\python.exe" -m pip install requests`


This will install the necessary dependencies for the add-in to function properly.

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
