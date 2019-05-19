# Introduction
This folder contains Python and batch scripts that will help populate a fresh portal
with users, groups and content for each of the user accounts. You can find the
list of users and groups in the corresponding `users.csv` and `groups.csv`
files.

## Steps
 1. Run `cloud_formation_a.bat` which will download and install miniconda,
 then install the `arcgis` package in a environment called `cloud_formation`
 1. Run `cloud_formation_b.bat` which execute the Python scripts in sequence
 and creates users, groups and content.
 2. Optionally run `clean_up.bat` to erase all users, groups and content

# Sample outputs below

## Running the cloud formation batch files
Call the batch files one after another. These files return 0 upon success. The `cloud_formation_b.bat`
accepts 4 command line arguments. Pass the URL to the portal, admin username and password and the log file
to output the messages.

```
>> cloud_formation_a.bat
0
```

```
>> cloud_formation_b.bat https://ESRIwebgis.webgistesting.net/portal -u admin -p xxxxxx -l python_log.log
Creating new environment
Package plan for package removal in environment C:\Users\atma6951\miniconda3\envs\cloud_formation:

The following packages will be REMOVED:

    arcgis:             1.0.1-py36_1  esri
    bleach:             1.5.0-py36_0
    colorama:           0.3.7-py36_0
...

Fetching package metadata ...........
Solving package specifications: .
Package plan for installation in environment C:\Users\atma6951\miniconda3\envs\cloud_formation:
The following NEW packages will be INSTALLED:

    pip:            9.0.1-py36_1
    python:         3.6.0-0

Installing arcgis package
Fetching package metadata .............
Solving package specifications: .
Package plan for installation in environment C:\Users\atma6951\miniconda3\envs\cloud_formation:
The following NEW packages will be INSTALLED:

    arcgis:             1.0.1-py36_1  esri
    bleach:             1.5.0-py36_0
...
Uninstalling prior versions of arcgis widget
- Validating: ok
0

0
```
# Running the Python scripts individually
If you choose to run the scripts individually instead of calling them using the batch files, you can do so 
as shown below. All files accept command line parameters, to view the options, call them with `--help` flag.

## Running clean_up.py
`clean_up.py` accepts the credentials as command line args. Inquiring help
on the file returns the following:

```
E:\code>python cleanup.py --help
usage: cleanup.py [-h] [-u USER] [-p PASSWORD] url

positional arguments:
  url                   Portal url of the form:
                        https://portalname.domain.com/webadaptor

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Administrator username
  -p PASSWORD, --password PASSWORD
                        Administrator password
  -l LOG_FILE --log     Log file to record all process outputs
```

Running it with credentials returns the following
```
E:\code>python cleanup.py https://ESRIwebgis.webgistesting.net/portal -u admin -p xxxxxx -l python_log.log
=====================================================================
RUNNING CLEANUP
Deleting groups
---------------

Deleting Basemaps  ##  success
Deleting Central Services  ##  success
...

Deleting user content
---------------------
User : adams.powell # 
Deleting : Adams Powell response locations # True | 
Deleting : SC # True | 
Deleting : SC # True | empty
User : admin # skipped
...

Deleting users
--------------
Deleting adams.powell  ##  success
Deleting allen.price  ##  success
Deleting anderson.bailey  ##  success
...

 All clean
```

## Running create_groups.py
Similar to `clean_up.py`, `create_groups.py` also accepts command line args.
Running it with valid credentials prints the following output:

```
E:\code>python create_groups.py https://ESRIwebgis.webgistesting.net/portal -u admin -p xxxxx
CREATING GROUPS
 Creating group:  Basemaps  ##  success
 Creating group:  Central Services  ##  success
 Creating group:  Compliance  ##  success
 Creating group:  Customer Service, Finance, Billing and Accounting  ##  success
 Creating group:  Demographic Content  ##  success

```

### Running create_users.py
`create_users.py` will create users on the portal and add them to appropriate
groups specified in the `users.csv` file. Running it with valid credentials
reports below, truncated for brevity:

```
E:\code>python create_users.py https://ESRIwebgis.webgistesting.net/portal -u admin -p xxxxxxx
CREATING USER ACCOUNTS
Creating user:  smith.collins ## success  ##
         Adding to groups:  # Basemaps #  Central Services #

Creating user:  johnson.stewart ## success  ##
         Adding to groups:  # Basemaps #  Central Services #

Creating user:  williams.sanchez ## success  ##
         Adding to groups:  # Basemaps #  Central Services #
...
```

### Running publish_content.py
This script will publish feature layers, web map with those layers and
assign it to each of the user. Running it will print the following output,
truncated for brevity:

```
E:\code>python publish_content.py https://ESRIwebgis.webgistesting.net/portal -u admin -p xxxxx
Publishing  .\user_content\KS.csv # webmaps ## success. Assigning to:   #  smith.collins
Publishing  .\user_content\NV.csv # webmaps ## success. Assigning to:   #  johnson.stewart
Publishing  .\user_content\IN.csv # webmaps ## success. Assigning to:   #  williams.sanchez
Publishing  .\user_content\NC.csv # webmaps ## success. Assigning to:   #  jones.morris
....
```