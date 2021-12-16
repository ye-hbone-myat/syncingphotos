# Syncing Photos

Description
-----------
This project is syncing photos from iPads to Mac and from Mac to Google Drive automically. All the photos in your iPads will be saved in Mac under folder named with photo taken date by using Seafile file service which is running with Docker, Mac Automator and Bash. Those folders in Mac will be synced to Google Drive using python custom program which is running with cronjob.

Requirements
-----------
1. Docker Desktop in Mac
2. Seafile Server and Client
3. Mac Automator
4. Bash
5. Python3

Workflow Diagram
----------------
![alter text](https://github.com/ye-hbone-myat/syncingphotos/blob/cbee168cb7f8f264dc28cc93d23e449bc7dfbb0b/Images/Screen%20Shot%202021-11-28%20at%203.05.23%20AM.png)

Docker Desktop Install Mac
--------------------------
1. Follow this [link](https://hub.docker.com/editions/community/docker-ce-desktop-mac) and download the Docker Desktop and install in Mac.
2. Search Docker Desktop in your machine and start.

Seafile Server install with Docker
---------------------------
1. Download the project repository to you machine.
```console
cd ~/ && git clone https://github.com/ye-hbone-myat/syncingphotos.git
```

2. Create seafile data folder in the downloaded repository folder and this will use as seafile data storage file path in seafile docker compose file.
```console 
mkdir -p ~/syncingphotos/Seafile/seafile-data
```

3. Create seafile mysql folder in the downloaded repository folder and this will use as seafile mysql storage file path in seafile docker compose file.
```console 
mkdir -p ~/syncingphotos/Seafile/seafile-mysql/db
```
4. Go the file directory where seafile docker file exists.
```console
cd ~/syncingphotos/Seafile/
```

5. Deploy the seafile with docker compose.
```console 
docker compose up -d
```

6. Check the docker containers whether they are running or not.
```console 
docker ps
```
( if they are running , you will see the docker containers: seafile, seafile-mysql and seafile-memcached)

7. Type **127.0.0.1** or **localhost** in your browser. After seafile server is up and running, you will able to see the seafile login screen. Use **username** and **password** which are predefined in docker compose file to login seafile server.

8. After login, first create a library for your photos in the Seafile Web UI.

9. Click the account logo in the top-right corner and click the system admin. In the system admin UI, click the setting and you will see the **SERVICE_URL** and **FILE_SERVER_ROOT**. Change your machine IP Address in **SERVICE_URL** and **FILE_SERVER_ROOT**. After that, you will be able to use your ip address as seafile server.

10. Install Seafile Desktop Syncing Client in Mac and Seafile Pro Client in iPad. Follow this [link](https://www.seafile.com/en/download/) for Mac and Follow this [link](https://apps.apple.com/us/app/seafile-pro/id639202512) for iPad.


Configure Seafile Pro Client in iPad
------------------------------------
1. Open Seafile Pro Client

2. Login with your credentials (Server IP Address, Username, Password)

3. Go to setting and turn on camera upload setting. It will provide you step-by-step configuration UI. Choose the library you created and select your camera album. This will allow you to upload automatically your photos from camera album to seafile library.


Configure Seafile Desktop Syncing Client in Mac
-----------------------------------------------
1. Open Seafile Desktop Client

2. Login with your credentials (Server IP Address, Username, Password)

3. Right click on the library you created, click **sync this library** and this will sync your photos to your Mac automatically.

4. After that, check your photos in seafile library and in your mac folder as well. Nextime your new photos will be synced automatically to the mac folder.


Now it's time to setup for automation part. I will use folder action with automator and bash script. When the photos come to the mac folder, the bash script will automatically run using mac automator and orginize the photos under the folder named with photo taken date.

Setup Automator with Bash
-------------------------

**REQUITEMENTS**

1. Home brew (Follow this [link](https://brew.sh) to install.)

2. Exiftool (To grep photo taken date from photo metadata)
```console 
brew install exiftool
```

3. Automator (Mac build-in software)

**STEPS**

1. Open **Automator** in Mac and choose **folder action**.

2. Search **Run Shell Script** in Name and click. Choose folder location path which your photos are stored.

3. Change **pass input** value from **stdin** to as **arguments**

4. Copy the script **seafileDrive.sh** from this repository and put into the **Run Shell Script** box and save with a workflow name. After that, all the photos will organize under photo taken folder accordingly and whenever new photos come in, will organize automatically.

Note: Don't forget to change destination folder directory path in **seafileDrive.sh** script.

Setup Google Drive Syncing with Python
--------------------------------------

**REQUIREMENTS**

1. Python3
```console 
brew install python3
```
2. Pip (Folllow this [link](https://phoenixnap.com/kb/install-pip-mac) to install.)

3. Google Authentication Python Libraries   
```console 
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client
```
4. Google Service Account (Follow this [link](https://developers.google.com/identity/protocols/oauth2/service-account) to create and save key json file in your machine.)

Note: If your organization is using Google Admin Workspace, need to authorize in **Domain wide delegation** for your service account. You can check [here](https://developers.google.com/identity/protocols/oauth2/service-account).


**STEPS**

1. Allow **cron** for full disk access in Mac. Check [here](https://blog.bejarano.io/fixing-cron-jobs-in-mojave/).

2. Change **Service Account Key Json file path** according to your key file location and modify **parentID** to upload as you want in python code. (parentID is the ID number of the folder from Google Drive you want to upload). [Get Folder ID](https://ploi.io/documentation/database/where-do-i-get-google-drive-folder-id)

3. Share the folder of your Google Drive to the service account because we will sync files from the background using service account.

Note: You can use Google Drive normal Oauth API authentication instead of service account. But if you do, you need through browser with the auth link everytime you run the script. I want to run the script in the background. So service account is the best choice for me.) 

4. Setup Python Script As Cron Job. I will setup a cronjob which wil be running every 30 min. That means your local folder from Mac and Google Drive Folder will be syncing every 30 min.

  Enter to cron editor. You can change text editor as you wish.
  ```console
  EDITOR=nano crontab -e
  ```
  Input the follow command in the cron editor.
  ```console
  */30 * * * * /path/to/python3 ~/syncingphotos/pythonDrive.py /path/to/SyncFolder
  ```
  Save and Exit from editor and your cronjob will be installed.

So, the python google drive syncing script will be running every 30 minutes.

Manual Importing Photos from iPads to iMac
--------------------------

1. Connect your iPad to iMac with USB-C cable.
2. Go to Photos.
3. Go to your iPad tab.
4. Select all new photos.
5. Copy those photos to Seafile Photo Folder.

Manual Syncing Photos from iMac to Google Drive with Python
----------------------

1. Open terminal
2. Run the following command.
```console
python3 ~/syncingphotos/pythonDrive.py /path/to/GoogleDriveSync/
```
It will sync your all new photos to the Google Drive.


