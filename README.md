# Two Bottle Monitor Time Bins 🐁

### Overview

__Two Bottle Monitor__

<p align="center">
<img src="https://github.com/H-Dempsey/Two_bottle_monitor_time_bins/assets/101311642/45877e65-1e08-4496-9733-2aff0cde704b" width="400">

The Two Bottle Monitor is an open source [automated mouse homecage two-bottle choice test device](https://hackaday.io/project/160388-automated-mouse-homecage-two-bottle-choice-test-v2).
It was developed by Meaghan Creed, Lex Kravitz, Jibran Khokhar and Lizzy Godynyuk.

__Purpose__

The CSV output from the these devices are in 1 min time bins. For the creation of custom time bin lengths, this repository:
* Provides a slightly modified C++ Arduino code (from the link above), so that the device can output timestamps of events, rather than time bins.
* Provides a Python GUI which converts this output into a time binned file with custom bin lengths.
* Can also perform group analysis for each of the varibles Left Count, Left Duration, Right Count and Right Duration. <br>

Also check out [SipperViz](https://github.com/earnestt1234/SipperViz), which provides more GUI functionality and analysis tools.

__Preview of the graphical user interfaces__

![image](https://github.com/H-Dempsey/Two_bottle_monitor_time_bins/assets/101311642/176527ab-0f73-4fb9-b0ff-73142e51f726)

__Input and output data__

![image](https://github.com/H-Dempsey/Two_bottle_monitor_time_bins/assets/101311642/01e446b1-b4fa-42ba-94d0-f48c039bba02)
  
### Simple GUI installation

Download the executable file for PC and double click to open it (note that it will take a while to start up). <br>
Unfortunately, this is not compatible with Mac. <br>
If you hover your cursor over text, help messages will appear, which can guide you through the GUI.

[Download here](https://figshare.com/articles/software/Two_Bottle_Choice_Analysis_GUI/24196047)

### Arduino device installation
  
Follow the instructions for building the sipper monitor and installing Arduino [here](https://hackaday.io/project/160388-automated-mouse-homecage-two-bottle-choice-test-v2). <br>
Use the latest libraries on that website, which can also be found [here](https://cdn.hackaday.io/files/1603886862040192/SipperLibraries102420.zip). <br>
Flash the C++ sipper codes in this repository onto your devices.
  
### Alternative GUI installation

Install [Anaconda Navigator](https://www.anaconda.com/products/distribution). <br>
Open Anaconda Prompt (on Mac open terminal and install X-Code when prompted). <br>
Download this repository to your home directory by typing in the line below.
```
git clone https://github.com/H-Dempsey/Two_bottle_monitor_time_bins.git
```
If you receive an error about git, install git using the line below, type "Y" when prompted and then re-run the line above.
```
conda install -c anaconda git
```
Change the directory to the place where the downloaded folder is. <br>
```
cd Two_bottle_monitor_time_bins
```

Create a conda environment and install the dependencies.
```
conda env create -n TBTB -f Dependencies.yaml
```

To run the codes through Anaconda, first close everything. <br>
Open Anaconda Prompt (on Mac open terminal). <br>
Change the directory to the place where the git clone was made.
```
cd Two_bottle_monitor_time_bins
```

Activate the conda environment.
```
conda activate TBTB
```

Run the codes.
```
python Codes/Run_program.py
```

### Acknowledgements

__Author:__ <br>
[Harry Dempsey](https://github.com/H-Dempsey) (Andrews lab and Foldi lab) <br>

__Credits:__ <br>
Leigh Walker, Simon Miller, Xavier Maddern, Andrew Lawrence Meaghan Creed, Lex Kravitz <br>
