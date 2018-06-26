$(function(){

    $('#id_is_private').change(function(){
        if(this.checked)
            $('#id_passphrase').fadeIn('slow');
        else
            $('#id_passphrase').fadeOut('slow');

    });

})