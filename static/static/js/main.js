jQuery(document).ready(function($) {	
	 $(window).on('scroll',function(){
	 	var coordinate = $(document).scrollTop();

	 	$('.menu__search_textblock, .menu__search').removeClass('active');

	 	 if (coordinate > 160) {
	 	    if ($('.menu').hasClass('menu__fixed')) return;

	 	 	$('.menu').addClass('menu__fixed');
	 	 		 	
	 	 }
	 	 else if (coordinate < 160){
	 	 	if (!$('.menu').hasClass('menu__fixed')) return;

	 	 	$('.menu').removeClass('menu__fixed');
	 	 }
	 })
	 /* search click */
	 $('.menu__search').on('click',function(e){

	 	if (!$(this).hasClass('active')) {	 		
		 	$(this).addClass('active');
		 	$('.menu__search_textblock').addClass('active')
	 	} else {	 		
	 		$(this).removeClass('active');
		 	$('.menu__search_textblock').removeClass('active')
	 	}

	 })
});
