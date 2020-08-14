$(document).ready(function (){

    // multi-step form js start

    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;

    $(".next").click(function(){

        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        //Add Class Active
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        //show the next fieldset
        next_fs.show();
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                }).prop('required', false);
                next_fs.css({'opacity': opacity});
            },
            duration: 600
        });
    });

    $(".previous").click(function(){

        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        //Remove class active
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

        //show the previous fieldset
        previous_fs.show();

        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                }).prop('required', false);
                previous_fs.css({'opacity': opacity});
            },
            duration: 600
        });
    });

    $('.radio-group .radio').click(function(){
    $(this).parent().find('.radio').removeClass('selected');
    $(this).addClass('selected');
    });

    $(".submit").click(function(){
        var input = $("form")
        input.find('input').each(function (){
            if(!$(this).val()){
                $("input.submit").attr('disabled', 'disabled')
            }else{
                $("input.submit").removeAttr('disabled', '')
            }
        });
         // return true;
    });
    $("input.submit").removeAttr('disabled');

    function validatef (){
        var input = $("form")
        var state = ''
        input.find('input').each(function (){
            if(!$(this).attr('value') && !$(this).val() || $(this).attr('value') && !$(this).val()){
                $("input.submit").attr('disabled', 'disabled')
                state = "disabled"
                return true;
            }else{
                $("input.submit").removeAttr('disabled')
                console.log($(this).val())
                state = "enabled"
                return true;
            }
        });
        console.log(state)
         // return true;
    }
    window.setInterval(validatef, 1000);

    // for(i = 0; i < input2.length; i++){ console.log(input2[i].value); if(input2[i].value == ""){ break; }; }






    // multi-step form js end

});