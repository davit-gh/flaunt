function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
function getCountry(sel){
    if($("#required").length){
        $("#required").remove();
    }
	$('#chosen_country').val(sel.value);
    $('#id_shipping_type').val("");
    $('#id_carrier').find('option').remove().end().append('<option value="0">Please select a country first</option').val("0");
    var shipping_type = document.getElementById('id_shipping_type');
    shipping_type.options.length = 1;
    shipping_type.options.add(new Option('Priority Shipping (fast)', 'priority'));
    shipping_type.options.add(new Option('Regular Shipping', 'regular'));
    
}
function setCarriers(s){
    if($("#required").length){
        $("#required").remove();
    }
    var country_name = $('#chosen_country').val();
    $.post('/ajax_country',{'country' : country_name}, function(data){ 
        console.log(data);
        var carrier = document.getElementById('id_carrier');
        var priority = data['carriers_priority'];
        var regular = data['carriers_regular'];
        carrier.name = s.value;
        if(s.value == 'priority'){
            carrier.options.length = 1;

            for(pri in priority){
                carrier.options.add(new Option(priority[pri], priority[pri]));
            }   
        }else{
            carrier.options.length = 1;
            for(reg in regular){
                carrier.options.add(new Option(regular[reg], regular[reg]));
            }   
        }
    });
    
}
function getCarrier(sel){
    if($("#required").length){
        $("#required").remove();
    }
    $.ajax({
        url: '/get_carrier',
        type: 'POST',
        data: {'carrier' : sel.value, 'shipping_type' : sel.name}, 
        success: function(data){ 
                    var shipping_type = data.shipping_type;
                    var shipping_total = data.shipping_total;
                    $('#subtotal').val(shipping_total);
                    $('#subtotal').attr('name',shipping_type);
                    var subtotal = data.total_price;
                    var total = parseFloat(shipping_total) + parseFloat(subtotal);
                    shipping_total = parseFloat(shipping_total).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                    subtotal = parseFloat(subtotal).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                    total = total.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                    var total_qty = $('#subtotal').attr('class');
                    if (total_qty != '1'){
                            $('#cart_menu').html('&nbsp;'+total_qty.toString()+' items in cart, total: $'+total);
                        }else{
                            $('#cart_menu').html(' 1 item in cart, total: $'+total);
                        }
                    var html = "<div class='order_totals'><div><label>Sub total:</label>$"+subtotal+"</div><div><label>"+shipping_type+"</label>$"+shipping_total+"</div><div class='total'><label>Total:&nbsp;</label>$"+total+"</div></div>";
                    $('#total_cell').html(html);
                },
        error: function(data){
            console.log('error '+JSON.stringify(data));
        }
    });
}