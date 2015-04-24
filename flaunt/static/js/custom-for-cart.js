function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
}

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

function updateContent(discount, subtotal, total, shipping_type, shipping_total){
    var html;    
        if(discount){
            html = "<table class='table'><tbody><tr><td>Sub total:</td><th>$" + subtotal + "</th></tr><tr><td>Discount:</td><th>$" + discount + "</th></tr><tr><td>" + shipping_type + ":</td><th>$" + shipping_total + "</th></tr><tr class='total'><td>Total:</td><th>" + total + "</th></tr></tbody></table>"
        } else {
            html = "<table class='table'><tbody><tr><td>Sub total:</td><th>$" + subtotal + "</th></tr><tr><td>" + shipping_type + ":</td><th>$" + shipping_total + "</th></tr><tr class='total'><td>Total:</td><th>" + total + "</th></tr></tbody></table>"
        }
        
        $('div#id_table_responsive.table-responsive').html(html);
}

function ajaxcallfree(){
                $.ajax({
                    url: '/get_carrier',
                    type: 'POST',
                    data: {'free_shipping' : 'True'}, 
                    success: function(data){
                        var total_qty = $('#subtotal').attr('class'),
                            subtotal = parseFloat(data.subtotal),
                            discount = parseFloat(data.discount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'),
                            total = data.total_price,
                            shipping_type = data.shipping_type,
                            shipping_total = data.shipping_total;

                        $('#subtotal').attr('name','Regular Shipping');
                        $("span.badge").html(total_qty.toString());
                        
                            if (total_qty != '1'){
                                    $('#cart_menu').html('&nbsp;'+total_qty.toString()+' items - $'+total);
                            }else{
                                    $('#cart_menu').html(' 1 item - $'+total);
                            }
                        updateContent(discount, subtotal, total, shipping_type, shipping_total);
                        
                    },
                    error: function(data){
                        console.log('error'+data);
                    } 
                });
}
function getCountry(sel){
    if($("#required").length){
        $("#required").remove();
    }
    if($('span#error').length){
        $('span#error').remove();
    }
	$('#chosen_country').val(sel.value);
    $('#id_shipping_type').val("");

    $('#id_carrier').find('option').remove().end().append('<option value="0">Please select shipping type</option').val("0").prop('disabled',true);;
    //ajaxcallfree()
    //var shipping_type = document.getElementById('id_shipping_type');
    //shipping_type.options.length = 1;
    //shipping_type.options.add(new Option('Priority Shipping (fast)', 'priority'));
    //shipping_type.options.add(new Option('Regular Shipping', 'regular'));
    var country_name = $('#chosen_country').val();
    $.ajax({
        url: '/ajax_set_selected_country',
        type: 'POST',
        data: {'country' : country_name}, 
        success: function(data){ 
                    console.log("success");
                },
        error: function(data){
            console.log('error '+JSON.stringify(data));
        }
    });
    
}
function setCarriers(s){
    if($("#required").length){
        $("#required").remove();
    }
    var country_name = $('#chosen_country').val();

    if (country_name === ""){
        $("#id_shipping_type").val('');
        if(!$("#country_first").length){
            $("label[for='id_country']").after("<span id='error' style='color:red'>&nbsp;Please select country first.</span>");
            
        }
        return false;
    }
    var carrier = document.getElementById('id_carrier');
    if(s.value === "Priority Shipping" && country_name != ""){
        $(carrier).prop('disabled',false);
        $.post('/ajax_country',{'country' : country_name}, function(data){ 
            
           var priority = data['carriers_priority'];
            //var regular = data['carriers_regular'];
            carrier.name = s.value;
            
            carrier.options.length = 1;
            for(pri in priority){
                carrier.options.add(new Option(priority[pri], priority[pri]));
            }   
        });
    } else if (s.value === "Regular"){

                $(carrier).val("0").prop('disabled','disabled');
                ajaxcallfree();
            }
        
    
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
                    var subtotal = data.subtotal,
                        discount = parseFloat(data.discount),
                        total = data.total_price,
                        shipping_total = parseFloat(shipping_total),
                        subtotal = parseFloat(subtotal).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'),
                        total_qty = $('#subtotal').attr('class');

                    if (total_qty != '1'){
                            $('#cart_menu').html('&nbsp;'+total_qty.toString()+' items - $'+total);
                        }else{
                            $('#cart_menu').html(' 1 item - $'+total);
                        }
                    
                    $("span.badge").html(total_qty.toString());
                    updateContent(discount, subtotal, total, shipping_type, shipping_total);
                    
                },
        error: function(data){
            console.log('error '+JSON.stringify(data));
        }
    });
}