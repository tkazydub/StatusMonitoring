from flask import Flask,jsonify, render_template, request, send_from_directory, url_for,json, redirect
from support.get_jenkins_jobs import JenkinsFeatures
from support.get_calendar_events import CalendarEvents
from support.jenkins_api import JenkinsApi
import config, re, configparser2
from flask.ext.triangle import Triangle

app = Flask(__name__)
Triangle(app)


@app.route('/')
def hello_world():
    return redirect(url_for("home"))


@app.route('/index')
def index():
    return redirect(url_for("home"))


@app.route('/get_events')
def get_events():
    events = CalendarEvents().get_events()
    num = request.args.get('num',0,type=str)
    if num and num.isdigit():
        return jsonify(result={"events":events[0:int(num)]})
    else:
        return jsonify(result={"events":events,"count":len(events)})


@app.route('/jenkins-status')
def jenkins():
    return JenkinsFeatures().get_jenkins_log()


@app.route('/bower_components/<path:path>')
def send_js(path):
    return send_from_directory("bower_components",path)


@app.route('/sounds/<path:path>')
def send_sound(path):
    return send_from_directory("sounds",path)


@app.route('/LastBuild', methods=['GET'])
def last_build():
    return json.dumps(JenkinsFeatures().get_last_build_info())


@app.route('/showConfigure')
def showConfigure():
    return render_template('configure.html')

@app.route('/get_jenkins_configs')
def get_jenkins_configs():
    jenkins_configs = JenkinsFeatures().get_configs()
    return jsonify(result={"jenkins_configs":jenkins_configs})

@app.route('/get_calendar_configs')
def get_calendar_configs():
    calendar_configs = CalendarEvents().get_configs()
    return jsonify(result={"calendar_configs":calendar_configs})

@app.route('/configure_jenkins',methods=['POST'])
def configure_jenkins():
    configparser = configparser2.ConfigParser()
    jConfigs = request.form.to_dict()
    jobs_list = [value for key, value in jConfigs.items() if re.search("jenkins_job-", key)]

    if jConfigs['jenkinsUrl'] and jConfigs['username'] and jConfigs['password'] and jobs_list and jConfigs['projectName']:
        configparser['"CONFIG_PARAMS "'] = {'host': "'" + str(jConfigs['jenkinsUrl'])+"'",
                                           'username': "'"+ str(jConfigs['username']) + "'",
                                           'password': "'" + str(jConfigs['password'])+ "'",
                                           'jobs_list': jobs_list,
                                           'projectname':"'" + str(jConfigs['projectName']) + "'"
                                           }
        with open('config.py', 'w') as config:
            configparser.write(config)
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route('/configure_calendar',methods=['POST'])
def configure_calendar():
    c_configs = request.form.to_dict()
    CalendarEvents().save_configs(c_configs)
    return json.dumps({'Response':'Configs were successfully saved'})

@app.route('/home')
def home():
    JA = JenkinsApi()
    if JA.get_job()['job_status'] == 'failed':
        return render_template('home.html', status1 = 'failed', company = config.projectname )
    else:
        return 'Pass'


@app.route('/get_jobs')
def get_jobs():
    JA = JenkinsFeatures()
    response = JA.get_last_build_info()
    return jsonify(result={"jobs":response})


@app.route('/test')
def test():
    JA = JenkinsFeatures()
    response = JA.get_last_build_info()
    return render_template('home.html', status1 = response[0]['status'], name1 = response[0]['fullName'], company = config.projectname,
                            status2 = response[1]['status'], name2 = response[1]['fullName'],
                            status3 = response[2]['status'], name3 = response[2]['fullName'],
                            status4 = response[3]['status'], name4 = response[3]['fullName']
                           )

    # if JA.get_last_build_info():
    # 	 return render_template('home.html', status1 = 'failed', company = config.projectname )

    # if JA.get_job()['job_status'] == 'failed':
    #     return render_template('home.html', status1 = 'failed', company = config.projectname )
    # else:
    #     return 'Pass'





if __name__ == '__main__':
    app.run(debug=True)




