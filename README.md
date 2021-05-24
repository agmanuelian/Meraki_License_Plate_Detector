# Meraki License Plate Detector

This projects integrates Meraki MV Cameras, MT Sensors and Plate Recognizer software to detect when a garage door is opened to take a snapshot, and detect vehicle license plates through Plate Recognizer software.

## Description

This project integrates Meraki MV Cameras with Amazon Rekognition through their APIs to perform a deeper image analysis, to detect whether a person is wearing a facemask or not. The results will be posted into a Webex Teams space.

### Workflow

The workflow will be the following:

![Alt text](imgs/workflow_plate.png "License Plate Detector - Workflow")
