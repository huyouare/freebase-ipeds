require 'csv'   

rows = CSV.read('us_news_scrape.csv', :encoding => 'windows-1251:utf-8')

CSV.open("us_news_parsed.csv", "wb") do |outfile|
  outfile << ["College name", "US News Key", "Rank", "Catgory", "Acceptance rate", "High school GPA", "SAT 75th Percentile", "ACT 75th Percentile"]

  rows.each_with_index do |row, i|
    next if i == 0
    name = row[0]
    key = row[1].match("%22\/best-colleges\/(.*)\\\\%22")[1].to_s
    rank = row[2].split(',')[0].split('#')[1].to_i if row[2] =~ /\d/ 
    category = row[2].split(', ')[1]
    acceptance = row[3].split('%')[0] if row[3] =~ /\d/
    gpa = row[4] if row[4] =~ /\d/
    sat_75th_percentile = row[5].split('/')[0].to_i if row[5] =~ /\d/
    act_75th_percentile = row[5].split('/')[1].to_i if row[5] =~ /\d/
    outfile << [name, key, rank, category, acceptance, gpa, sat_75th_percentile, act_75th_percentile]
  end
end