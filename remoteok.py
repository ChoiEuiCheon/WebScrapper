from bs4 import BeautifulSoup
import requests


def extract_remoteok_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  results = []
  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")

    jobs = soup.find_all('tr', class_="job")
    for trs in jobs:
      job_posts = trs.find('td',
                           class_="company position company_and_position")
      job_description = job_posts.find('a', class_="preventLink")
      job_link = job_description['href']
      job_title = job_posts.find('h2')
      job_company = job_posts.find('h3')
      job_locations = job_posts.find_all('div', class_="location")
      salary = ""
      contract = ""
      locations = []
      for element in job_locations:
        if "$" in element.string:
          salary = element.string
        elif "⏰" in element.string:
          contract = element.string
        else:
          locations.append(element.string)
      job_result = {
        'link': "https://remoteok.com/" + job_link,
        'title': job_title.string.replace("\n", ""),
        'company': job_company.string,
        'location': ', '.join(locations)
      }
      results.append(job_result)
  else:
    print("Can't get jobs.")

  return results
