# HAR Sys (Home Activity Recognition System Public Repository)

<!-- ABOUT THE PROJECT -->
## About The Project

The project utilizes the CASAS dataset to train an ML model to predict the presence of UTI (urinary tract infection) and health features valuable for monitoring. The ML model was can be deployed on a Raspberry Pi for on-site prediction and the results can be sent to an Android phone app for clinical monitoring. 

The **main** branch includes all files used in the two data processing pipelines, excluding weights, raw sensor data, and activity-labeled sensor data. \
The **Bluetooth-Branch** branch includes all files actually uploaded onto the Raspberry Pi.\
The **app** branch includes all relevant files for the app, including the APK file to install the application on an Android phone.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple example steps.

### Prerequisites
* Raspberry Pi 4B configured with SPP (serial port profile) for Bluetooth communication.
* Android phone with APK file found at the [**app** branch](https://github.com/PaggieZ/Smart-Home-Activity-Recognition-System/tree/app)

### Installation 
1. To deploy the code onto the microcontroller, clone the Bluetooth-Branch branch on the Raspberry Pi.
   ```sh
   git clone -b Bluetooth-Branch https://github.com/PaggieZ/Smart-Home-Activity-Recognition-System.git
   ```
2. Ensure the Raspberry Pi is discoverable.
3. On the phone app's side, connect with the Raspberry Pi via the phone's settings if this is the first time connecting the two devices.
4. Open the app and navigate to the Bluetooth Screen via the bottom navigation window.
5. Press "Show Paired Devices" and ensrue the Raspberry Pi pops up.
6. Open a bluetooth channel on the Raspberry Pi's side:
   ```sh
   hciconfig
   sudo rfcomm watch hci0
   ```
   After seeing the following output, you may proceed to the next step.
   ```
   Waiting for connection on channel 1
   ```
7. In the opened app, Press "Connect to Device" to connect to the Raspberry Pi. 
8. Open a separate terminal and run PythonBluetooth.py on the Raspberry Pi.
   ```sh
   python3 PythonBluetooth.py
   ```
_For more help, please refer to the [Video Demo -- Sorry for the shaky camera](https://youtu.be/jgieGqn79Qg)_
   
### Usage 
```PythonBluetooth.py``` allows for 3 modes: 

1. ```PROCESS```
* Process raw data, extract features, and UTI labeling for model input and training
* _Please see the [Process Video Demo -- Sorry for the even more shaky camera](https://youtu.be/K6eTaZum5Kk?si=h9xnVUI0uJSMzYLJ)_

2. ```SEND_STR ```
* The program will prompt user for a data string
* The phone app will then receive the string. 
3. ```SEND_DATA```
* The program will prompt user for a date in format yyyy-mm-dd.
* The program will then compute a UTI prediction and send relevant features to the phone app.


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
**Special thank you to Dr. Chen-Nee Chuah, Dr. Roschelle Fritz, Dr. Diane J. Cook, and Yui Ishihara.**\
The following resources were utilized:
* [AL Smart Home Model by Dr. Diane J. Cook](https://github.com/WSU-CASAS/AL-Smarthome/tree/master)
* [OpenAI Chat-4o Model](https://chatgpt.com/?model=gpt-4o)
* [Best README.md template](https://github.com/othneildrew/Best-README-Template/blob/main/BLANK_README.md)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
