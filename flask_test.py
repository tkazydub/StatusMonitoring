from flask import Flask, jsonify, render_template, request, send_from_directory, url_for
from flask import Flask,jsonify, render_template, request, send_from_directory, url_for,json, redirect
from support.get_jenkins_jobs import JenkinsFeatures
from support.get_calendar_events import CalendarEvents
from support.jenkins_api import JenkinsApi
import config
from support.database import WriteToDb
from flask.ext.triangle import Triangle
#
app = Flask(__name__)
Triangle(app)

# DATABASE = 'support/test.db'
# db = WriteToDb(DATABASE)

@app.route('/', methods=['GET'])
def hello_world():
    # return render_template("index.html")
    return redirect(url_for("home"))


@app.route('/get_events')
def get_events():
    events = CalendarEvents().get_events()
    if request.args.get('type',0,type=str) == "all":
        return jsonify(result=events)
    else:
        return jsonify(result={"events":events,"count":len(events)})


@app.route('/jenkins-status')
def jenkins():
    return JenkinsFeatures().get_jenkins_log()

@app.route('/bower_components/<path:path>')
def send_js(path):
    print("path: " + str(path))
    return send_from_directory("bower_components",path)

@app.route('/index/sounds/<path:path>')
def send_sound(path):
    print("path: " + str(path))
    return send_from_directory("sounds",path)

@app.route('/index/')
def index():
    return 'index'

@app.route("/events", methods=['GET'])
def echo():
    return str(CalendarEvents().get_events())

@app.route('/LastBuild', methods=['GET'])
def last_build():
    JenkinsFeatures().get_last_build_info()

@app.route('/showConfigure')
def showConfigure():
    return render_template('configure.html', company = config.projectName)

@app.route('/configure',methods=['POST'])

def configure():

    _project_name = request.form['projectName']
    _jenkins_url = request.form['jenkinsUrl']
    _job_name = request.form['jobName']

    params = [_project_name, _jenkins_url, _job_name]
    # print(params)
    jobs = {1:[],2:[],3:[],4:[]}

    if _project_name and _jenkins_url and _job_name:
        f = open('config.py', 'w')
        for key in jobs:
            print("first   " + str(key))
            if _project_name == 'job'+str(key):
                jobs[key] = params
                print(jobs[key])
                print("pass  " + str(key))
                f.write('# '+ str(jobs[key][0]) + ':' + '\n' + 'projectName=' + "'" + str(jobs[key][0]) + "'" + '\n')
                f.write('jenkinsUrl=' + "'" + str(jobs[key][1]) + "'" + '\n')
                f.write('jobName=' + "'" + str(jobs[key][2]) + "'" + '\n')
            else:
                pass

        f.close()


        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/home')
def home():
    JA = JenkinsApi()
    if JA.get_job()['job_status'] == 'failed':
        return render_template('home.html', status1 = 'failed', company = config.projectName )
    else:
        return 'Pass'


if __name__ == '__main__':
    app.run(debug=True)




