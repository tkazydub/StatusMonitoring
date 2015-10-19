#from jenkinsapi.jenkins import Jenkins
import jenkins
import config
import json


class JenkinsFeatures():
    host = config.host
    username = config.username
    password = config.password
    server = jenkins.Jenkins(host, username=username, password=password)

    def get_jenkins_log(self):
        J = jenkins.Jenkins('http://erebor.ct.pb.com/')
        return J['test_saas-shipping-ui_custom_suite'].get_last_good_build().get_console()

    def get_last_build_info(self, name):
        job_info = self.server.get_job_info(name)
        last_job_info = self.server.get_build_info(name, job_info['lastCompletedBuild']['number'])
        last_build_info = json.dumps({"fullDisplayName": last_job_info['fullDisplayName'],
                                      "status": last_job_info['result'],
                                      "building": last_job_info['building']})
        return last_build_info