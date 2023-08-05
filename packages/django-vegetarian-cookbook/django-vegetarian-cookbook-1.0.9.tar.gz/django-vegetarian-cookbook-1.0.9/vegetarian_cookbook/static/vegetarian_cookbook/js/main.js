$.Search = {"request":false};

$.Search.simple = function(e) {
    var query = $(e.target).val().trim();
    if ($.Search.request) clearTimeout($.Search.request)
    $.Search.request = setTimeout(function(){
        $.Search.send(query);
    }, 1000);
    e.preventDefault();
    return false;
}

$.Search.full = function(e) {
    if ($.Search.request) clearTimeout($.Search.request)
    $.Search.request = setTimeout(function(){
        var data = $("#search-form").serializeArray();
        var query = $('#search-form input[name="query"]').val().trim();
        $.Search.send(query, data);
    }, 1000);
    e.preventDefault();
    return false;
}

$.Search.send = function(query, data) {
    if (query.length < 3) return;
    if (!data) {
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            'csrfmiddlewaretoken':csrftoken,
            'query':query,
        }
    }
    $.post('/search/', data, function(response) {
        $.Search.show(response)
    });

}
//TODO update max-min by ajax

$.Search.show = function(data) {
    var template = _.template($("#ajax-search_template").html());
    var htmlOutput = template(data);
    if ($(".search-result").length)
        $(".search-result").html(htmlOutput);
    else
        $(".ajax-search-results").html(htmlOutput);
    if (data.search) {
        console.log(data.search);
        $.each(['energy', 'time', 'protein', 'fat', 'carbohydrate'],
            function(i, parameter) {
                var cmin = data.search[parameter].cmin;
                var cmax = data.search[parameter].cmax;
                var range = cmin + ' - ' + cmax;
                $("#range-slider__value_" + parameter).html(range);
                $( "#slider-range_" + parameter ).slider({
                    "min": data.search[parameter].min,
                    "max": data.search[parameter].max,
                    "values":[cmin, cmax]
                })
        });

    }
}
