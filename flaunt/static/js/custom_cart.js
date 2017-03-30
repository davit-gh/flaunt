$(document).ready(function(){     
    $(document).bind("ajaxSend", function(){
        $("#loading").show();
    }).bind("ajaxComplete", function(){
        $("#loading").hide();
    });
    $('#id_carrier').prop('disabled',true);
    $('#id_shipping_type').val("");

    $("select[name='country'] option:eq(0)").attr('disabled','disabled');
    $("select[name='shipping_type'] option:eq(0)").attr('disabled','disabled');
    $("select[name='carrier'] option:eq(0)").attr('disabled','disabled');
    $('#id_carrier').prop('disabled','disabled');
    
        $('#checkout').click(function(){
            var country = $("#id_country");
            var ship_type = $("#id_shipping_type");
            var carrier = $('#id_carrier');
            if(!country.prop('selectedIndex')) {
                if(!$("#required").length){
                    $("label[for='id_country']").after("<span id='required' style='color:red; font-size: 16px'>&nbsp;* required</span>");
                } 
                return false;
            }
            if(ship_type.prop('selectedIndex') == 0) {
                if(!$("#required").length){
                    $("label[for='id_shipping_type']").after("<span id='required' style='color:red; font-size: 16px'>&nbsp;* required</span>");
                } 
                return false;
            }
            if(ship_type.prop('selectedIndex') == 2 && !carrier.prop('selectedIndex')){
                 if(!$("#required").length){
                    $("label[for='id_carrier']").after("<span id='required' style='color:red; font-size: 16px'>&nbsp;* required</span>");
                 }
                 return false;
            }
            return true;
        });
    
	$("input[type|='checkbox']").hide();
        $('#main_form').submit(function(){
            $.ajax({
                type: 'POST',
                url: '/update_cart', 
                data: $(this).serialize(),
                success: function(data){
                    var discount = data.discount_total;
                    
                    var clicked_id = $('#subtotal').data('notenoughstockid'),
                        quantity = $('#'+clicked_id).data('quantity'),
                        input_field = $('#'+clicked_id).parent().find('input');
                    if (data.error){
                        $('#warning_alert').show();

                        $(input_field).val(quantity);
                    }else{
                        var subtotal = parseFloat(data['subtotal']).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'),
                            grand = data.grand;
                        var shipping_fee = $('#subtotal').val();
                        if (shipping_fee == '0'){
                            shipping_fee = 'Not set yet';
                            
                        }else{
                            shipping_fee = $('#subtotal').val();
                            grand = parseFloat(grand) + parseFloat(shipping_fee);
                            shipping_fee = '$' + $('#subtotal').val();
                        }
                        var shipping_type = $('#subtotal').attr('name');
                        var sub = data['sub'];
                        var total_qty = data['total_qty'],
                            html,
                            order_summary_html;
                        $('#subtotal').attr('class',total_qty);

                            table = "<table class='table'><tbody><tr><td>Sub total:</td><th>$"+subtotal+"</th></tr><tr><td>Discount:</td><th>$"+discount+"</th></tr><tr><td>"+shipping_type+"</td><th>"+shipping_fee+"</th></tr><tr class='total'><td>Total:</td><th>$"+grand+"</th></tr></tbody></table>";
                            
                            $("#id_table_responsive").html(table);

                            order_summary_html = "<td>Total:</td><th>$"+grand+"</th>";

                        
                        $('tr.total').html(order_summary_html);
                        
                        $.each(sub,function(index,element){
                            var i = parseInt(index)+1;
                            $('table tr:eq('+i+') td:eq(4)').html('$'+parseFloat(element).toFixed(2));
                            
                        });
                        var count = $("#id_items-TOTAL_FORMS").val();
                        if (count === '0'){
                            $('div.box').html('<h4>Your Cart is empty.</h4>');
                            $('a.dropdown-toggle > span#cart_menu').html(' 0 items in cart, total: $0.00');

                        }
                        $("span.badge").html(total_qty.toString());
                        
                        if (total_qty != '1'){
                                $('#cart_menu').html('&nbsp;'+total_qty.toString()+' items - $'+grand);
                        }else{
                                $('#cart_menu').html(' 1 item - $'+grand);
                        }
                        
                    }
                            
                },
                error: function(xhRequest, ErrorText, thrownError){
                    console.log('xhRequest: ' + JSON.stringify(xhRequest) + "\n");
                    console.log('ErrorText: ' + ErrorText + "\n");
                    console.log('thrownError: ' + thrownError + "\n");
                }
            });
            return false;       
        });
        $("a[id|='update']").click(function(){
            $('#main_form').submit();
            $('#subtotal').attr('data-notenoughstockid', $(this).attr('id'));
            return false;
        });
        
        $("a[id|='rem']").on('click', function(){
            $(this).parent().parent().fadeOut('slow');
            var value = $(this).attr('class');
            var id = $("input[value|="+ value +"]").attr('id');
            console.log(id);
            var chkbx_id = id.slice(0,id.length-2) + 'DELETE';
            $('#'+chkbx_id).prop("checked",true);
            $('#main_form').submit();
            $(this).parents('.dynamic-form').remove();
            var forms = $('.dynamic-form');
            $('#id_items-TOTAL_FORMS').val(forms.length);
            
            
            return false;
        });
        $('#discount_button').click(function(){
            $.ajax({
                type: 'POST',
                url: '/getdiscount',
                data: {'discount_code':$('#id_discount_code').val()}, 
                success: function(data){

                            if (data.discount_code){
                                $('#warning_alert').show();

                                return false;
                            }
                            var discount = data.discount_total,
                                cart_total = data.cart_total,
                                ship_total = data.shipping_total,
                                ship_type = data.shipping_type,
                                total = (parseFloat(cart_total)-parseFloat(discount)+parseFloat(ship_total)).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                                $('#main_form').submit();
                            
                            
                         },
                error: function(data){
                    console.log('error'+JSON.stringify(data));
                }
            });
            return false;
        })
});  