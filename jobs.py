import requests, os, json, time, argparse, threading, urllib
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='This will collect a JSON for job listings from Glassdoor.')
parser.add_argument('job', action="store", help="Ex. Software Engineer")
parser.add_argument('level', action="store", help="all, entrylevel, fulltime, parttime, apprenticeship, etc")
parser.add_argument('count',action="store", help="Amount of Jobs to pull (Incr. of 30)")
args = parser.parse_args()

level = urllib.quote_plus(args.level)
job = urllib.quote_plus(args.job)
jobCount = int(args.count)

listingArray = []

#File to input jobs to
JSON = "../glassdoorJobAPI/json/glassdoorURL-" + job + "+" + level + ".json"

def main():
    pages=jobCount/30
    
    print "\n+-------------------------------------------"
    print "| We're trying to get " + str(pages*30) + " jobs via " + str(pages) + " pages."
    print "| Getting "+ level + " " + job + " jobs."
    print "+-------------------------------------------"
    
    print "\nPinging glassdoor to see if they're online:\n"
    ping = os.system("ping -c 1 glassdoor.com" )
    if ping == 0:
        open(JSON, 'w').close()
        getListing(pages)
    else:
        print "\n\nUhhh This is Awkard: The ping never reached Glassdoor. It's likely they're job listing service is down.\n\n"

def getListing(pages):
    page = 1
    jobListings = []
    contentURL = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + job + "&jobType=" + level
    while (page <= pages): 
        jl = {}
        print "\nURL that we're getting jobs from: "+contentURL
        webPage = requests.get(contentURL, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        
        if (page == 1):
            pageUrl = webPage.content.split("untranslatedUrl' : '")[1].split('.htm')[0]
        contentURL = pageUrl +'_IP'+ str(page + 1) + '.htm?jobType=' + level
    
        soup = BeautifulSoup(webPage.content, 'html.parser')
        soup = soup.select('span[data-job-id]')
        for span in soup:
            jl = {"jobID":span['data-job-id']}
            jobListings.append(jl)
       
        print "\nWe now have: " + str(len(jobListings)) + " URLs in our list.\n"
        
        page += 1
    print "Finished getting Glassdoor URLs.\n"
    
    starttime = time.time()
    getRealURL(jobListings)
    with open(JSON, 'w+') as file:
        json.dump(listingArray, file, indent=4)
    endtime = time.time()
    
    print "Total Time Taken: %s seconds" % (endtime-starttime)

def getRealURL(jobListings):
    
    failCount = 0
    
    totalPosts = len(jobListings)
    
    for line in jobListings:
        jobID = line['jobID']
        line['url'] = "https://www.glassdoor.com/partner/jobListing.htm?jobListingId="+jobID
        print "Trying to get final url for job ID: "+jobID
        try:
            page = requests.get(line['url'], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            line['FinalURL'] = page.url
            print "Got it -> "+line['FinalURL']
        except:
            print "Failed"
            line['FinalURL'] = ""
            failCount += 1
        line['url'] = "https://www.glassdoor.com/job-listing/JV.htm?jl="+jobID
    
    gatherJob(jobListings)    
        
    print "\nFinished getting final URLs: Out of "+str(totalPosts)+" total listings, "+str(totalPosts-failCount)+" URLs were successful"

def gatherJob(joblistings):
    print "\nTrying to gather listing information now.\n"
 
    for listing in joblistings:
        page = requests.get(listing['url'], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            soup = str(soup).split('<script type="application/ld+json">')[1].split('</script>')[0].replace("&lt;","<").replace("&gt;",">").replace("\n","").replace("\r","")
            listingJSON = json.loads(soup)
            listingJSON['FinalURL'] = listing['FinalURL']
            listingArray.append(listingJSON)
            print "Got info for job: "+listingJSON['url']
        except Exception as err:
            print "We couldn't get the job information at URL: " +listing['url']
            #print "\nError: "+str(err)+"\n"


if __name__ == "__main__":
    main()
