from jenkinsapi.jenkins import Jenkins
class JenkinsFeatures():
    def get_jenkins_log(self):
        J = Jenkins('http://erebor.ct.pb.com/')
        return J['test_saas-shipping-ui_custom_suite'].get_last_good_build().get_console()