$(document).ready(function(){
	//initialize main map
	$(google.maps.event.addDomListener(window, 'load', initialize));

	$("#top_choice_list").selectable();
	//or . hover
	$("#top_choice_div").mouseEnter(function(){
		$("#choice_cat_name").animate(function(){
			fontSize: '20px'
		});
		//get children of cat list eventhough cat name is one? lets see what happens
		$("#choice_cat_list li").animate(function(){
			fontSize: '14px'
		});
	});


});