     
    
    function project_modal_function(x) {

        
        $.post('/openmodalproject', {project: x}, function(data){
        
            data = JSON.parse(data)

            $("#myModal_reliant").empty();

            var project = data['project_modal'][0]

            var strhtmlmodal ='<section id="section_projects_3">'                
                    strhtmlmodal +='<div class="container">'

                    strhtmlmodal +='<div class="row" style="margin-left: 0px;margin-right: 0px;">'
                    strhtmlmodal +='<div class="col-md-9 col-12 rel_snippet5_loc">'
                    strhtmlmodal +='<div class="rel_snippet5_1_1">'
                    strhtmlmodal +='<p class="p_reliant_project_1">' + project['project_name'] +'</p>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='<div id="colum3_modal_project_1" class="col-3 rel_snippet5_loc">'
                    strhtmlmodal +='<div  class="rel_snippet5_1_2" style="background-color: #ffffff;">'
                    strhtmlmodal +='<div style="width: 100%;height:100%;background-color:white;padding: 3px 0 3px 0;">'
                    strhtmlmodal +='<div style="background: url(data:image/png;base64,' + project['client_id_image'] + '); width: 100%;height: 100%;background-size: contain;background-repeat: no-repeat;background-position: center;" >'

                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='<div id="row_modal_mobile_1" class="row" style="margin-left: 0px;margin-right: 0px;">'
                    strhtmlmodal +='<div class="col-4 rel_snippet5_loc">'
                    strhtmlmodal +='<div id="div_block_1" style="background-color:#fff;width: 100%;height:100%;">'
                    strhtmlmodal +='<div style="background: url(data:image/png;base64,' + project['client_id_image'] + '); width: 100%;height: 100%;background-size: contain;background-repeat: no-repeat;background-position: center;">'
                    strhtmlmodal +='</div></div></div>'
                    strhtmlmodal +='<div class="col-4 rel_snippet5_loc">'
                    strhtmlmodal +='<div id="div_block_2" style="background-color:#C8C8C8; margin: 0 2px 0 2px;height: 100%;">'
                    strhtmlmodal +='<p class="project_detail_titulo">CLIENT</p>'
                    strhtmlmodal +='<p class="project_detail_subtitulo" >' + project['client_id_name'] + '</p>'
                    strhtmlmodal +='</div></div>'
                    strhtmlmodal +='<div class="col-4 rel_snippet5_loc">'
                    strhtmlmodal +='<div style="background-color:#E6E6E6; margin: 0 0 0 0;height: 100%;">'
                    strhtmlmodal +='<p class="project_detail_titulo">LOCATION</p>'
                    strhtmlmodal +='<p class="project_detail_subtitulo">' + project['location_country'] + '-' + project['location_city'] + '</p>'
                    strhtmlmodal +='</div></div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='<div id="row_modal_mobile_2" class="row" style="margin-left: 0px;margin-right: 0px;">'
                    strhtmlmodal +='<div class="col-4 rel_snippet5_loc">'
                    strhtmlmodal +='<div id="div_block_3" style="background-color:#C8C8C8; margin: 0 0 0 0;height:100%;">'
                    strhtmlmodal +='<p class="project_detail_titulo">COMMODITIES</p>'
                    strhtmlmodal +='<p class="project_detail_subtitulo">' + project['commodity'] + '</p>'
                    strhtmlmodal +='</div></div>'
                    strhtmlmodal +='<div class="col-8 rel_snippet5_loc">'
                    strhtmlmodal +='<div style="background-color:#E6E6E6;height: 100%;margin:0 0 0 2px;">'
                    strhtmlmodal +='<p class="project_detail_titulo">SERVICES PROVIDED</p>'
                    project['servicios'].forEach(p => {
                        strhtmlmodal +='<p class="project_detail_subtitulo">' + p + '</p>'
                    })
                    strhtmlmodal +='</div></div>'
                    strhtmlmodal +='</div>'
                    
                    strhtmlmodal +='<div class="row" style="margin-left: 0px;margin-right: 0px;">'
                    strhtmlmodal +='<div class="col-md-9 col-12 rel_snippet5_loc">'
                    strhtmlmodal +='<div >'
                    strhtmlmodal +='<div id="myCarousel_modal_project" class="s_carousel s_carousel_default carousel slide" data-interval="3000" style="height:525px; margin: 8px 8px 0 0;" >'

                    strhtmlmodal +='<ol class="carousel-indicators">'
                    strhtmlmodal +='<li data-target="#myCarousel_modal_project" data-slide-to="0" class="active"/>'
                    strhtmlmodal +='<li data-target="#myCarousel_modal_project" data-slide-to="1"/>'
                    strhtmlmodal +='<li data-target="#myCarousel_modal_project" data-slide-to="2"/>'
                    strhtmlmodal +='</ol>'
                    strhtmlmodal +='<div class="carousel-inner">'

                    strhtmlmodal +='<div class="carousel-item active oe_img_bg " data-name="Slide" style="background: url(data:image/png;base64,' + project['image_detail_1'] + ');width: 100%;height: 100%;background-repeat: round;">'
                    strhtmlmodal +='<div class="container carrousel_project"></div>'
                    strhtmlmodal +='</div>'

                    strhtmlmodal +='<div class="carousel-item oe_img_bg " data-name="Slide" style="background: url(data:image/png;base64,' + project['image_detail_2'] + ');width: 100%;height: 100%;background-repeat: round;">'
                    strhtmlmodal +='<div class="container carrousel_project">'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'

                    strhtmlmodal +='<div class="carousel-item oe_img_bg " data-name="Slide" style="background: url(data:image/png;base64,' + project['image_detail_3'] + ');width: 100%;height: 100%;background-repeat: round;">'
                    strhtmlmodal +='<div class="container carrousel_project"></div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'

                    strhtmlmodal +='<a class="carousel-control-prev" href="#myCarousel_modal_project" data-slide="prev" role="img" aria-label="Previous" title="Previous">'
                    strhtmlmodal +='<span class="carousel-control-prev-icon"/>'
                    strhtmlmodal +='<span class="sr-only">Previous</span>'
                    strhtmlmodal +='</a>'
                    strhtmlmodal +='<a class="carousel-control-next" href="#myCarousel_modal_project" data-slide="next" role="img" aria-label="Next" title="Next">'
                    strhtmlmodal +='<span class="carousel-control-next-icon"/>'
                    strhtmlmodal +='<span class="sr-only">Next</span>'
                    strhtmlmodal +='</a>'      
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'   
                    strhtmlmodal +='<div id="colum3_modal_project_2" class="col-3" style="padding: 0">'
                    strhtmlmodal +='<div id="fields_projects_reliant" style="margin: 8px 0 0 0;">'
                    strhtmlmodal +='<div style="background-color:#C8C8C8; margin: 0 0 8px 0;">'
                    strhtmlmodal +='<p class="project_detail_titulo">CLIENT</p>'
                    strhtmlmodal +='<p class="project_detail_subtitulo" >' + project['client_id_name'] + '</p>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='<div style="background-color:#E6E6E6; margin: 0 0 8px 0;">'
                    strhtmlmodal +='<p class="project_detail_titulo">LOCATION</p>'
                    strhtmlmodal +='<p class="project_detail_subtitulo">' + project['location_country'] + '-' + project['location_city'] + '</p>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='<div style="background-color:#C8C8C8; margin: 0 0 8px 0;">'
                    strhtmlmodal +='<p class="project_detail_titulo">COMMODITIES</p>'
                    strhtmlmodal +='<p class="project_detail_subtitulo">' + project['commodity'] + '</p>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='<div id="div_service" style="background-color:#E6E6E6;height:240px;">'
                    strhtmlmodal +='<p class="project_detail_titulo">SERVICES PROVIDED</p>'
                    project['servicios'].forEach(p => {
                        strhtmlmodal +='<p class="project_detail_subtitulo">' + p + '</p>'
                    })
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</div>'
                    strhtmlmodal +='</section>'
                    
                    $("#myModal_reliant").append(strhtmlmodal);
                    $("#myModal_reliant").show();

        }) 
    }

    function jobfunction(x) {

        $.post('/openmodaljob', {job: x}, function(data){
        data = JSON.parse(data)

                 
            $("#myModal_reliant_job").empty();

            var job = data['job_modal'][0]

            var strhtmlmodaljob ='<section style="background-color:#898A84;padding:2% 2% 2% 2%">'
                            strhtmlmodaljob +='<div class="container" style="padding:0;">'
                            strhtmlmodaljob +='<div id="row_modal_job_primary_1">'
                            strhtmlmodaljob +='<div id="col_job_1_1">'
                            strhtmlmodaljob +='<div id="div_job_1_1">'
                            strhtmlmodaljob +='<p class="p_font_job_position">' + job['position'] + '</p>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='<div id="col_job_1_2">'
                            strhtmlmodaljob +='<div id="div_job_1_2">'
                            strhtmlmodaljob +='<div style="background: url(data:image/png;base64,' + job['client_id_image_1920'] + '); width: 100%;height: 100%;background-size: contain;background-repeat: no-repeat;background-position: center;" >'

                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'

                            strhtmlmodaljob +='<div id="row_modal_job_primary_2" >'
                            strhtmlmodaljob +='<div id="col_job_2_1">'
                            strhtmlmodaljob +='<div style="background: url(data:image/png;base64,' + job['img_job'] + ');width: 100%;height:100%;    background-size: cover;background-position-x: center;">'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='<div  id="col_job_2_2">'
                            strhtmlmodaljob +='<div id="row_modal_job">'
                            strhtmlmodaljob +='<div id="col_job_2_2_1">'
                            strhtmlmodaljob +='<div id="div_job_2_1">'
                            strhtmlmodaljob +='<p class="p_font_job_client_title">CLIENT</p>'
                            strhtmlmodaljob +='<p class="p_font_job_client">' + job['client_id'] + '</p>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='<div id="col_job_2_2_2">'
                            strhtmlmodaljob +='<div id="div_job_2_2">'
                            strhtmlmodaljob +='<p class="p_font_job_location_title">LOCATION</p>'
                            strhtmlmodaljob +='<p class="p_font_job_location">' + job['location'] + '</p>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='<div id="row_modal_job">'
                            strhtmlmodaljob +='<div id="col_job_2_2_3">'
                            strhtmlmodaljob +='<div id="div_job_2_3" class="p_font_job_description">'
                            strhtmlmodaljob +='<p class="p_font_job_description_title">DESCRIPTION</p>'
                            strhtmlmodaljob +=''+ job['description_job_opportunity'] +''
                            strhtmlmodaljob +='<div  style="width: 100%;display: flex;justify-content: flex-end;">'
                            strhtmlmodaljob +='<div  class="btn_apply_popup_job" >'
                            strhtmlmodaljob +='<a href="" class="btn_reliant_popup_job" style="" >Apply</a>'
                            strhtmlmodaljob +='<i class="fa fa-angle-right " style="color:white;padding-left: 20px;font-size: 25px;"/>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'

                            strhtmlmodaljob +='<div id="row_modal_job_primary_3" >'
                                strhtmlmodaljob +='<div  id="row_modal_job">'
                                    strhtmlmodaljob +='<div id="col_job_3_1">'
                                        strhtmlmodaljob +='<div style="background: url(data:image/png;base64,' + job['img_job'] + ');width: 100%;height:100%;    background-size: cover;background-position-x: center;">'
                                        strhtmlmodaljob +='</div>'
                                    strhtmlmodaljob +='</div>'
                                    strhtmlmodaljob +='<div  id="col_job_3_2">'
                                        strhtmlmodaljob +='<div id="row_modal_job">'
                                            strhtmlmodaljob +='<div id="col_job_3_2_1">'
                                                strhtmlmodaljob +='<div id="div_job_3_1">'
                                                    strhtmlmodaljob +='<p class="p_font_job_client_title">CLIENT</p>'
                                                    strhtmlmodaljob +='<p class="p_font_job_client">' + job['client_id'] + '</p>'
                                                strhtmlmodaljob +='</div>'
                                            strhtmlmodaljob +='</div>'
                                        strhtmlmodaljob +='</div>'
                                        strhtmlmodaljob +='<div  id="row_modal_job">'
                                            strhtmlmodaljob +='<div id="col_job_3_2_2">'
                                                strhtmlmodaljob +='<div id="div_job_3_2">'
                                                    strhtmlmodaljob +='<p class="p_font_job_location_title">LOCATION</p>'
                                                    strhtmlmodaljob +='<p class="p_font_job_location">' + job['location'] + '</p>'
                                                strhtmlmodaljob +='</div>'
                                            strhtmlmodaljob +='</div>'
                                        strhtmlmodaljob +='</div>'
                                    strhtmlmodaljob +='</div>'
                                strhtmlmodaljob +='</div>'
                                strhtmlmodaljob +='<div  id="row_modal_job">'
                                    strhtmlmodaljob +='<div id="col_job_3_2_3">'
                                        strhtmlmodaljob +='<div id="div_job_3_3" class="p_font_job_description">'
                                            strhtmlmodaljob +='<p class="p_font_job_description_title">DESCRIPTION</p>'
                                            strhtmlmodaljob +=''+ job['description_job_opportunity'] +''
                                            strhtmlmodaljob +='<div  style="width: 100%;display: flex;justify-content: flex-end;">'
                                                strhtmlmodaljob +='<div  class="btn_apply_popup_job" >'
                                                    strhtmlmodaljob +='<a href="" class="btn_reliant_popup_job" style="" >Apply</a>'
                                                    strhtmlmodaljob +='<i class="fa fa-angle-right " style="color:white;padding-left: 20px;font-size: 25px;"/>'
                                                strhtmlmodaljob +='</div>'
                                            strhtmlmodaljob +='</div>'
                                        strhtmlmodaljob +='</div>'
                                    strhtmlmodaljob +='</div>'
                                strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</div>'
                            strhtmlmodaljob +='</section>'
                
                $("#myModal_reliant_job").append(strhtmlmodaljob);
                $("#myModal_reliant_job").show();

        }) 

    }


odoo.define('theme_reliant.home', function (require) {
"use strict";

    
    var ajax = require('web.ajax')
    


    $(document).ready(function(){

        
        $('.customer-logos').slick({
            slidesToShow: 5,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 1000,
            arrows: false,
            dots: false,
                pauseOnHover: false,
                responsive: [{
                breakpoint: 768,
                settings: {
                    slidesToShow: 4
                }
            }, {
                breakpoint: 710,
                settings: {
                    slidesToShow: 3
                }
            }, {
                breakpoint: 520,
                settings: {
                    slidesToShow: 2
                }
            }]
        });

        $('.customer-footer').slick({
            infinite: true,
            slidesToShow: 4,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 1800,
            arrows: false,
            dots: false,
                pauseOnHover: true,
                responsive: [{
                breakpoint: 480,
                settings: {
                    slidesToShow: 1
                }
            }]
        });
        $('.customer-history').slick({
            infinite: true,
            slidesToShow: 2,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 1800,
            arrows: false,
            dots: false,
                pauseOnHover: true,
                responsive: [{
                breakpoint: 480,
                settings: {
                    slidesToShow: 2
                }
            }]
        });

        $("p.p_reliant_project_list_2_1").click(function(){
            var id_country_filtro = $(this).attr("id");
            var selector_oculta = "div.show_init:not([id='" + String(id_country_filtro) + "'])";
            var selector_muestra = "div.show_init[id='" + String(id_country_filtro) + "']";
            $(selector_oculta).hide();
            $(selector_muestra).show();

            $(this).css('font-weight', 'bold');
            $("p.p_reliant_project_list_2_0").css('font-weight', 'initial');
            var selector_pinta_option = "p.p_reliant_project_list_2_1:not([id='" + String(id_country_filtro) + "'])";
            $(selector_pinta_option).css('font-weight', 'initial')


        });

        $("p.p_reliant_project_list_2_0").click(function(){
            var selector_muestra = "div.show_init:not([id='0'])";
            $(selector_muestra).show();
            $("p.p_reliant_project_list_2_0").css('font-weight', 'bold');
            $("p.p_reliant_project_list_2_1").css('font-weight', 'initial');
        });


        $("div.reliant_sustent_3_1").click(function(){
            $(".sustent_active").removeClass("sustent_active")
            $(this).addClass('sustent_active')
            var id_values_type_filtro = $(this).attr("id");
            var selector_oculta = "div.show_init:not([id='" + String(id_values_type_filtro) + "'])";
            var selector_muestra = "div.show_init[id='" + String(id_values_type_filtro) + "']";
            $(selector_oculta).hide();
            $(selector_muestra).show();



        });

        $("div.show_init_services").click(function(){

            $(".service_active").removeClass("service_active")
            $(this).find('div.info_service_estado_1').addClass('service_active')

            ajax.jsonRpc("/jsonservices", 'call', 
            { service: this.id},
            {'async':true}).then(function (data) {

                
                $(".show_init_services_2").empty();

                var service = data['values_service'][0]

                var strhtml =  '<div class="rel_snippet4_loc_service_detail_right">';
                strhtml += '<p class="p_reliant_service_title_right">' + service[1] +'</p>';
                strhtml += '<div class="p_reliant_service_description_4">' + service[2] +'</div></div>';
            
                $(".show_init_services_2").empty(strhtml);
                $(".show_init_services_2").append(strhtml);
            })

        });


        /*
        $("div.show_init_services").click(function(){   
            $(".service_active").removeClass("service_active")
            $(this).find('div.info_service_estado_1').addClass('service_active')

                var strhtml =  '<div class="rel_snippet4_loc_service_detail_right">';
                strhtml += '<p class="p_reliant_service_title_right">' + $(this).find("p.p_reliant_service_title").text() + '</p>';
                strhtml += '<p class="p_reliant_service_description_4">' + $(this).find("div.p_reliant_service_description_2_2").text() + '</p></div>';

                $(".show_init_services_2").empty(strhtml);
                $(".show_init_services_2").append(strhtml);

        });
        */ 

        $("div.show_init_services_project").click(function(){
           
            ajax.jsonRpc("/ajaxtocontroller_service", 'call', 
            { service: this.id},
            {'async':true}).then(function (data) {

                
                $("#show_project").empty();
                data['project'].forEach(p => {
                                                                                                                     
                            var strhtmlimg1 ='<div class="col-md-4 col-6 rel_snippet4_loc show1" onmouseover="changeovershow(this)" onmouseout="changeoutshow(this)" data-toggle="modal" data-target="#myModal" id="' + p[0] + '" onclick="project_modal_function(this.id)">' 
                            strhtmlimg1 +='<div class="rel_snippet4_3_2 info_current_project_estado_1">'
                            strhtmlimg1 +='<div style="background-image: url(data:image/png;base64,' + p[2] + '); width: 100%;height:100%;background-size: cover;background-repeat: no-repeat;background-position: center;">'
                            strhtmlimg1 +='<div class="rel_snippet4_3_2_aux" style="display:none;" >'
                            strhtmlimg1 +='<p class="p_reliant_service_title_4">' + p[1] + '</p>'
                            strhtmlimg1 +='</div>'
                            strhtmlimg1 +='</div>'
                            strhtmlimg1 +='</div>'
                            strhtmlimg1 +='</div>'
                    $("#show_project").append(strhtmlimg1);  
                });
               
            })
        });


        $("a.btn_reliant_project").mouseover(function(){
            $(this).css('background-color', '#000000')
            $(this).css('color', '#ffffff')
            $(this).css('border', '1px solid #D4FCE8')
        });
        $("a.btn_reliant_sustainability").mouseover(function(){
            $(this).css('background-color', '#000000')
            $(this).css('color', '#ffffff')
            $(this).css('border', '1px solid #D4FCE8')
        });
        $("a.btn_reliant_about").mouseover(function(){
            $(this).css('background-color', '#000000')
            $(this).css('color', '#ffffff')
            $(this).css('border', '1px solid #D4FCE8')
        });
        $("a.btn_reliant_project").mouseout(function(){
            $(this).css('background-color', '#D4FCE8')
            $(this).css('color', '#000000')
            $(this).css('border', '1px solid #000')
        });
        $("a.btn_reliant_sustainability").mouseout(function(){
            $(this).css('background-color', '#D4FCE8')
            $(this).css('color', '#000000')
            $(this).css('border', '1px solid #000')
        });
        $("a.btn_reliant_about").mouseout(function(){
            $(this).css('background-color', '#D4FCE8')
            $(this).css('color', '#000000')
            $(this).css('border', '1px solid #000')
        });

        $(".show1").mouseover(function(){
            $(this).find('div.rel_snippet4_3_2_aux').show()
            
        });

        $(".show1").mouseout(function(){
            $(this).find('div.rel_snippet4_3_2_aux').hide()
        });

        
        

        $("div.show_init").mouseover(function(){
            $(this).find('div.div_reliant_project_1').hide();
            $(this).find('div.div_reliant_project_2').show();
            $(this).find('div.div_reliant_project_3').show();  
        });

        $("div.show_init").mouseout(function(){
            $(this).find('div.div_reliant_project_1').show();
            $(this).find('div.div_reliant_project_2').hide();
            $(this).find('div.div_reliant_project_3').hide();  
        });

        $("div.show_init_home_bottom_1").mouseover(function(){
            $(this).find('div.div_name_home_bottom_1').show();
        });

        $("div.show_init_home_bottom_1").mouseout(function(){
            $(this).find('div.div_name_home_bottom_1').hide();  
        });
        $("div.show_init_home_bottom_2").mouseover(function(){
            $(this).find('div.div_name_home_bottom_2').show();
        });

        $("div.show_init_home_bottom_2").mouseout(function(){
            $(this).find('div.div_name_home_bottom_2').hide();  
        });
        $("div.show_init_home_bottom_3").mouseover(function(){
            $(this).find('div.div_name_home_bottom_3').show();
        });

        $("div.show_init_home_bottom_3").mouseout(function(){
            $(this).find('div.div_name_home_bottom_3').hide();  
        });

        $("#inputCountry").change(function(){
            var country = $(this).val()
            var department = $('#inputDepartment').val()
            var site = $('#inputSite').val()
            var language = $('#inputLanguage').val()
            


            ajax.jsonRpc("/change/job", 'call', 
            { country: country, department: department, site: site, language: language })          
            .then(function (data) {
                $("#job_opportunity").empty();
                data['opportunities'].forEach(opportunity => {
                    var div = '<div style="padding: 10px 0 10px 0;">'
                    div+='<div id="id_div_job" style="background-color:#C8C8C8;padding:18px 18px 0 18px;">'   
                    div+='<div id="id_div_job_1" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:50%;font-size:15px;">'
                    div+='<div id="id_name_position_job" style="width: 45%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['position'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:30%;font-size:15px;">'
                    div+='<div style="width: 75%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['location'].toString()+'</strong> / <strong>'+opportunity['site'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:20%;font-size:15px;">'
                    div+='<div>'
                    div+='<p class="p_font_job"><strong>'+opportunity['closing_date'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_2" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:100%;font-size:12px;">'
                    div+='<div><p class="p_font_job">'+opportunity['category_job_opportunity'].toString()+'</p></div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_3" tyle="display:flex;">'
                    div+='<div class="p_font_job" style="font-size:12px;">'
                    div+=''+opportunity['description_job_opportunity'].toString().replaceAll('<p>','').replaceAll('</p>','').replaceAll('<b>','').replaceAll('</b>','').replaceAll('<br>','').replaceAll('</br>','')+''
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="row" style="justify-content: flex-end;">'
                    div+='<a data-toggle="modal" data-target="#myModal" style="text-decoration: none;" onclick="jobfunction(this.id)" id="'+opportunity['id'].toString()+'"  class="btn_reliant_job">> Read more</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="modal fade" id="myModal" role="dialog">'
                    div+='<div class="modal-dialog" style="max-width:1280px !important;">'
                    div+='<div id="modal-content-job" class="modal-content" style="background-color: #E6E6E6">'
                    div+='<div class="">'
                    div+='<div id="header-modal-job" class="row" style="padding: 0 25px 0 25px;margin-top:20px;">'
                    div+='<div class="p-2 ">'
                    div+='<a href="/" aria-current="page" id="log_main_mobile" class="list__item__enlace logo justify-content-center py-0 nuxt-link-exact-active nuxt-link-active" >'
                    div+='<img id="img_logo_modal_job" src="/theme_reliant/static/img/reliant_logo_home.png" alt="Logo RELIANT" class="img-fluid list__item__enlace__logo" style="width:304;height:60px;"/>'
                    div+='</a>'
                    div+='</div>'
                    div+='<div id="icon_nav_reliant_1" class="ml-auto p-2 ">'
                    div+='<a  data-dismiss="modal" style="display: flex;align-items: center;text-decoration: none;padding: 25px 0 0 0;">'
                    div+='<i class="fa fa-times fa-2x " style="color:black;"></i>'
                    div+='</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="myModal_reliant_job">'

                    div+='</div>'

                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'

                    $("#job_opportunity").append(div);
                })
                
            });
            
        });
        $("#inputDepartment").change(function(){
            var country = $('#inputCountry').val()
            var department = $(this).val()
            var site = $('#inputSite').val()
            var language = $('#inputLanguage').val()
            
            ajax.jsonRpc("/change/job", 'call', 
            { country: country, department: department, site: site, language: language })          
            .then(function (data) {
                $("#job_opportunity").empty();
                data['opportunities'].forEach(opportunity => {
                    var div = '<div style="padding: 10px 0 10px 0;">'
                    div+='<div id="id_div_job" style="background-color:#C8C8C8;padding:18px 18px 0 18px;">'   
                    div+='<div id="id_div_job_1" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:50%;font-size:15px;">'
                    div+='<div id="id_name_position_job" style="width: 45%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['position'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:30%;font-size:15px;">'
                    div+='<div style="width: 75%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['location'].toString()+'</strong> / <strong>'+opportunity['site'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:20%;font-size:15px;">'
                    div+='<div>'
                    div+='<p class="p_font_job"><strong>'+opportunity['closing_date'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_2" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:100%;font-size:12px;">'
                    div+='<div><p class="p_font_job">'+opportunity['category_job_opportunity'].toString()+'</p></div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_3" tyle="display:flex;">'
                    div+='<div class="p_font_job" style="font-size:12px;">'
                    div+=''+opportunity['description_job_opportunity'].toString().replaceAll('<p>','').replaceAll('</p>','').replaceAll('<b>','').replaceAll('</b>','').replaceAll('<br>','').replaceAll('</br>','')+''
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="row" style="justify-content: flex-end;">'
                    div+='<a data-toggle="modal" data-target="#myModal" style="text-decoration: none;" onclick="jobfunction(this.id)" id="'+opportunity['id'].toString()+'"  class="btn_reliant_job">> Read more</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="modal fade" id="myModal" role="dialog">'
                    div+='<div class="modal-dialog" style="max-width:1280px !important;">'
                    div+='<div id="modal-content-job" class="modal-content" style="background-color: #E6E6E6">'
                    div+='<div class="">'
                    div+='<div id="header-modal-job" class="row" style="padding: 0 25px 0 25px;margin-top:20px;">'
                    div+='<div class="p-2 ">'
                    div+='<a href="/" aria-current="page" id="log_main_mobile" class="list__item__enlace logo justify-content-center py-0 nuxt-link-exact-active nuxt-link-active" >'
                    div+='<img id="img_logo_modal_job" src="/theme_reliant/static/img/reliant_logo_home.png" alt="Logo RELIANT" class="img-fluid list__item__enlace__logo" style="width:304;height:60px;"/>'
                    div+='</a>'
                    div+='</div>'
                    div+='<div id="icon_nav_reliant_1" class="ml-auto p-2 ">'
                    div+='<a  data-dismiss="modal" style="display: flex;align-items: center;text-decoration: none;padding: 25px 0 0 0;">'
                    div+='<i class="fa fa-times fa-2x " style="color:black;"></i>'
                    div+='</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="myModal_reliant_job">'

                    div+='</div>'

                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'

                    $("#job_opportunity").append(div);
                })
                
            });
            
        });
        $("#inputSite").change(function(){
            var country = $('#inputCountry').val()
            var department = $('#inputDepartment').val()
            var site = $(this).val()
            var language = $('#inputLanguage').val()
            
            ajax.jsonRpc("/change/job", 'call', 
            { country: country, department: department, site: site, language: language })          
            .then(function (data) {
                $("#job_opportunity").empty();
                data['opportunities'].forEach(opportunity => {
                    var div = '<div style="padding: 10px 0 10px 0;">'
                    div+='<div id="id_div_job" style="background-color:#C8C8C8;padding:18px 18px 0 18px;">'   
                    div+='<div id="id_div_job_1" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:50%;font-size:15px;">'
                    div+='<div id="id_name_position_job" style="width: 45%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['position'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:30%;font-size:15px;">'
                    div+='<div style="width: 75%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['location'].toString()+'</strong> / <strong>'+opportunity['site'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:20%;font-size:15px;">'
                    div+='<div>'
                    div+='<p class="p_font_job"><strong>'+opportunity['closing_date'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_2" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:100%;font-size:12px;">'
                    div+='<div><p class="p_font_job">'+opportunity['category_job_opportunity'].toString()+'</p></div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_3" tyle="display:flex;">'
                    div+='<div class="p_font_job" style="font-size:12px;">'
                    div+=''+opportunity['description_job_opportunity'].toString().replaceAll('<p>','').replaceAll('</p>','').replaceAll('<b>','').replaceAll('</b>','').replaceAll('<br>','').replaceAll('</br>','')+''
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="row" style="justify-content: flex-end;">'
                    div+='<a data-toggle="modal" data-target="#myModal" style="text-decoration: none;" onclick="jobfunction(this.id)" id="'+opportunity['id'].toString()+'"  class="btn_reliant_job">> Read more</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="modal fade" id="myModal" role="dialog">'
                    div+='<div class="modal-dialog" style="max-width:1280px !important;">'
                    div+='<div id="modal-content-job" class="modal-content" style="background-color: #E6E6E6">'
                    div+='<div class="">'
                    div+='<div id="header-modal-job" class="row" style="padding: 0 25px 0 25px;margin-top:20px;">'
                    div+='<div class="p-2 ">'
                    div+='<a href="/" aria-current="page" id="log_main_mobile" class="list__item__enlace logo justify-content-center py-0 nuxt-link-exact-active nuxt-link-active" >'
                    div+='<img id="img_logo_modal_job" src="/theme_reliant/static/img/reliant_logo_home.png" alt="Logo RELIANT" class="img-fluid list__item__enlace__logo" style="width:304;height:60px;"/>'
                    div+='</a>'
                    div+='</div>'
                    div+='<div id="icon_nav_reliant_1" class="ml-auto p-2 ">'
                    div+='<a  data-dismiss="modal" style="display: flex;align-items: center;text-decoration: none;padding: 25px 0 0 0;">'
                    div+='<i class="fa fa-times fa-2x " style="color:black;"></i>'
                    div+='</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="myModal_reliant_job">'

                    div+='</div>'

                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'

                    $("#job_opportunity").append(div);
                })
                
            });
            
        });
        $("#inputLanguage").change(function(){
            var country = $('#inputCountry').val()
            var department = $('#inputDepartment').val()
            var site = $('#inputSite').val()
            var language = $(this).val()
            
            ajax.jsonRpc("/change/job", 'call', 
            { country: country, department: department, site: site, language: language })          
            .then(function (data) {
                $("#job_opportunity").empty();
                data['opportunities'].forEach(opportunity => {
                    var div = '<div style="padding: 10px 0 10px 0;">'
                    div+='<div id="id_div_job" style="background-color:#C8C8C8;padding:18px 18px 0 18px;">'   
                    div+='<div id="id_div_job_1" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:50%;font-size:15px;">'
                    div+='<div id="id_name_position_job" style="width: 45%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['position'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:30%;font-size:15px;">'
                    div+='<div style="width: 75%;">'
                    div+='<p class="p_font_job"><strong>'+opportunity['location'].toString()+'</strong> / <strong>'+opportunity['site'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div style="width:20%;font-size:15px;">'
                    div+='<div>'
                    div+='<p class="p_font_job"><strong>'+opportunity['closing_date'].toString()+'</strong></p>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_2" style="display:flex;margin: 0 0 12px 0;">'
                    div+='<div style="width:100%;font-size:12px;">'
                    div+='<div><p class="p_font_job">'+opportunity['category_job_opportunity'].toString()+'</p></div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="id_div_job_3" tyle="display:flex;">'
                    div+='<div class="p_font_job" style="font-size:12px;">'
                    div+=''+opportunity['description_job_opportunity'].toString().replaceAll('<p>','').replaceAll('</p>','').replaceAll('<b>','').replaceAll('</b>','').replaceAll('<br>','').replaceAll('</br>','')+''
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="row" style="justify-content: flex-end;">'
                    div+='<a data-toggle="modal" data-target="#myModal" style="text-decoration: none;" onclick="jobfunction(this.id)" id="'+opportunity['id'].toString()+'"  class="btn_reliant_job">> Read more</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div class="modal fade" id="myModal" role="dialog">'
                    div+='<div class="modal-dialog" style="max-width:1280px !important;">'
                    div+='<div id="modal-content-job" class="modal-content" style="background-color: #E6E6E6">'
                    div+='<div class="">'
                    div+='<div id="header-modal-job" class="row" style="padding: 0 25px 0 25px;margin-top:20px;">'
                    div+='<div class="p-2 ">'
                    div+='<a href="/" aria-current="page" id="log_main_mobile" class="list__item__enlace logo justify-content-center py-0 nuxt-link-exact-active nuxt-link-active" >'
                    div+='<img id="img_logo_modal_job" src="/theme_reliant/static/img/reliant_logo_home.png" alt="Logo RELIANT" class="img-fluid list__item__enlace__logo" style="width:304;height:60px;"/>'
                    div+='</a>'
                    div+='</div>'
                    div+='<div id="icon_nav_reliant_1" class="ml-auto p-2 ">'
                    div+='<a  data-dismiss="modal" style="display: flex;align-items: center;text-decoration: none;padding: 25px 0 0 0;">'
                    div+='<i class="fa fa-times fa-2x " style="color:black;"></i>'
                    div+='</a>'
                    div+='</div>'
                    div+='</div>'
                    div+='<div id="myModal_reliant_job">'

                    div+='</div>'

                    div+='</div>'
                    div+='</div>'
                    div+='</div>'
                    div+='</div>'

                    $("#job_opportunity").append(div);
                })
                
            });
            
        });

    });
});


