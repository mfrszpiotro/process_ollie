# process_ollie
Data science project which inspects possible useful properties of a motion captured skateboarder performing so called "Ollie". Data is gathered Kinect v2 body+floor frames. This work was created alongside bachelor thesis application at Warsaw University of Technology.
* [related thesis paper](https://github.com/mfrszpiotro/ollie_with_kinect/blob/main/docs/praca_inzynierska_mpiotrowski.pdf)
* [desktop application which utilizes process_ollie CLI tool and Microsoft Kinect sensor](https://github.com/mfrszpiotro/ollie_with_kinect)

## Overview
The comparison algorithm was created using Python, and it involves two types of
indicators that can be used to distinguish between two trick performances. The first
indicator is based on the variations in timing between detected events occurring within
the duration of the ollie:

<img src="/reports/figures/example-time-constraints.png" width="500" />

The second indicator involves comparing time series representative of the angle between the skater’s hip bones (crotch angle):

<img src="/reports/figures/example-crotch-angle-asymmetric.png" width="500" />


More than that, proposed code solution is adaptable, and the indicators can be used to extract results from arbitrary Ollie stage.

## Usage (Windows):
```
python -m venv env
.\env\Scripts\activate
pip install -r requirements
python plot_app.py
```

## Process Ollie - Usage (Windows):
```
python processing_app.py
```

## Run tests (currently not working - todo):
```
python -m pytest
```
