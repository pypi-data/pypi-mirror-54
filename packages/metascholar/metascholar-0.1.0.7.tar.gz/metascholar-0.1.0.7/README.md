# MetaScholar 

Metascholar is digital library scholarly metadata retrieve tool based on python.
Metascholar is originally developed for the purpose of obtaining the metadata from the [EZProxy](https://www.oclc.org/en/ezproxy.html) (or any other library proxy system) logs.
All code is free and open source.

MetaScholar is a processing project which aims at empowering library researchers with easy, quick, and flexible tools to manage, update, and check their scholarly digital resources.
Current version of MetaScholar uses the functions from [CrossRef](https://www.crossref.org/services/metadata-delivery/rest-api/) and [OpenURL](https://en.wikipedia.org/wiki/OpenURL).

We welcome the library researchers in any field to work together for this project. 
Please check [CONTRIBUTING](https://github.com/ameyakarnad/metascholar/CONTRIBUTING.md) for more detail.

# Functions 

Currently, we focus on the logs in common log format.
The address that we provide solutions are starting point URLs.


## Versioning

| Version | Release Date | Comments |
|---------|--------------|----------|
| v0      | Sep 2019     | First documented version |

## log_processing
| function | parameter |  Return | Note |
|---------|--------------|----------|----------|
| log_process | log file path and name, column | list of column value| column can be 'ip','Session', 'datetime','address','status','size', and 'protocol'| |



## metadata
| function | parameter |  Return | Note |
|---------|--------------|----------|----------|
| get_DOI_from_URL | URL |return DOI or False| |
| get_metadata_from_DOI | DOI |return Metadata or False | |
| get_metadata_from_URL | URL | return Metadata or False | try to find DOI and openurl first |

## download
| function | parameter |  Return | Note |
|---------|--------------|----------|----------|
| download | DOI, location | save pdf or xml files| |
| download_bulk | DOI list | save pdf or xml files| multi-threading download  |

# Documentation History
