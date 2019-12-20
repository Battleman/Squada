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

Based on our conclusions we will provide advice to the New York public service providers.

# Research questions
* Identify recurring patterns and evolution of the complaints relating to rats. Show correlation with the complaints to the Department of Sanitation.
* Rank neighborhoods based the number of complaints and delay in their resolution.
* Rank Education, Police, Sanitation and Fire departments by district of operation.
* Identify correlation between certain events, such as earthquakes or hurricanes, and the complaints that follow them.

# Datasets
## Datasets we will use
- **NYC 311 Service Requests from 2010 to Present**\
All the 311 requests from 2010 up till now, updated daily. Currently about 22M entries, publicly available.
The data is stored in csv format and contains attributes like: Complaint Type, Created Date, Closed Date, Due Date,
Incident Address, etc.
-  **NYC Population By Neighborhood Tabulation Areas**\
Self explanatory. In csv format.

Boundaries of areas in NYC in GeoJSON format:
-  **Neighborhood Tabulation Areas**
-  **Police Precincts**
-  **School Districts**
-  **DSNY Districts**
-  **Fire Battalions**

## Methodology
1. The data can be accessed from [data.cityofnewyork.us](https://data.cityofnewyork.us/)
2. The 311 dataset contains location based on GPS coordinates while the population data is based on the Neighborhood Tabulation Areas, so we will have to map the requests to regions using the Neighborhood Tabulation Areas dataset.
3. Analyse complaint types and dates to identify short-term and long-term trends for Neighborhood Tabulation Areas, seasonalities, and separate the changes within neighborhoods from city-wide trends.
4. Compile a clean dataset of the external events related to neighborhoods, and attempt to provide insights on the changes observed by relating event timestamps to our trends.
5. Provide a ranking of neighborhoods using relevant metrics that we will infer from the data analysis process.


# A list of internal milestones up until project milestone 3
- Dec. 2nd: Ranking agencies and neighborhoods.
- Dec. 9th: Analysis of the influence of external events and problems with rats/
- Dec. 16th: First version of the data story on GitHub.
- Dec. 20th: Milestone 3 deadline. Finalizing the visualization and the data story.


# Contributions
* Artur Szalata:
* Louis Landelle:
* Julien Heitmann:
* Olivier Cloux: Worked on analyzing and displaying seasonality pattern in the dataset. Also, created most of the structure of the website, and made it responsive, modern, and concise.