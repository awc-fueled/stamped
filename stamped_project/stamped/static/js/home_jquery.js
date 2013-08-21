function get_map_place(output_list){
	$("#output").append("<p>"+output_list[0]+"</p>")
}
$(document).ready(function(){
	//initialize main map
	$(google.maps.event.addDomListener(window, 'load', initialize));

	//get values from google map when changed


});