from flask import Flask, jsonify, render_template, request, send_from_directory, url_for
from flask import Flask,jsonify, render_template, request, send_from_directory, url_for,json, redirect
from support.get_jenkins_jobs import JenkinsFeatures
from support.get_calendar_events import CalendarEvents
from support.jenkins_api import JenkinsApi
import config
import configparser2
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
    return json.dumps(JenkinsFeatures().get_last_build_info())

@app.route('/showConfigure')
def showConfigure():
    return render_template('configure.html', company = config.projectname, job1 = config.jobs_list[0],
                           job2 = config.jobs_list[1], job3 = config.jobs_list[2], job4 = config.jobs_list[3],
                           project_name = config.projectname, jenkins_url = config.host, username = config.username,
                           password = config.password)

@app.route('/configure',methods=['POST'])

def configure():

    configparser = configparser2.ConfigParser()
    _project_name = request.form['projectName']
    _jenkins_url = request.form['jenkinsUrl']
    _job_1 = request.form['job1']
    _job_2 = request.form['job2']
    _job_3 = request.form['job3']
    _job_4 = request.form['job4']
    _username = request.form['username']
    _password = request.form['password']

    if _project_name and _jenkins_url and _job_1 and _job_2 and _job_3 and _job_4 and _username and _password:

        configparser['"CONFIG_PARAMS "'] = {'host':"'"+_jenkins_url+"'",
                                           'username':"'"+_username+"'",
                                           'password':"'"+_password+"'",
                                           'jobs_list':"["+"'"+str(_job_1)+"'"+","+" '"+str(_job_2)+"'"+","
                                                       +" '"+str(_job_3)+"'"+","+" '"+str(_job_4)+"'"+"]",
                                           'projectname':"'"+str(_project_name)+"'"
                                           }
        with open('config.py', 'w') as config:
            configparser.write(config)
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/home')
def home():
    JA = JenkinsApi()
    if JA.get_job()['job_status'] == 'failed':
        return render_template('home.html', status1 = 'failed', company = config.projectname )
    else:
        return 'Pass'


if __name__ == '__main__':
    app.run(debug=True)




