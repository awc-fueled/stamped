$(document).ready(function(){
	//initialize main map
	$(google.maps.event.addDomListener(window, 'load', initialize));

	//fadeIn dashboard
	$(".top_choice_list").fadeIn(1000);
	$("#recently_added_Restaurants").fadeIn(1000);
	$("#recent_reviews").fadeIn(1000);


});