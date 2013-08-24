$(document).ready(function(){
	//initialize main map
	$(google.maps.event.addDomListener(window, 'load', initialize));

	$(".top_choice_list").selectable();
	//or . hover
	$(".top_choice_div").mouseenter(function(){
		$(".choice_cat_name").animate({
			fontSize: '20px'
		});
		//get children of cat list eventhough cat name is one? lets see what happens
		$(".choice_cat_list li").animate({
			fontSize: '14px'
		});
	});

	$(".top_choice_div").mouseleave(function(){
		$(".choice_cat_name").animate({
			fontSize: '15px'
		});
		//get children of cat list eventhough cat name is one? lets see what happens
		$(".choice_cat_list li").animate({
			fontSize: '13px'
		});
	});

});