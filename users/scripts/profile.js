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

});
