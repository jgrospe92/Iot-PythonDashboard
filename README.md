# Iot-PythonDashboard
Academic Project for IoT Course.

# Project Description
By utilizing sensors, actuators, motors, Single-board computers, and micro-controllers, students
design and simulate a smart home. They capture environmental information and make a decision
based on received data. They also develop access control and occupancy systems and transfer all
data to the cloud or a local server. Finally, they design and develop a web-based IoT dashboard to
control and monitor the system.

# IOT dashboard Gadgets
## LED Controll
![LED_control](https://user-images.githubusercontent.com/77903214/226199328-e43ea068-e232-4dad-af93-d2dc6bbfe0ae.gif)

## Temperature Controll
![fan_control](https://user-images.githubusercontent.com/77903214/226211001-8dbc55a2-8f59-43f4-8850-296829f73b0b.gif)

# Virtual Environment
## Windows
- cd to the to main directory
- Once inside Iot-PythonDashboard
- Run the command `Scripts\activate` to activate the virtual environment
- Your terminal should change into this (Iot-PythonDashboard)
- To deactivate it, run the command `deactivate`


## Arduino & MAc
- cd to the to main directory
- Once inside Iot-PythonDashboard
- Run the command `source Scripts/activate` to activate the virtual environment
- Your terminal should change into this (Iot-PythonDashboard)
- To deactivate it, run the command `deactivate`
# Important
- Make sure you name the folder Iot-PythonDashboard
- if you don't have the virtual environment installed, you can't activate the virtual environment
- run this command to install it `pip install virtualenv`

# Installing Dependencies
- Make sure you're in the python environment
- Then run the command `pip install -r requirements.txt`
- If the above command doesnt work
- You have to install each dependencies manually by running this command
- `pip install {the name of the dependency}`
- Check the requirements.txt for the names

# How to install SqLite Browser
- Run this command `sudo apt-get install sqlitebrowser`

# How to run the project
- Look for the app.py and execute it
- It should provide you a localhost address

# Email Libraries
- Red mail
  - For sending email 
  - [Documentation](https://red-mail.readthedocs.io/en/stable/tutorials/getting_started.html)
- Redbox
  - For receiving email
  - [Documentation](https://red-box.readthedocs.io/en/latest/tutorials/getting_started.html)
- :warning: IMPORTANT In order for the email function to work, you have to create email_config.py in src/Controller/
- Inside that python file add you credentials as key value pair
- example : `username = "your usename` `password = "your password"`

# Plottly Dash Documentation
- https://dash.plotly.com/
