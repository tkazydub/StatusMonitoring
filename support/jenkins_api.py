__author__ = 'aparmon'
import jenkins
import json

class JenkinsApi():
	def get_job(self):
		server = jenkins.Jenkins('http://ci-netpulse.cogniance.com/', username='kid911', password='f0da03e34dec1f4d323ae83e9fe45ced')

		job_info = server.get_job_info('DEV Galaxy Server Build')
		json_job_info = json.dumps(job_info)

		print("Last completed build number:\n%s" % job_info['lastCompletedBuild']['number'])
		# TODO: Add get last build status for further UI variations
		print("Last stable build number:\n%s" % job_info['lastStableBuild']['number'])
		print("Last failed build number:\n%s" % job_info['lastFailedBuild']['number'])

		failed_job_info = server.get_build_info('DEV Galaxy Server Build', job_info['lastFailedBuild']['number'])
		json_failed_job_info = json.dumps(json.dumps(failed_job_info))

		print("Last failed build branch:\n%s" % failed_job_info['actions'][0]['parameters'][0]['value'])
		# print("Last commit to failed build:\n%s" % failed_job_info['changeSet']['items'][0]['msg'])
		return {'job_status': 'failed'}