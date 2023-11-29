# ALevel topic-based Pastpaper Scraper
## Introdution
Physics and maths is a useful and famous website which is filled with pubulic pastpaper and revision resources. This python program provides a demo to scrape some the revision practice categorized by topic in CAIE ALevel and IGCSE exams. The downloaded resources will be automaticallly stored in the folders with related URLs(usually contain the name of topic) 

In this demo, only revision resources of Biology, Physics and Chemistry from CAIE will be downloaded(beacause clearly these are the subjects I choose.  
## Use
Download all the source code.

Use poetry or maunally load all the dependency in toml file.

```
poetry install
```

Run pastpaper_craper.py 

## Improve
The logic of these program is to index for PDF file in a specific subject URL(specify the organization like CAIE). The URL list is stored in the .env file, you can change the urls to download resources of different subjects.
