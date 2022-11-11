from bs4 import BeautifulSoup
import requests


def extract_weworkremotely_jobs(term):
  url = f"https://weworkremotely.com/remote-jobs/search?utf8=✓&term={term}"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  results = []

  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    jobs = soup.find_all('li', class_="feature")

    for trs in jobs:
      job_description = trs.find_all('a')[1]
      job_link = job_description['href']
      job_company, job_position, job_region = job_description.find_all(
        'span', class_="company")
      job_title = job_description.find('span', class_="title")

      job_result = {
        'link': "https://weworkremotely.com/" + job_link,
        'company': job_company.string,
        'title': job_title.string.replace("\n", ""),
        'location': job_region.string.replace("/", ", "),
      }

      results.append(job_result)

  else:
    print("Can't get jobs.")

  return results
