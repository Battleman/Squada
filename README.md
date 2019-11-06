# Life in New York City

# Abstract
Nowadays many communities in the United States and Canada provide a special telephone number
"3-1-1". It works just like 9-1-1, but for request of non-emergency municipal services,
 such as: a broken streetlamp, presence of rats in a neighbourhood, bulk trash pick up.
Inhabitants can submit their requests either by phone or by using a web platform.

In NYC the service has been introduced in 2003 and became the largest 3-1-1 in operation to date.
All those requests are made publicly available with a lot of information regarding each ticket, such as:
 time of submission, time of closing, neighborhood, geolocation, etc. Through analysis of this data
 we aim to understand what are the main problems in NYC. A success in providing meaningful insights 
 could be used as a proof of concept to convince more cities to set this service up and ease
 the communication between a city and it's inhabitants.

# Research questions
* Can we rank neighborhoods based the number/delay of requests?
* Can we identify recurring patterns/seasonality that could help preventing the issues?
* Is there a clear trend of the problems?
* Can we identify external events that influence the rate of requests within a timeframe?

# Datasets
List the dataset(s) you want to use, and some ideas on how do you expect to get, manage, process and enrich it/them. Show us you've read the docs and some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant.

## Datasets we will use
- **NYC 311 Service Requests from 2010 to Present**\
All the 311 requests from 2010 up till now, updated daily. Currently about 22M entries, publicly available.
The data is stored in csv format and contains attributes like: Complaint Type, Created Date, Closed Date, Due Date,
Incident Address, etc.
-  **NYC Population By Neighborhood Tabulation Areas**\
Self explanatory. In csv format.
-  **Neighborhood Tabulation Areas**\
Boundaries of Neighborhood Tabulation Areas in NYC in GeoJSON format. 

## Methodology
1. The data can be accessed from [data.cityofnewyork.us](https://data.cityofnewyork.us/)
2. The 311 dataset contains location based on GPS coordinates while the population data is based on the Neighborhood Tabulation Areas, so we will have to map the requests to regions using the Neighborhood Tabulation Areas dataset.
3. Analyse complaint types and dates to identify short-term and long-term trends for Neighborhood Tabulation Areas, seasonalities, and separate the changes within neighborhoods from city-wide trends.
4. Compile a clean dataset of the external events related to neighborhoods, and attempt to provide insights on the changes observed by relating event timestamps to our trends.
5. Provide a ranking of neighborhoods using relevant metrics that we will infer from the data analysis process.

# A list of internal milestones up until project milestone 2
- Nov. 4th: Making sure the data is clean, downloading it and deciding on a pipeline (Spark?)
- Nov. 11th: Selecting relevant attributes, joining data from multiple tables. Cleaning the datasets.
- Nov. 18th: First version of the analysis notebook with initial plots and visualization. Finding more specific/additional research questions.
- Nov. 25th: Milestone 2 deadline. Finalizing the analysis and visualization.
