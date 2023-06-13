# Two Bottle Monitor Time Bins 🐁

### Overview

__Two Bottle Monitor__

![image](https://github.com/H-Dempsey/Two_bottle_monitor_time_bins/assets/101311642/45877e65-1e08-4496-9733-2aff0cde704b)

The Two Bottle Monitor is an open source [automated mouse homecage two-bottle choice test device](https://hackaday.io/project/160388-automated-mouse-homecage-two-bottle-choice-test-v2).
It was developed by Meaghan Creed, Lex Kravitz, Jibran Khokhar and Lizzy Godynyuk.

__Purpose__

The CSV output from the these devices are in 1 min time bins. For the creation of custom time bin lengths, this repository:
* Slightly the C++ Arduino code to output timestamps of events, rather than time bins.
* Provides a Python GUI which converts this output into a time binned file with a custom bin length.
* The GUI can also group analysis for each of the varibles Left Count, Left Duration, Right Count and Right Duration. <br>

Also check out [SipperViz](https://github.com/earnestt1234/SipperViz), which provides more GUI functionality and analysis tools.

__Preview of the graphical user interfaces__

![image](https://user-images.githubusercontent.com/101311642/195033127-046fec78-24ae-4ab7-b059-f763a19e93b4.png)

__Input and output data__

![image](https://user-images.githubusercontent.com/101311642/194794376-e8ae77ac-dbc8-41dc-a1c8-bf0b7ace3f52.png)

### Installation

Install [Anaconda Navigator](https://www.anaconda.com/products/distribution). <br>
Open Anaconda Prompt (on Mac open terminal and install X-Code when prompted). <br>
Download this repository to your home directory by typing in the line below.
```
git clone https://github.com/Andrews-Lab/FED3_time_bins.git
```
If you receive an error about git, install git using the line below, type "Y" when prompted and then re-run the line above.
```
conda install -c anaconda git
```
Change the directory to the place where the downloaded folder is. <br>
```
cd FED3_time_bins
```

Create a conda environment and install the dependencies.
```
conda env create -n FTB -f Dependencies.yaml
```

### Usage
Open Anaconda Prompt (on Mac open terminal). <br>
Change the directory to the place where the git clone was made.
```
cd FED3_time_bins
```

Activate the conda environment.
```
conda activate FTB
```

Run the codes.
```
python FED.py
```

### Guide

View the guide about [how to analyse your FED data](How_to_use_FED_code.pdf).

<br>

### Acknowledgements

__Author:__ <br>
[Harry Dempsey](https://github.com/H-Dempsey) (Andrews lab and Foldi lab) <br>

__Credits:__ <br>
Zane Andrews, Wang Lok So, Lex Kravitz <br>

__About the labs:__ <br>
The [Andrews lab](https://www.monash.edu/discovery-institute/andrews-lab) investigates how the brain senses and responds to hunger. <br>
The [Foldi lab](https://www.monash.edu/discovery-institute/foldi-lab) investigates the biological underpinnings of anorexia nervosa and feeding disorders. <br>
The [Kravitz lab](https://kravitzlab.com/) investigates the function of basal ganglia circuits and how they change in diseases such as obesity, addiction, and depression. <br>
