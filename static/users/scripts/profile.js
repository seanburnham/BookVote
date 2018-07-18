$(function(){

    // $('[data-toggle="tooltip"]').tooltip();

    $(document).on('click', '#leaveGroupBtn', function(evt){
        
        if ($(this).data('admin') == "True"){
            $('.alert-danger').fadeIn() //or fadeIn
            setTimeout(function() {
                $('.alert-danger').fadeOut(); //or fadeOut
            }, 4000);
        }
        else{
            $('#currentGroups').load('/users/profile.leaveGroup/' + $(this).data('group') + '/');
            evt.preventDefault();
        }
        
    });


    $(document).on('click', '#saveSettingsBtn', function(evt){
        
        if ($('#emailNotification').is(':checked')) {
            $.ajax({
                type:'POST',
                url: '/users/profile.update_settings/',
                data : {
                    settings: 1,
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                },
                cache: false,
                traditional: true,
                success: function(data){
                },
            });
        }
        else{
            $.ajax({
                type:'POST',
                url: '/users/profile.update_settings/',
                data : {
                    settings: 0,
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                },
                cache: false,
                traditional: true,
                success: function(data){
                },
            });
        }

        //Hide modal
        $('#settingsModal').modal('hide');

    });


});


function ChangeCheckboxLabel(ckbx)
{
   if( ckbx.checked )
   {
       document.getElementById(id="emailLabel").innerHTML = 'Opt out of all email notifications';
   }
   else
   {
       document.getElementById(id="emailLabel").innerHTML = 'Opt in to all email notifications';
   }
}

