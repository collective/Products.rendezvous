var rendezvous = {};


rendezvous.init = function(){
    jq('.template-edit_dates').each(rendezvous.initchoicesselection);
    jq('.template-rendezvous_view').each(rendezvous.inituserchoice);
    jq('#rendezvous-choose-date').click(rendezvous.startdatechoice);
};

rendezvous.initchoicesselection = function(){
    bind_dates = function (){
        jq('#rendezvous-dates-select a.calendar-date').click(function(){
            /* first submit the form in case it has been modified */
            var datelink = jq(this);
            var formData = jq('form#rendezvous-edit').serialize();
            var formAction = jq('form#rendezvous-edit').attr('action');
            jq.post(formAction, formData, function(){
                jq.get(datelink.attr('href') + '&ajax_load=1', function(html){
                    jq('#rendezvous-edit').html(jq(html).find('#rendezvous-edit').html());
                    rendezvous.initchoicesselection();
                });
            });
            return false;
        });
    };
    bind_dates();

    bind_next_month = function (){
        jq('#rendezvous-dates-select .calendarHeader a').unbind('click').click(function(){
            /* update calendar when click on next */
            var url = jq('base').attr('href') + '/' + jq(this).attr('href');
            update_calendar_month(url);
            return false;
        });
    };
    bind_next_month();

    function update_calendar_month(href){
        jq.get(href, function(html){
            var new_month = $(html).find('#rendezvous-dates-select .portletCalendar .portletItem');
            $('#rendezvous-dates-select .portletCalendar .portletItem').replaceWith(new_month);
            bind_dates();
            bind_next_month();
        });
    }

    jq('#rendezvous-hours-select input[name="extend"]').click(function(){
        var formData = jq('form#rendezvous-edit').serialize();
        var formAction = jq('form#rendezvous-edit').attr('action') + '?extend=1';
        jq.post(formAction, formData, function(html){
            jq('#rendezvous-edit').html(jq(html).find('#rendezvous-edit').html());
            rendezvous.initchoicesselection();
        });
        return false;
    });
};

rendezvous.inituserchoice = function(){
    jq('td.selectable').click(rendezvous.toggleuserchoice);
};

rendezvous.toggleuserchoice = function(){
    var cell = jq(this);
    var input = cell.children('input');
    var span = cell.children('span');
    if(input.attr('value') === ''){
        /* select value */
        cell.removeClass('unavailable');
        cell.removeClass('unknown');
        cell.addClass('available');
        input.attr('value', input.attr('id'));
        span.html('OK');
    }
    else{
        /* unselect value */
        cell.removeClass('available');
        cell.addClass('unavailable');
        input.attr('value', '');
        span.html('');
    }
};

rendezvous.startdatechoice = function(){
    jq('body').css('cursor', 'pointer');
    jq('.rendezvous-datechoice').css('color', 'blue');
    jq('#rendezvous').click(rendezvous.enddatechoice);
    jq('.rendezvous-datechoice').click(rendezvous.selectdatechoice);
};

rendezvous.enddatechoice = function(){
    jq('body').css('cursor', 'default');
    jq('#rendezvous').unbind('click');
    jq('.rendezvous-datechoice').removeAttr('style');
};

rendezvous.selectdatechoice = function(){
    var base_url = jq('base').attr('href');
    var date = jq(this).attr('class').split(' ')[1];
    window.location.href = base_url + '@@rendezvous_create_event?date=' + date;
};
jq(document).ready(rendezvous.init);
