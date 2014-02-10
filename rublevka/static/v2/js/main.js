jQuery(document).ready(function($) {
	topOffset();
    $("html").mousemove(function(){
        $('.sub_menu li:visible:first a').css('border','none');
  	 });

	//for article
	$('.article__content p:has(img,iframe)').css('margin','10px 0px');
	$('.article__content p').css('text-align','left');



	var qwerty = $('.main_content');
	if (qwerty.hasClass('for_article')){
		$('html').addClass('article');
	}

	//start topOffset() when scrolling
	$(window).scroll(function(){
		topOffset();

	});
	//up-button
	$('.up_button').on('click', function() {
		$("html, body").animate({ scrollTop: 0 }, 400);
	});
	function topOffset() {

		if ($(this).scrollTop()>400){
	        $(".up_button").fadeIn(500);     
	    }
	    else{
	        $(".up_button").fadeOut(500);
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


	//active sub-rubric color
	$('.sub_active').parent().css('color','#3575d8');


	//Добавление дата атрибута в меню
	$('.menu__item').each(function(){
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

    }).on("mouseleave",function(){
    	return;
    });

    //открытие под меню
	 $(".col-11 a").on("mouseenter",function(){
	//count of active sub-rubric
	var countSub = $('.sub_menu').find('.active').length;
		$('.sub_menu').fadeOut(200);
	//отображаем подрубрики,если их количество больше одной
	   if(countSub>1){
			$('.sub_menu').fadeIn(200);
			$('.sub_menu li').css('display','none');
			$('.sub_menu').find('.active').parent('li').css('display','inline-block');
		}


    }).on("mouseleave",function(){
    	return;
    });

    //закрываем подменю
	 $(".sub_menu").on("mouseleave",function(){

	 	var qwerty = $('.sub_menu li:visible a');
	 		console.log($(this).children());
	 	if(qwerty.children().hasClass('sub_active')){
			 return;
	 	} else $('.sub_menu').fadeOut(200);
    
	});
	 //доп.условие
		var qqqq = $('.sub_menu li:visible a');
		var countSub = $('.sub_menu').find('.active').length;
	 	if(qqqq.children().hasClass('sub_active')){
			 	 		
	 	} else {
	 			if(countSub>1){
	 				$('.sub_menu').find('.active').parent('li').css('display','inline-block');
	 				$('.sub_menu').show();
	 			}
	 	}




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
		 	$(this).addClass('active');
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
		var item = localStorage.getItem('sex');
		var slct = $('.slct');

		if (item == null) {
			slct.text('Man');
		}
		else slct.text(item);

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
			$('.main_photo__image').transition({opacity:0},100,function(){
				//$(this).attr('src', href);
				console.log(href);
				$(this).attr('style', ''+href+'');

				$(this).transition({opacity:1},100,'ease');
				animating = false;
				
			});

			},
			function () {

			}
		);

		$('.thumbnails a').on('click',function(e){
			e.preventDefault();
		});




});

