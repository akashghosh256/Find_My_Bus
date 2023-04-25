from flask import Flask,render_template,jsonify,request
# from database import load_jobs_from_db,load_job_from_db, add_application_to_db

 
print("yo")
app = Flask(__name__)


@app.route("/")
def hello():
 
  return  render_template('home.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/help")
def help():
  return render_template('help.html')

@app.route("/track")
def track():
  return render_template('track.html')

@app.route("/mylocation")
def mylocation():
  return render_template('mylocation.html')

@app.route("/pointlocation")
def pointlocation():
  return render_template('pointlocation.html')


@app.route("/code")
def  github():
  return render_template()

# @app.route("/job/<id>")
# def show_job(id):
#   job = load_job_from_db(id)
#   if not job:
#     return "No job found", 404 
#   return render_template('jobpage.html',job=job)
#   #return jsonify(job)


# @app.route("/job/<id>/apply", methods=['post'])
# def apply_job(id):
#    data = request.form
#    job = load_job_from_db(id)
#    add_application_to_db(data)
#    #return jsonify(data)
#    return render_template('submitted_form.html',application=data)


#print(__name__)
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug = True)
  






