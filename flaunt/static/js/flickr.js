$(document).ready(function(){
	//Flickr Integration 36334875@N04
    $.getJSON("http://api.flickr.com/services/feeds/photos_public.gne?id={{settings.PHOTO_SHARING_FLICKR_ID}}&lang=en-us&format=json&jsoncallback=?", function(data){
		$.each(data.items, function(i,item){
			if(i<=11){ // <— change this number to display more or less images
				$("<img/>").attr("src", item.media.m.replace('_m', '_s')).appendTo(".FlickrImages ul")
				.wrap("<li><a href='" + item.link + "' target='_blank' title='Flickr'></a></li>");
			}
		});			
    });	
})
