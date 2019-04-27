# RSVP
Really Simple Video Place - software that works with Open Broadcast Software

This project contains 2 python files. The first, rsvp.py, has a GUI front end for OBS. This launches a PowerPoint Viewer or a browser for use with OBS. It selects a profile and a scene collection too. The ptuya library controls the wifi sockets that turn on and off the lighting in the RSVP studio.
The other file, rectest.py, is an OBS script. It detects the record start and stop events and turns a USB light (blink1) to red (recording) or blue (idle).
