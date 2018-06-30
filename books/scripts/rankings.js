var groupID = ""
var bookID = ""

$(function(){

    $(document).on('show.bs.modal', '#deadlinePicker', function (e) {
        groupID = $(e.relatedTarget).data('id');
        bookID = $(e.relatedTarget).data('book');

    });


    $(document).on('click', '#deadlineBtn', function (evt){

        var deadline = $( "input[type=date][name=deadline]" ).val();

        ///Check to make sure date selected is in the future
        var dt = new Date(deadline)
        var today = new Date()

        if(dt > today){
            var group = groupID;
            var book = bookID;
    
            var csrftoken = Cookies.get('csrftoken');
            $.ajax({
                type: 'POST',
                url: '',
                data: {
                    deadline: deadline,
                    group: group,
                    book: book,
                    csrfmiddlewaretoken: csrftoken,
                },
                cache: false,
                traditional: true,
                success: function(response){
                    console.log('Success');
                    $('#deadlinePicker').modal('hide');
                    window.location.replace("https://bookvotingapp.herokuapp.com/books/bookvote/" + groupID);
                },
            });
        }
        else{
            alert('Please select a deadline in the future.')
        }

        
    });
});

