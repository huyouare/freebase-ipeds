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
* Go to [IPEDS Data Center](https://nces.ed.gov/ipeds/use-the-data).
* Under "Survey Data" section, choose "Select download option" → "Custom Data Files".
* Here it offers to search for individual institutions by their names. Since all institutions are required, we're gonna perform a hacky workaround. They also claim that "if you want all institutions on the list, click Select", except it doesn't work.
  * On the "1. Select Institutions" tab, hover "By Variables" link and choose "Browse/Search Variables".
  * Choose "Institutional Characteristics" → "Directory information" → "1980-81 to current year".
  * Select the latest (topmost leftmost) year range. Example: `2020-21`.
  * Scroll down the list of checkboxes and check the "Institution is active in current year" checkbox near the bottom of the list.
  * Click "Continue" button on the right side of the blue sticky top bar.
* The page will display a list of "My Variables".
* Click "Continue" button on the right side above "My Variables".
* Now it asks to specify a value for each of the "My Variables".
  * Click the "Institution is active in current year  - (20)" link in the list of variables. A popup will open. Choose "Yes" option. Click the small "save" button on the right side above the "Yes" option.
  * Click "Submit" button on the left side right above the list of variables.
* The page will output a list of institutions. That should be all of the "currently active" institutions.
* Click a small and stealthy "continue" button right above the list of institutions.
* Now it offers to select the variables of the institutions that will be present in the exported data. 
  * For example, assume that the data required to be present in the output is: IPEDS ID, name, city and state code.
* Choose "Institutional Characteristics" → "Directory information, institution classifications, and response status information" → "Directory information and response status". Select checkboxes:
  * ~"Institution (entity) name"~ (no need to select it here because it's already present by default)
  * "City location of institution" — Institution city.
  * ~"State abbreviation"~ (that's state name rather than state code)
  * "State and 116TH Congressional District ID" — Institution state code and some kind of a "district".
* Click "Continue" button on the right side of the blue header.
* Click "CSV" link on the right side.
* A `.zip` archive will be downloaded. Extract its contents. The CSV file name will look like `CSV_6262022-283.csv`.
* Open the `.csv` file. It will list columns:
  * `unitid` — IPEDS ID. Example: `494250`.
  * `institution name` — Institution name. Example: `Elevate Salon Institute`.
  * `year` — (ignore). Example: `2020`.
  * `HD2020.City location of institution` — Institution city (US). Example: `Cleveland`.
  * `HD2020.State and 116TH Congressional District ID` — Institution state code and some kind of a "district" (US). Example: `CA, District 27`.

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
Format the sorted list to give the columns desired  
`python master-script.py`  
Add the additional SAT quartile & percent submitting data  
`python master-with-sat.py`  
Add the additional debt and default rates data  
`python append-debt-and-default.py`   

##### US News Rescrape
Found in lib/tasks/us_news_rescrape.rake.  
Used US News Premium to gather more SAT/ACT information, rankings, acceptance rates, and HS GPAs.  
A csv was scraped  from http://premium.usnews.com/best-colleges/search?spp=10000&category=all. Then, a rake task found in lib/tasks/colleges.rake called "us_news_rescrape:scrape" is run to gather SAT/ACT fields for each college. This is imported in the "colleges:populate" rake task.

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
Name | Attribute | Description
------------- | ------------- | -------------
ipeds_id | IPEDS ID | Renamed from gov_id; the ID provides by IPEDS
doe_id | DoE ID     | Department of Education Accredidation Data ID
freebase_id | Freebase mid | Freebase ID '/m/XXXXXX'
ope_id | OPE ID    | Department of Education Office of Postsecondary Education ID (found in IPEDS and DoE data)
is_four_year | Four-Year | "YES" if the institution grants four-year undergraduate degrees, otherwise "NO"
test_scores_required | Test Scores Required | "YES" if the institution requires submission of test scores for admission, otherwise "NO"
sat_reading_25th_percentile | SAT CR 25th | 25th Percentile Score on SAT Critical Reading Section (IPEDS 2012)
sat_reading_75th_percentile | SAT CR 75th	| 75th Percentile Score on SAT Critical Reading Section (IPEDS 2012)
sat_math_25th_percentile | SAT M 25th	| 25th Percentile Score on SAT Math Section (IPEDS 2012)
sat_math_75th_percentile | SAT M 75th	| 75th Percentile Score on SAT Math Section (IPEDS 2012)
sat_writing_25th_percentile | SAT W 25th	| 25th Percentile Score on SAT Writing Section (IPEDS 2012)
sat_writing_75th_percentile | SAT W 75th	| 75th Percentile Score on SAT Writing Section (IPEDS 2012)
act_composite_25th_percentile | ACT Composite 25th	| 25th Percentile ACT Composite Score (IPEDS 2012)
act_composite_75th_percentile | ACT Composite 75th	| 75th Percentile ACT Composite Score (IPEDS 2012)
graduation_rate | Graduation Rate	| Graduation Rate (Total cohort) from IPEDS
retention_rate | Retention Rate	| Retention Rate from IPEDS
average_debt | Avg Debt of Graduates	| Average Debt of Graduates, in Dollars, from CollegeInSight 2011-2012 http://college-insight.org/#explore/go&h=44b136f4d155362e46d5da65ab244409  
num_defaults | NBD 1 | Number of student defaults (3-Year) from DoE OSFAP 2010 http://www2.ed.gov/offices/OSFAP/defaultmanagement/cdr.html
num_repayments | NBR 1 | Number of students entered repayment (3-Year) from DoE OSFAP 2010
default_rate | DRATE | Default rate (NBD/DBR) from DoE OSFAP 2010
us_news_rank | US News Ranking | Ranking as provided by US News "Best Colleges" http://premium.usnews.com/best-colleges/search?spp=10000&category=all  
us_news_category | US News Category | The category in which the college was ranked (e.g. "National Universities").
acceptance_rate | Acceptance Rate | Acceptance rate of colleges as given by US News 
high_school_gpa | High School GPA | GPA of entering freshmen from US News
sat_reading_average | SAT CR Average | Average SAT Reading score from US News, 2012
sat_math_average | SAT M Average | Average SAT Math score from US News, 2012
sat_writing_average | SAT W Average | Average SAT Writing score from US News, 2012
act_composite_average | ACT Composite Average | Average ACT Composite score from US News, 2012

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
* Number of schools added: 6764
* Number of previous schools that have new SAT/ACT data: 251
* Number of new schools added that have SAT/ACT data: 117

##### After US News Rescrape:
* Number of schools with SAT/ACT data: 2190 (858 new)
* Number of schools with graduation rate: 6503 (437 new)
* Number of schools with default rate: 5121 (5121 new)

###Migration/Rake:
1) Create backup table, copy current College table to backup  
2) Create new columns in College table  
3) Create new columns for US News  
4) Run `rake colleges:populate` to populate rows
