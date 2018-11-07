# apk_api_key_extractor
Automatically extracts API Keys from APK (Android Package) files

For technical details, [check out my thesis (_Automatic extraction of API Keys from Android applications_) and, in particular, **Chapter 3 and 4** of the work.](https://goo.gl/uryZeA)

The library responsible for identifying the API Keys is [a standalone project](https://github.com/alessandrodd/api_key_detector).

Searches for API Keys embedded in Android String Resources, Manifest metadata, Java code (included Gradle's BuildConfig), Native code.

## Requirements

- Java 7+
- Python 3.5+
- Modules in requirements.txt (use pip3 to install)
```
pip3 install -r requirements.txt
```

## Installation

```bash
$ git clone --recursive https://github.com/alessandrodd/apk_api_key_extractor.git
$ cd apk_api_key_extractor
$ pip3 install -r requirements.txt
$ python3 main.py
```

## Test
```bash
$ git clone https://github.com/alessandrodd/ApiKeyTestApp.git
$ cd apk_api_key_extractor
$ python3 main.py --analyze-apk ../ApiKeyTestApp/apk/apikeytestapp_obfuscated.apk
```

## Usage

```bash
usage: main.py [-h] [--debug] [--analyze-apk APK_PATH] [--monitor-apks-folder]

A python program that finds API-KEYS and secrets hidden inside strings

optional arguments:
  -h, --help            show this help message and exit
  --debug               Print debug information
  --analyze-apk APK_PATH
                        Analyze a single apk to find hidden API Keys
  --monitor-apks-folder
                        Monitors the configured apks folder for new apks. When
                        a new apk is detected, the file is locked and analysis
                        starts.
```

Let's say you want to find any API Key hidden inside a set of Android apps.

Using the default settings:
- Copy all the desired .apk files to the [_apks_](apks) folder
- Start apk_api_key_extractor with the _monitor-apks-folder_ argument, i.e. : ```python3 main.py --monitor-apks-folder```
- Check the _apikeys.json_ file for detected API Keys
- As soon as an apk is analyzed, it gets moved from the [_apks_](apks) to the [_apks_analyzed_](apks_analyzed) folder

Note that this software is process-safe, meaning that you can start multiple instances of the same script without conflicts. You can also configure the _apks_ folder as a remote folder in a Network File System (NFS) to parallelize the analysis on multiple hosts.

## Config File Explained
### config.json
**key_dump** => Can be **local** or **remote**. If local, the detected API Keys are dumped as json objects in the configured local_dump_file json file. If remote, then **_dbconfig.json_ should be configured**

**local_dump_file** => If key_dump is set to local, the destination file where the API Keys should be dumped

**apks_folder** => The folder containing the .apk files to be analyzed

**apks_decoded** => The folder that will temporarily contain the decompiled apk files

**apks_analyzed** => The folder that will contain the already analyzed .apk files. Each time an APK is analyzed, it gets moved from the apks_folder to this folder

**save_analyzed_apks** => If false, the .apk files gets removed instead of being moved to the apks_analyzed folder

**apktool** => Path of the main [apktool](https://ibotpeaches.github.io/Apktool/) jar file, used to decode the apks

**lib_blacklists** => Txt files containing names of the native libraries (one for each line) that should be ignored during the analysis

**shared_object_sections** => Txt files containing names of the ELF sections (one for each line) that should be searched for API Keys

**logging** => Used to config logging capabilities, see [here](https://docs.python.org/3/howto/logging.html)

### dbconfig.json
Used if key_dump is set to _remote_

**name** => Name of the MongoDB 3.+ database

**address** => Address of the MongoDB 3.+ database

**port** => Port to which to contact the MongoDB 3.+ database (default 27017)

**user** => Database credentials

**password** => Database credentials