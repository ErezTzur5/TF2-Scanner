Welcome,

Last week, I had a conversation with a friend who reminded me of our past activity: scanning players from Team Fortress 2 servers to check their played hours and inventory items. This sparked an idea in me to create an executable (exe) file that replicates this process.

This scan 48 players in under 2 mins

For the realization of this project, I employed several technologies: Python, tkinter, pyinstaller, APIs, Web-Scraping, and multiprocessing.

The process begins by logging into a server, followed by opening the console ( ` ) and entering the "status" command:

![edit1](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/381353b8-4627-49f2-8218-ea9fc9fbaee1)

The output of this command is then copied:

![edit2](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/d1252f1b-60b1-4084-bb5e-b6ddb3a359bb)

After that, the executable is launched:
![image](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/1bb2c3a7-abde-4ebc-8129-18c851c78269)

The copied data is pasted into the GUI, and the "Scan" button is pressed:
![edit3](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/1062e0e4-2f9c-4dff-b7e8-5243d0143af0)


Within a few seconds, a "Player Info" button becomes accessible, which, when clicked, displays the results:
![edit4](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/e00fd932-6985-4436-91be-8ae31097755b)

The results are presented in the following format:

The player with the least played hours appears at the top of the list.

Players with more than 700 hours played will not be shown.

In terms of inventory:

The top 10 most valuable items in each player's inventory are showcased, sorted in descending order of value.

Visual representation(prices shown too):

![Capture](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/9df92ffc-1689-447b-a962-ce32fa60b93f)
![Capture2](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/56673c1c-febf-4846-8100-cebc19533082)
![Capture3](https://github.com/ErezTzur5/TF2-Scanner/assets/141019783/74a381d0-d0af-46a0-add9-9f05dc407225)


notes: i didnt publish the full-code yet. in the future if people request

Discord: erezur#4734
