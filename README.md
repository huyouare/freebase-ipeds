Constructing Master List of Colleges & Data
=========================================

### Introduction
The purpose of this project was to:   
1) Create a more complete list of schools,  
2) Collect more data for each school for use in the mode, and  
3) Reconcile the previous list of schools to the new list.

### Goals:
* Establish reliable sources of data
* Discern a unique and complete ID(s)
* Collect as many accredidated colleges by volume 
* Append SAT/ACT, graduation and retention rates
* Append debt, and default rate data

### Getting Started
######Install dependencies:  
`pip install -r requirements.txt`

###Procedure:
#####Establishing sources of data & IDs
We gathered 4-5 sources that were publicly available:  
* IPEDS (Integrated Postsecondary Education Data System) Data Center from NCES (National Center for Education Statistics)  
http://nces.ed.gov/ipeds/datacenter/  
* Freebase /education Domain & IPEDS Namespace
http://www.freebase.com/education/educational_institution 
http://www.freebase.com/authority/nces/ipeds
* 

Four sources of IDs were collected: the IPEDS IDs, OPE IDs, Department of Education IDs, and Freebase IDs. Though each source provides an extended list of schools and more data, the IPEDS ID was chosen as the main ID. The IPEDS ID, provided by NCES, was unique to each university and was the most complete. OPE IDs were unique to each campus (with the main campus's 6-digit ID ending in 00), but were not as comprehensive. 

####Notes:
