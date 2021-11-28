# Syncing Photos

Description
-----------
This project is syncing photos from Ipads to Mac using Seafile file service which is running with Docker and will save in Mac under folder named with photo taken date with Mac Automator and Bash. And the photo folders will sync to Google Drive with python custom program running with cronjob. That's the workflow.

Requirements
-----------
1. Docker Desktop in Mac
2. Seafile Server and Client
3. Mac Automator
4. Bash
5. Python3

Workflow Diagram
----------------
![Syncing Photos Workflow Diagram](https://github.com/ye-hbone-myat/syncingphotos/blob/cbee168cb7f8f264dc28cc93d23e449bc7dfbb0b/Images/Screen%20Shot%202021-11-28%20at%203.05.23%20AM.png)

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
( if they are running ,you will see the docker containers: seafile, seafile-mysql and seafile-memcached)

7. Type **127.0.0.1** or **localhost** in your browser. After seafile server is up and running, you will able to see the seafile login screen. Use **username** and **password** which are predefined in docker compose file to login seafile server.

8. Create a library for your photos in the seafile web ui.


9. After login, click the account logo in the top-right corner and click the system admin. In the system admin UI, click the setting and you will see the **SERVICE_URL** and **FILE_SERVER_ROOT**. Change your machine IP Address in **SERVICE_URL** and **FILE_SERVER_ROOT**. After that. you will able to use your ip address as seafile server.

10. Install seafile desktop syncing client in Mac and seafile pro client in Ipad. Follow this [link](https://www.seafile.com/en/download/) for Mac and Follow this [link](https://apps.apple.com/us/app/seafile-pro/id639202512) for Ipad.


Configure Seafile Pro Client in Ipad
------------------------------------
1. open Seafile Pro Client

2. login with your credentials (Server IP Address, Username, Password)

3. Go to setting and turn on camera upload setting. It will provide you step-by-step configuration UI. Choose the library you created and select your camera album. This will allow you to upload automatically your photos from camera album to seafile library.

Configure Seafile Desktop Syncing Client in Mac
-----------------------------------------------
1. open Seafile Desktop Client

2. login with your credentials (Server IP Address, Username, Password)

3. Right click on the library you created, click **sync this library** and this will sync your photos to your Mac automatically.


