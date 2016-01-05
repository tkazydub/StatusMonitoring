var app = angular.module('myApp',[]);
    app.controller('configs', function($rootScope, $scope, $http){
        $scope.calendarConfigs = null;
        $scope.jenkinsConfigs = null;
        (function getJenkinsConfigs(){
            $http.get('/get_jenkins_configs')
                    .success(function(response) {
                        $scope.jenkinsConfigs = response.result.jenkins_configs;
                    });
        })();
        (function getCalendarConfigs(){
            $http.get('/get_calendar_configs')
                    .success(function(response){
                        $scope.calendarConfigs = response.result.calendar_configs;
                    });
        })();
    });
    function showToolTip(){
        $("#jenkinsConfiguration :input").tooltip({position :"bottom left"});
    }
    (function($) {
  		$(document).ready(function(){
  			var count = $('div[id^="inputJob-"]').length;
            console.log("number of elements = " + count);
			if (count < 2) $('.removeJob').attr('disabled','disabled');
			$(document)
				.on('click', '#add_job', function() {
			  		var $input = $('div[id^="inputJob-"]:last');
			  		var num = parseInt($input.prop("id").match(/\d+/g),10)+1;
			  		var $newJob =
			  			$input.clone().attr('id','inputJob-'+num)
			  			.find('input').attr({id: 'job-'+num, name: "jenkins_job-"+num}).val("").end();
			  		$input.after($newJob);
                    count = $('div[id^="inputJob-"]').length;
                    console.log("number of elements = " + count);
			  		if (count > 1) $('.removeJob').removeAttr('disabled');
			 	})
			  	.on("click",'.removeJob',function(){
			  		$(this).closest('div').remove();
                    count = $('div[id^="inputJob-"]').length;
                    console.log("number of elements = " + count);
			  		if (count < 2) $('.removeJob').attr('disabled','disabled');
			  	});
  		});
	})(jQuery);

function showDiv() {
            var congratsMessage, errorMessage, projectName, jenkinsUrl, job1, job2, job3, job4, username, password;
            congratsMessage = document.getElementById("okDiv");
            errorMessage = document.getElementById("errorDiv");
            projectName = document.getElementById("projectName").value;
            jenkinsUrl = document.getElementById("jenkinsUrl").value;
//            job1 = document.getElementById("job-1").value;
//            job2 = document.getElementById("job-2").value;
//            job3 = document.getElementById("job-3").value;
//            job4 = document.getElementById("job-4").value;
            username = document.getElementById("username").value;
            password = document.getElementById("password").value;

            document.getElementById('okDiv').style.display = "none";
            document.getElementById('errorDiv').style.display = "none";
            document.getElementById('projectName').style.border = "";
            document.getElementById('jenkinsUrl').style.border = "";
            document.getElementById('username').style.border = "";
            document.getElementById('password').style.border = "";
//            document.getElementById('jobs').style.border = "";

            try {
              if(projectName == "") throw "projectName";
              if(jenkinsUrl == "") throw "jenkinsUrl";
              if(job1 == ""&&job2 == ""&&job3 == ""&&job4 == "") throw "jobs";
              if(username == "") throw "username";
              if(password == "") throw "password";
              document.getElementById('okDiv').style.display = "block";

            }
            catch(err) {

              if(err != "jobs") {
                document.getElementById('errorDiv').innerHTML = "Please enter " + err;
              } else {
              document.getElementById('errorDiv').innerHTML = "Please enter at least one Job"
              }
              document.getElementById('errorDiv').style.display = "block";
              document.getElementById(err).style.border = "solid red";
            }

          }