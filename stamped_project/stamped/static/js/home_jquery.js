$(document).ready(function(){
	//initialize main map
	$(google.maps.event.addDomListener(window, 'load', initialize));

	$(".top_choice_list").selectable();

});