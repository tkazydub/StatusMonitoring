from jenkinsapi.jenkins import Jenkins
import jenkins
import config
import re

class JenkinsFeatures():
    host = config.host
    username = config.username
    password = config.password
    server = jenkins.Jenkins(host, username=username, password=password)
    jobs_list = config.jobs_list
    jj = Jenkins(host, username=username, password=password)


    def get_jenkins_log(self):
        J = jenkins.Jenkins('http://erebor.ct.pb.com/')
        return J['test_saas-shipping-ui_custom_suite'].get_last_good_build().get_console()

    def get_last_build_info(self):
        response2 = []

        commits =''
        committers = []

        for job in self.jobs_list:
            job_info = self.server.get_job_info(job)
            last_build_info = self.server.get_build_info(job, job_info['lastCompletedBuild']['number'])

            test_build = self.jj.get_job(job).get_build(job_info['lastCompletedBuild']['number'])
            branch = test_build.get_revision_branch()[0].get('name')

            if not last_build_info['changeSet']["items"]:
                commits = 'No Commits'
            else:
                commits = last_build_info['changeSet']["items"][0]['msg']

            if last_build_info['actions'][5]:
                tests = last_build_info['actions'][5]
            else:
                tests = dict(message='No tests were ran on this build.')
            try:
                _build_name = re.search('(.*?) #(\d+)', last_build_info['fullDisplayName']).group(1)
            except AttributeError:
                _build_name = last_build_info['fullDisplayName']

            for i in last_build_info['changeSet']["items"]:
                if i['causes']:
                    try:
                        started_by = last_build_info['actions'][1]['causes'][0]['userName']
                    except KeyError:
                        started_by = last_build_info['actions'][1]['causes'][0]['shortDescription']

            if not last_build_info['changeSet']["items"]:
                committers.append('No Commits')
            else:
                for item in last_build_info['changeSet']["items"]:
                    committers.append(item['author']['fullName'])

            if last_build_info['result'] == 'SUCCESS' or last_build_info['result'] == 'ABORTED':
                response2.append(dict(fullName=_build_name,
                                      buildNumber=last_build_info['number'],
                                      status=last_build_info['result'],
                                      branch=branch,
                                      startedBy=started_by,
                                      committers=committers,
                                      commits=commits,
                                      testsFailed=str(tests['message'])))

            elif last_build_info['result'] == 'FAILURE':
                # for item in last_build_info['changeSet']['items']:
                    # commits.append(dict(message=item['msg'], author=item['author']['fullName']))
                response2.append(dict(fullName=_build_name,
                                      buildNumber=last_build_info['number'],
                                      status=last_build_info['result'],
                                      branch=branch,
                                      startedBy=started_by,
                                      committers=committers,
                                      commits=commits,
                                      testsFailed=str(tests['message'])))
        return response2

    def get_configs(self):
        jobs_list = []
        jobs = config.jobs_list
        index = 1
        for j in jobs:
            jobs_list.append({"name": j, "index": index})
            index += 1
        return {
                "project_name": config.projectname,
                "host": config.host,
                "username": config.username,
                "password": config.password,
                "jobs": jobs_list}
