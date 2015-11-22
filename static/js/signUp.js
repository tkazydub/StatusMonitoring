/**
 * Created by aparmon on 10/18/15.
 */
$(function(){
	$('#btnConfigureJenkins').click(function(){

		$.ajax({
			url: '/configure',
			data: $('#jenkinsConfiguration').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});