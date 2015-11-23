#from jenkinsapi.jenkins import Jenkins
import jenkins
import config
import re

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
        response2 = []
        commits = []

        for job in self.jobs_list:
            job_info = self.server.get_job_info(job)
            last_build_info = self.server.get_build_info(job, job_info['lastCompletedBuild']['number'])

            if last_build_info['actions'][5]:
                tests = last_build_info['actions'][5]
            else:
                tests = dict(message='No tests were ran on this build.')
            try:
                _build_name = re.search('(.*?) #(\d+)', last_build_info['fullDisplayName']).group(1)
            except AttributeError:
                _build_name = last_build_info['fullDisplayName']

            if last_build_info['result'] == 'SUCCESS' or last_build_info['result'] == 'ABORTED':
                response2.append(dict(fullName=_build_name,
                                      buildNumber=last_build_info['number'],
                                      status=last_build_info['result']))

            elif last_build_info['result'] == 'FAILURE':
                for item in last_build_info['changeSet']['items']:
                    commits.append(dict(message=item['msg'], author=item['author']['fullName']))
                response2.append(dict(fullName=_build_name,
                                      buildNumber=last_build_info['number'],
                                      status=last_build_info['result'],
                                      startedBy=last_build_info['actions'][1]['causes'][0]['userName'],
                                      commits=commits, testsFailed=tests))
        return response2

    def get_configs(self):
        jobs_list = []
        jobs = config.jobs_list
        index = 1
        for j in jobs:
            jobs_list.append({"name":j,"index": index})
            index+=1
        return {
                "project_name": config.projectname,
                "host": config.host,
                "username":config.username,
                "password":config.password,
                "jobs":jobs_list}
