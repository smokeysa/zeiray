# zeiray

These scripts provide a way to import time entry data from the Timeular API into Taskray.

The name Zeiray is a portmanteau of Timeular _Zei_ and Task _Ray_.

## Features

- Uses the Timeular API to download all your tracking data for the specified time period.
- Uses the Salesforce API to upload each time entry into Taskray.

## Limitations

- Requires each Activity in Timeular to include the TaskRay task ID. In the future this could be
replaced with some sort of keyword search in Taskray.

## Installation

1. Update `sf_creds.json` with your Salesforce credentials:

    * Username is the email address you use to log into salesforce.com.
    * `security_token` is your Salesforce security token. If you don't know this, you might be able
    to find it in an old email with Subject "Your new Salesforce security token", or you may have
    to reset it from `[your salesforce domain]//_ui/system/security/ResetApiTokenEdit?retURL=%2Fui%2Fsetup%2FSetup%3Fsetupid%3DPersonalInfo&setupid=ResetApiToken`
    * User ID is the internal identifier Salesforce uses for you. You can find this by navigating to
    your profile page and grabbing it from the URL - e.g. `https://undo.lightning.force.com/lightning/r/User/<here>/view`

2. Create a Timeular API key from the Timeular profile page https://profile.timeular.com/#/app/account.
The Python bindings are included in the checkout. They are an updated version of https://github.com/Ankirama/python-timeular
which is MIT licensed. Save your API kep to `timeular_creds.json` in this format: `{"apiKey": "...", "apiSecret": "..."}
3. Install `simple-salesforce` Python API with `pip install simple-salesforce`.

## Usage

`./import_times.py`

### Required format for Timeular activities

Unfortunately at the moment it is required for you to put the Taskray ID in the name of your activity,
in the following format: "blah de blah [TR#xxxxxxxxxxxxxx]".

## Contributions, bug reports, feature requests

I welcome any bug reports and contributions.

Feature requests will be taken on a case-by-case basis.

