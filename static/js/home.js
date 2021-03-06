var app = angular.module('myApp',['timer','ngAudio']);
    app.factory('eventsCtrlFactory',function($http){
           var getConfigs = function() {
             return $http.get('/get_calendar_configs').then(function(response){
                 return response.data.result.calendar_configs;
             });
           };
           return {getConfigs: getConfigs};
       });
    app.controller('eventsCtrl', function($rootScope, $scope, $http, $timeout,eventsCtrlFactory){
        $scope.events = null;
        $scope.calendarConfigs = null;
        (function update(){
            var myDataPromise = eventsCtrlFactory.getConfigs();
            myDataPromise.then(function(result){
                $scope.calendarConfigs = result;
                $scope.getEvents($scope.calendarConfigs.itemsToDisplay);
                $timeout(update,$scope.calendarConfigs.updateTime*1000);
            });
        })();

        $scope.getEvents = function(number){
            $http.get('/get_events?num='+number)
                    .success(function(response) {
                        $scope.events = $scope.setEventsStatus(response.result.events);
                        console.log($scope.events);
                        });
        };

        $scope.setEventsStatus = function(events){

            for (var i=0; i < events.length; i++){
                if ($scope.countTime(events[i].start)>0){
                     status="pending";}
                else{
                    if ($scope.countTime(events[i].start)<0 && $scope.countTime(events[i].end)>0) {
                        status="inprogress";
                    }
                    else {
                        status="finished";
                    }
                }
                  events[i].status = status;
          }
            console.log("modified events:"+events.toString());
            return events;
        };


        $scope.formatDate = function(date)
        {
            var thisDate = new Date();
            thisDate.setTime(Date.parse(date));
            date_hours = thisDate.getHours();
            new_hours = (date_hours<10)?"0"+date_hours.toString():date_hours.toString();
            date_minutes = thisDate.getMinutes();
            new_minutes = (date_minutes<10)?"0"+date_minutes.toString():date_minutes.toString();
            return new_hours + ":" + new_minutes;
        };
        $scope.getMachineTime = function(date){
            return Date.parse(date);
        };
        $scope.getTimeNow = function(){
            //console.log(new Date().getTime());
            return new Date().getTime();
        };

        $scope.countTime = function(date) {
            var interval = Date.parse(date) - new Date().getTime();
//            console.log(interval);
            return interval;
        };
        $scope.stopTimer = function() {
          $scope.$broadcast('timer-stop');
        };
        $scope.$on('timer-stopped', function (event, data){
                console.log('Timer Stopped - data = ', data);
                $scope.setInProgress();
                $rootScope.$broadcast('playNotificationEvent');
            });
        $scope.setInProgress = function(){
            events = $scope.events;
            for (var i=0;i<events.length;i++){
                if (events[i].status == "pending") {
                    console.log("element number:" + i.toString());
                    document.getElementsByName("event")[i].setAttribute("class","inprogress");
                    $scope.events[i].status="inprogress";
                    break;
                }
            }
        };
        $scope.setEventsFinished = function(event_ids){
            for (var i=0;i< event_ids.length;i++){
                document.getElementsByName("event")[event_ids[i]].setAttribute('class','finished');
                $scope.events[event_ids[i]].status="finished";
            }
        };

        $scope.getEventClass =function(event){
            return event.status;
        };

        $scope.setColor = function(){
            document.getElementsByName("event")[1].setAttribute("class","finished");
        }
    });

    app.controller('playSound', function($scope, ngAudio){
        $scope.$on('playNotificationEvent',function(){$scope.playMusic()});
        var sound = ngAudio.load("sounds/notification.mp3");
            $scope.playMusic = function(){
              sound.play();
            };
            $scope.stopMusic = function(){
                sound.stop();
            };
            $scope.pauseMusic = function(){
              sound.pause();
            };

    });

    app.controller('jobsCtrl', function($scope,$http, $timeout){
         $scope.jobs = null;
        (function update(){
            $http.get('/get_jobs')
                    .success(function(response) {
                        $scope.jobs = response.result.jobs;
                        console.log($scope.jobs);
                    });
            $timeout(update,1000000);
        })();
        $scope.getJobClass = function(job){
          if (job.status == "SUCCESS"){
              return "success";
          }
          else {
              if (job.status == "FAILURE"){
                  return "failed";
              }
              else {
                  return "aborted";
              }
          }
        };
    });