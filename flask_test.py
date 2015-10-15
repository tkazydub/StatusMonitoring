from flask import Flask,jsonify, render_template, request
from support.get_jenkins_jobs import JenkinsFeatures
from support.get_calendar_events import CalendarEvents
from support.database import WriteToDb
app = Flask(__name__)


DATABASE = 'support/test.db'
db = WriteToDb(DATABASE)

@app.route('/')
def hello_world():
    # return render_template("index.html")
    return "lol"


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


# @app.route('/events')
# def events():
#     db.write_events_to_db(CalendarEvents().get_events())
#     db.print_db()
#     return "Events were successfully fetched!"


@app.route('/index')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route("/events", methods=['GET'])
def echo():
    return str(CalendarEvents().get_events())

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         pass
#     db.close()

if __name__ == '__main__':
    app.run()




