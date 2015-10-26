#from jenkinsapi.jenkins import Jenkins
import jenkins
import config
import json


class JenkinsFeatures():
    host = config.host
    username = config.username
    password = config.password
    server = jenkins.Jenkins(host, username=username, password=password)
    jobs_list = config.jobs_list

    def get_jenkins_log(self):
        J = jenkins.Jenkins('http://erebor.ct.pb.com/')
        return J['test_saas-shipping-ui_custom_suite'].get_last_good_build().get_console()

    def get_last_build_info(self):
        response = []

        for job in self.jobs_list:
            job_info = self.server.get_job_info(job)
            last_build_info = self.server.get_build_info(job, job_info['lastCompletedBuild']['number'])

            if last_build_info['result'] == 'SUCCESS' or last_build_info['result'] == 'ABORTED':
                response.append(dict(fullName=last_build_info['fullDisplayName'],
                                      status=last_build_info['result']))

            elif last_build_info['result'] == 'FAILURE':
                response.append(dict(fullName=last_build_info['fullDisplayName'],
                                      status=last_build_info['result'],
                                      startedBy=last_build_info['actions'][1]['causes'][0]['userName']))
        return response