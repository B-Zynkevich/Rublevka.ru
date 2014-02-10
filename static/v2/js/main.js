jQuery(document).ready(function($) {

	//for article
	$('.article__content p:has(img,iframe)').css('margin','10px 0px');
	$('.article__content p').css('text-align','left');


    $(window).load(function() {



  	});
  	

	//start topOffset() when scrolling
	$(window).scroll(function(){
		topOffset();
	});
	//up-button
	$('.up_button').on('click', function() {
		$("html, body").animate({ scrollTop: 0 }, 400);
	});
	function topOffset() {
		var upButton = $(".up_button");
		if ($(this).scrollTop()>400){
	        upButton.fadeIn(500);     
	    }
	    else{
	        upButton.fadeOut(500);
	    }
	}

	/* main menu */	
	$(window).on('scroll',function(){

	 	var coordinate = $(document).scrollTop();
	 	$('._4s7c').css('width','235px');
	 	$('.menu__search_textblock, .menu__search').removeClass('active');

	 	 if (coordinate > 160) {
	 	    if ($('.menu').hasClass('menu__fixed')) return;
	 	    $('.menu').removeClass('menu__absolute');
	 	 	$('.menu').addClass('menu__fixed');	 	 		 	
	 	 }
	 	 else if (coordinate < 160){
	 	 	if (!$('.menu').hasClass('menu__fixed')) return;

	 	 	$('.menu').removeClass('menu__fixed');
	 	 	$('.menu').addClass('menu__absolute');
	 	 }
	 });

	//sub-menu


	//Добавление дата атрибута в меню
	$('.col-11 > a').each(function(){
			var rubric = $(this).text();
		$(this).attr('data-rubric',rubric);
	});

	//Добавление дата атрибута в под меню
	$('.sub_menu span').each(function(){
		var rubric = $(this).text();
		$(this).attr('data-rubric',rubric);

	});

	//Событие при наведении на рубрику
	 $(".col-11 a").on("mouseenter",function(){
	//count of active sub-rubric
		var rubricName = $(this).attr('data-rubric');
		//перебираем дата атрибуты в под меню
		$('.sub_menu li').each(function(){
			subRubric = $(this).find('.rubric_name').attr('data-rubric');
			if (subRubric == rubricName){
				$(this).find('a').addClass('active');
			} else $(this).find('a').removeClass('active');
		});


		//count of active sub-rubric
		var countSub = $('.sub_menu').find('.active').length;
		$('.sub_menu').fadeOut(200);
		//отображаем подрубрики,если их количество больше одной
	   if(countSub>1){
			$('.sub_menu').fadeIn(200);
			$('.sub_menu li').css('display','none');
			$('.sub_menu').find('.active').parent('li').css('display','inline-block');
		} else return;


    }).on("mouseleave",function(){
    	return;
    });

    //закрываем подменю
	 $(".sub_menu").on("mouseleave",function(){
			 $(this).fadeOut(200);;
	});







		//Close dropdown function
	function closeDropdown() {
		$('._dropdown.active').removeClass('active');
		$('.drop').slideUp();
	}

		/* search click */
	$('.menu__search').on('click',function(e){
	 	if (!$(this).hasClass('active')) {
	 		closeDropdown();	 		
		 	$(this).addClass('active');
		 	$('.menu__search_textblock').addClass('active')
	 	} else {	 		
	 		$(this).removeClass('active');
		 	$('.menu__search_textblock').removeClass('active')
	 	}

	 });
		/* more click */
	$('.menu__more').on('click',function(e){
	 	if (!$(this).hasClass('active')) {	 
	 		closeDropdown();		

		 	$('.menu__more_textblock').addClass('active')
	 	} else {	 		
	 		$(this).removeClass('active');
		 	$('.menu__more_textblock').removeClass('active')
	 	}

	 });
		// Dropdown
	$('.slct').click(function(){
		/* Заносим выпадающий список в переменную */
		var dropBlock = $(this).parent().find('.drop');
		/* Делаем проверку: Если выпадающий блок скрыт то делаем его видимым*/
		if( dropBlock.is(':hidden') ) {
			closeDropdown();
			dropBlock.slideDown(200);
			/* Выделяем ссылку открывающую select */
				$(this).addClass('active');

			/* Работаем с событием клика по элементам выпадающего списка */
			dropBlock.find('li').click(function(){
					
				/* Заносим в переменную HTML код элемента 
				списка по которому кликнули */
				var selectResult = $(this).html();
				
				/* Находим наш скрытый инпут и передаем в него 
				значение из переменной selectResult */
				$(this).parent().parent().find('input').val(selectResult);
				
				/* Передаем значение переменной selectResult в ссылку которая 
				открывает наш выпадающий список и удаляем активность */
				$('.slct').removeClass('active').html(selectResult);
				
				/* Скрываем выпадающий блок */
				dropBlock.slideUp();
			});
			
		/* Продолжаем проверку: Если выпадающий блок не скрыт то скрываем его */
		} else {
			$(this).removeClass('active');
			dropBlock.slideUp();
		}

		/* Предотвращаем обычное поведение ссылки при клике */
		return false;
	});	



	// localStorage for sex
	$('.drop a').on('click',function(){ 
		var text = $(this).text();
		localStorage.setItem('sex', text);
	 });
		//var item = localStorage.getItem('sex');
		var slct = $('.selected_sex').text();
		$('.slct').text(slct);
	//	if (item == null) {
	//		slct.text('All');
//		}
	//	else slct.text(item);

	//	if(location.href == 'http://rublevka.com/'){
//			slct.text('All');
//		} else ;


	  // localStorage for menu
   /*
	  $('.col-11 a,menu__more_textblock a').on('click',function(){ 
	    var text = $(this).text();
	    localStorage.setItem('active_menu', text);
	   });
	    var item = localStorage.getItem('active_menu');
	    $('.menu__item').each(function(){
	      var menuLink = $(this).text();
	      if(menuLink == item){
	          $('.menu__item').removeClass('active_menu');
	          $(this).addClass('active_menu');
	      } else return;

	    });

	    

	   //additional conditions
	    var main_photo__rubric = $('.main_photo__rubric').text();
	    $('.menu__item').each(function(){
	    	if($(this).text() == main_photo__rubric){
	    		$(this).addClass('active_menu');
	    	} else ;
	    });
	   	$('.sub_menu a').each(function(){
	    	if($(this).text() == main_photo__rubric){
	    		$(this).addClass('active_subrubric');
	    	} else ;
	    });
	*/
	   	var mainURL = (window.location.href);
	   	if( mainURL.match('news')!= null ){
	   		$('#news_list').addClass('active_menu');
	   	} else if( mainURL.match('life')!= null ){
	   		$('#life').addClass('active_menu');
	   	} else if( mainURL.match('blog')!= null ){
	   		$('#blog_list').addClass('active_menu');
	   	}


	//show blog and news only on main page
/* пока что не надо
		if ($('.menu a').hasClass('active_menu')){
			
		} else $('.main_content').addClass('main');
*/

	//clean Local storage 
	$('.logo').on('click', function(){
		window.localStorage.clear();
		location.reload();
	});

	/* Цвет для пола */
	var	sex_text = $('.slct').text();
	var sex_color = $('.slct');
	
		if(sex_text == 'Man'){
			sex_color.addClass('forMan').removeClass('forWoman').removeClass('forAll');
		}
		else if (sex_text == 'Woman'){
			sex_color.addClass('forWoman').removeClass('forMan').removeClass('forAll');
		}
		else if(sex_text == 'All')sex_color.addClass('forAll').removeClass('forMan').removeClass('forWoman');



	/* socials tabs */
	$('.social_network td').on('click',function(e){ 		
		 	$(this).addClass('active').siblings('td').removeClass('active');

		 	if($(this).hasClass('fb-tab')){
		 		$('.fb-wrapper').show().siblings('div').hide();
		 	}
		 	else if ($(this).hasClass('tw-tab')){
		 		$('.tw-wrapper').show().siblings('div').hide();
		 	}
		 	else if ($(this).hasClass('vk-tab')){
		 		$('.vk-wrapper').show().siblings('div').hide();
		 	}
		 	else $('.ins-wrapper').show().siblings('div').hide();

	 });
	
	/* thumbnails*/

	var animating = false;

	if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Mac') != -1 && navigator.userAgent.indexOf('Chrome') == -1) {      
        $('html').addClass('safari-mac');
	}



		$('.thumbnails a').hover(
			function () {
				$(this).addClass('active').siblings('a').removeClass('active');	

			if (animating) return;
				var href = $(this).attr('style');
				if ($('.top-slider .main img').attr('src') == href)	return;

				var main_photo__image = $('.main_photo__image');
				var main_photo__hdr = $('.main_photo__hdr');
				var headimp = $(this).attr('data-header');
				var articlehref = $(this).attr('href');
				var rubric = $(this).attr('data-rubric-main');
				var main_photo__rubric = $('.main_photo__rubric');

				main_photo__hdr.text(headimp);
				main_photo__hdr.attr('href', ''+articlehref+'');
				main_photo__rubric.text(rubric);


				main_photo__image.parent().attr('href', ''+articlehref+'');

				main_photo__image.transition({opacity:0},100,function(){
					$(this).attr('style', ''+href+'');
					$(this).transition({opacity:1},100,'ease');
					animating = false;
				});

				},
			function () {

		});

		$('.thumbnails a,.main_photo__rubric').on('click',function(e){
			e.preventDefault();
		});

/*
		//отображение 4 важных статей
		$('.important').each(function(i,item){

			var hrefimp = $(this).siblings('.article_anonce__photo').find('a').attr('href');
			var imgimp = $(this).siblings('.article_anonce__photo').find('img').attr('src');
			var headimp = $(this).siblings('.article_anonce__header').text();
			var rubrickimp = $(this).siblings('a').find('.rubric_label').text();

			console.log(rubrickimp);

			$('.thumbnails a:eq('+i+')').attr('href', hrefimp);
			$('.thumbnails a:eq('+i+')').attr('style', 'background:url('+imgimp+')');
			$('.thumbnails a:eq('+i+')').attr('data-header', ''+headimp+'');
			$('.thumbnails a:eq('+i+')').attr('data-rubric-main', ''+rubrickimp+'');

			if(i == 4 ) return false;
			
		});
*/

		var firstThumbBG = $('.thumbnails a:first').css('background-image');
		var firstThumbHref = $('.thumbnails a:first').attr('href');
		var firstThumbHeader = $('.thumbnails a:first').attr('data-header');
		var firstThumbHRubrick = $('.thumbnails a:first').attr('data-rubric-main');

		$('.main_photo__image').attr('style', 'background-image:'+firstThumbBG+'').parent().attr('href', firstThumbHref);
		$('.main_photo__hdr').attr('href', firstThumbHref);
		$('.main_photo__hdr').text(firstThumbHeader);
		$('.main_photo__rubric').text(firstThumbHRubrick);

});

