from wwk import extract_weworkremotely_jobs
from remoteok import extract_remoteok_jobs
from flask import Flask, render_template, request, redirect

app = Flask("JobScrapperWeb")


@app.route("/")
def home():
  return render_template("home.html")


db = {}


@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None or keyword == "":
    return redirect("/")
  if keyword in db:
    jobs = db[keyword]
  else:
    remoteok = extract_remoteok_jobs(keyword)
    wework = extract_weworkremotely_jobs(keyword)
    jobs = remoteok + wework
    db[keyword] = jobs

  return render_template("search.html", keyword=keyword, jobs=jobs)


app.run("0.0.0.0")
