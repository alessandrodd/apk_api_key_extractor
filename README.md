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
$ cp config.example.yml config.yml
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

## Run in a docker container
```bash
NOTE: make sure your .APK file is in the 'apks' folder.

$ git clone --recursive https://github.com/alessandrodd/apk_api_key_extractor.git
$ cd apk_api_key_extractor
$ docker build -t apk_key_extractor:latest .
$ docker run -it apk_key_extractor:latest

Rebuild your image when you've added other .apk's in your 'apks' folder.
```

## Config File Explained
### config.yml
**apks_dir** => The folder containing the .apk files to be analyzed

**apks_decoded_dir** => The folder that will temporarily contain the decompiled apk files

**apks_analyzed_dir** => The folder that will contain the already analyzed .apk files. Each time an APK is analyzed, it gets moved from the apks_folder to this folder

**save_analyzed_apks** => If false, the .apk files gets removed instead of being moved to the apks_analyzed folder

**apktool** => Path of the main [apktool](https://ibotpeaches.github.io/Apktool/) jar file, used to decode the apks

**lib_blacklists** => Txt files containing names of the native libraries (one for each line) that should be ignored during the analysis

**shared_object_sections** => When analyzing native libraries, all the ELF sections listed here will be searched for API Keys

**dump_all_strings** => If true, the script dumps not only API Keys but also every other string found in the APK. Useful to make a dataset of common not-api-key strings that can be used to train the model itself.

**dump_location** => Where to dump the API Keys found (as well as every other strin, if dump_all_strings is set to true). Possible values are console (stdout), jsonlines (text files in the [jsonlines](http://jsonlines.org/) format), mongodb.

**jsonlines.dump_file** => Path of the jsonlines file where the API Keys will be dumped

**jsonlines.strings_file** => Path of the jsonlines file where the every string will be dumped, if dump_all_strings is true

**mongodb.name** => Used if key_dump is set to mongodb; name of the MongoDB database

**mongodb.address** => Address of the MongoDB database

**mongodb.port** => Port to which to contact the MongoDB database (default 27017)

**mongodb.user** => MongoDB database credentials

**mongodb.password** => MongoDB database credentials

# Notes
I'm a curious guy; if you make something cool with this and you want to tell me, drop me an email at didiego.alessandro+keyextract (domain is gmail.com)
