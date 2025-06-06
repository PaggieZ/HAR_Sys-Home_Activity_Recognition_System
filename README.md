<!-- ABOUT THE PROJECT -->
## About The Project
The phone app for this project includes dashboards that display wake-up time, sleep time, bathroom trip frequency, sleep duration, sensor battery usage, etc, providing private, accessible and preventive insights into the smart home residents’ health status.
This repository includes the latest APK file to install the app on an Android phone and the code used to generate the APK file.  

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple example steps.

### Prerequisites
* Smartphone with Android 15 (SDK/API Level 35) or Higher!
* Raspberry Pi 4B with downloaded code found at [Smart-Home-Activity-Recognition-System Repo](https://github.com/PaggieZ/Smart-Home-Activity-Recognition-System) and configured with SPP (serial port profile) for Bluetooth communication.

### Installation
To work with the code: 
1. Clone the repo.
   ```sh
   git clone https://github.com/lmvchau/HAR-App.git
   ```
2. Open the 'app' folder in Android Studio IDE.
   
To directly view the app: 
1. Select **app-debug.apk** from the main branch and download.
2. Open the APK file on a smartphone that meets the prerequisites.
3. Allow complete installation.


<!-- USAGE EXAMPLES -->
## Usage
1. Ensure Bluetooth is enabled and that the Raspberry Pi is discoverable.
2. Connect with the Raspberry Pi via your phone's settings, if this is the first time connecting the two.
3. Open the app and navigate to the Bluetooth Screen via the bottom navigation window.
4. Press "Show Paired Devices" and ensure the Raspberry Pi pops up.
5. Open a bluetooth channel on the Raspberry Pi's side.
   ```sh
   hciconfig
   sudo rfcomm watch hci0
   ```
   After seeing the following output, you may proceed to the next step.
   ```
   Waiting for connection on channel 1
   ```
7. Press "Connect to Device" to connect to the Raspberry Pi. 
8. Open a separate terminal and run PythonBluetooth.py on the Raspberry Pi.
   ```sh
   python3 PythonBluetooth.py
   ```
9. Wait for the "Raspberry Pi Listening" Toast pop-up before beginning to select a specific date and request data via 'Get Health Data' button.

_For more help, please refer to the [Video Demo -- Sorry for the shaky camera](https://youtu.be/jgieGqn79Qg)_


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
The following resources were utilized:
* [Android Bluetooth Basics Code Snippets](https://gist.github.com/t-34400/7c80a06925058f6a1076cbf1d5e8fd29)
* [MPAndroidChart Library](https://github.com/PhilJay/MPAndroidChart)
* [OpenAI Chat-4o Model](https://chatgpt.com/?model=gpt-4o)
* [Best README.md template](https://github.com/othneildrew/Best-README-Template/blob/main/BLANK_README.md)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
