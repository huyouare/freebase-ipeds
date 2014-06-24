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
We gathered 6 sources that were publicly available:  
* IPEDS (Integrated Postsecondary Education Data System) Data Center from NCES (National Center for Education Statistics) 
http://nces.ed.gov/ipeds/datacenter/  
Supplemented by College Navigator  
http://nces.ed.gov/collegenavigator/  
* Freebase /education Domain & IPEDS Namespace  
http://www.freebase.com/education/educational_institution   
http://www.freebase.com/authority/nces/ipeds  
* Database of Accredidated Postsecondary Institutions and Programs  
http://ope.ed.gov/accreditation/  
* Payscale College Salary Report     
http://www.payscale.com/college-salary-report-2014/full-list-of-schools  
* CollegeInSight Graduates Debt  
http://college-insight.org/#explore/go&h=44b136f4d155362e46d5da65ab244409
* Three-year Official Cohort Default Rates for Schools (ed.gov)  
http://www2.ed.gov/offices/OSFAP/defaultmanagement/cdr.html

Four sources of IDs were collected: the IPEDS IDs, OPE IDs, Department of Education IDs, and Freebase IDs. Though each source provides a different list of schools and unique data, the IPEDS ID was chosen as the main ID. The IPEDS ID, provided by NCES, was unique to each university and was the most complete. OPE IDs were unique to each campus (with the main campus's 6-digit ID ending in 00), but were not as comprehensive. 

Considering the three most complete sources - IPEDS, Freebase, and DoE Accredidation, no one data set was a strict subset of another. Due to different IDs, years of recording, and accrediation measures, each set had colleges not contained in others. To construct the master list, the Freebase list and then the DoE tables were outer-joined on the IPEDS ID to the IPEDS data to create the largest set.

##### IPEDS
###### Download from Data Center:   
Select "Download Custom Data Files"   
Click "Select" to get all institutions   
(May not work. Instead, choose one variable that all schools have, and select the full range - e.g. 
Use drop-downs and search to select variables   
Download as CSV   

At the time, the latest set available for download was 2012 data. However, the College Navigator uses the most updated data, from 2013-2014. In order to collect a small set of data from colleges that were found in Freebase/DoE lists but not in IPEDS 2012, the College Navigator site was scraped for information in HTML.

To use the College Navigator, search by institution name in the search box, or use the IPEDS ID in the following url: http://nces.ed.gov/collegenavigator/?id=xxxxxx, where 'xxxxxx' is the 6-digit IPEDS ID.

##### SAT/ACT, 4-Year Degree
In the 2012 data set, SAT data was provided as 25th and 75th percentiles, for each of the three categories. ACT data was also provided as 25th and 75th percentiles, for the four categories and as the Composite score. Note that colleges may submit one or the other test, or both.  

Whether test scores were required or not, as well as the percent of students submitting was also recorded.   
In addition, 4-Year institutions were designated based on the data (Level 5 or higher)

##### Freebase Reconciliation
As part of a separate project, the old school list was matched by name to freebase IDs (m\_id). Using the Freebase Search and Reconciliation APIs, the Freebase IDs were collected for all (real) colleges. The Freebase entities for each college were then used to collect the IPEDS IDs (from the IPEDS 'namespace'). The IPEDS ID is the same as 'gov\_id' in the previous model.

##### Name Conflicts
The IPEDS Data was chosen as the authority on college names, with the exception being when a college is not found in IPEDS. A few colleges' names were taken from the corresponding College Navigator page. 

##### Joining Data

Join Accredidation list with IPEDS 2012 list, on IPEDS ID, keeping the DoE ID  
`join-accred-with-ipeds.py`  
Join the created list with the Freebase list, keeping the Freebase ID   
`join-accred-ipeds-freebase.py`    
Use 'fuzzy matching' package to find where names do not match   
`name-conflicts.py`   

##### Current process steps
`python master-script.py`  
`python master-with-sat.py`  
`python append-debt-and-default.py`   

##### Previous Colleges Schema
```ruby
create_table "colleges", :force => true do |t|
  t.integer  "university_id"
  t.integer  "median_sat_score"
  t.integer  "median_starting_salary"
  t.integer  "median_mid_career_salary"
  t.decimal  "average_annual_salary_growth_rate"
  t.datetime "created_at",                        :null => false
  t.datetime "updated_at",                        :null => false
  t.string   "name"
  t.integer  "graduation_rate"
  t.integer  "retention_rate"
  t.integer  "gov_id"
end
```

##### New Attributes
Attribute | Description
------------- | -------------
DoE ID     | Department of Education Accredidation Data ID
Freebase mid | Freebase ID '/m/XXXXXX'
OPE ID    | Department of Education Office of Postsecondary Education ID (found in IPEDS and DoE data)
Four-Year | "YES" if the institution grants four-year undergraduate degrees, otherwise "NO"
Test Scores Required | "YES" if the institution requires submission of test scores for admission, otherwise "NO"
SAT CR 25th | 25th Percentile Score on SAT Critical Reading Section (IPEDS 2012)
SAT CR 75th	| 75th Percentile Score on SAT Critical Reading Section (IPEDS 2012)
SAT M 25th	| 25th Percentile Score on SAT Math Section (IPEDS 2012)
SAT M 75th	| 75th Percentile Score on SAT Math Section (IPEDS 2012)
SAT W 25th	| 25th Percentile Score on SAT Writing Section (IPEDS 2012)
SAT W 75th	| 75th Percentile Score on SAT Writing Section (IPEDS 2012)
ACT Composite 25th	| 25th Percentile ACT Composite Score (IPEDS 2012)
ACT Composite 75th	| 75th Percentile ACT Composite Score (IPEDS 2012)
Graduation Rate	| Graduation Rate (Total cohort) from IPEDS
Retention Rate	| Retention Rate from IPEDS
Avg Debt of Graduates	|
NBD 1	| Number of student defaults (3-Year) from PayScale
NBR 1	| Number of students entered repayment (3-Year) from PayScale
DRATE | Default rate (NBD/DBR) from PayScale

####Notes:
* Previous College List size: 1982
* Colleges with Median SAT: 1342
* Colleges with Graduation Rate: 1566
* New 'master' list size: 8528
* 4-Year (undergraduate) colleges in new list: 2870
* SAT/ACT Quartile data in new list: 1434
* Number with graduation rates: 6370
* Number with average debt: 1070
* Number with default rates: 5510
Majors: http://nces.ed.gov/ipeds/cipcode/resources.aspx?y=55
