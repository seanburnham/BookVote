var groupID = ""
var bookID = ""

$(function(){

    $(document).on('show.bs.modal', '#deadlinePicker', function (e) {
        groupID = $(e.relatedTarget).data('id');
        bookID = $(e.relatedTarget).data('book');

    });


    $(document).on('click', '#deadlineBtn', function (evt){

        var deadline = $( "input[type=date][name=deadline]" ).val();
        var group = groupID;
        var book = bookID;

        console.log(deadline, group, book)

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
                window.location.replace("http://localhost:8000/books/bookvote/" + groupID);
            },
        });
    });
});

