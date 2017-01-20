    function load_qr(){
        var usd_amount = $('#id_amount').val();
        var invoice_key = '{{ request.session.session_key }}';
        var cart_pk = '{{ request.cart.pk }}';
        $.getJSON( '/create.php', {invoice_key:invoice_key, cart_pk: cart_pk, usd_amount:usd_amount}, function(data) {
            var addr = data['input_address'];
            var btc_amount = data['btc_amount'];
            var url = data['url'];
            $('#amount_to_pay').html(btc_amount+'BTC ($'+usd_amount+')');
            $('#qrcode').attr('src',url);
            $('#btc_addr').html(addr);
        });
    }
