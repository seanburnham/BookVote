$(function(){

    $(document).on('click', '#upVote', function (evt){

        $('#bookStuff').load('/books/bookvote.upVote/' + $(this).data('id') + '/');
        evt.preventDefault();

    });

    $(document).on('click', '#downVote', function (evt){

        $('#bookStuff').load('/books/bookvote.downVote/' + $(this).data('id') + '/');
        evt.preventDefault();

    });

})



function bookSearch() {
    var search = document.getElementById('search').value;
    document.getElementById('searchResults').innerHTML = "";

    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=" + search, // + ":keyes&key=AIzaSyDNoBh8E3DyB1PTktxBE2ZLpIK2kIPipS4",
        dataType: "json",

        success: function (data) {
            console.log(data)
            for (i = 0; i < data.items.length; i++) {
                if(data.items[i].volumeInfo.industryIdentifiers[0].type == 'ISBN_13'){
                    var isbn = data.items[i].volumeInfo.industryIdentifiers[0].identifier;
                }
                else{
                    var isbn = data.items[i].volumeInfo.industryIdentifiers[1].identifier;
                }
                // var isbn = data.items[i].volumeInfo.industryIdentifiers[0].identifier;
                searchResults.innerHTML += '<li class="list-group-item list-group-item"> <img src="' +
                    data.items[i].volumeInfo.imageLinks.smallThumbnail + '"/>' + '<div class="titleDiv align-middle"> <p>' + data.items[i].volumeInfo.title + ' - ' +
                    data.items[i].volumeInfo.authors + '</p> </div>' + '<button class="btn btn-warning" onclick="addBookToList(' + isbn + ');">+</button> </li>';
            }
        },
        type: 'GET'
    });

}


//url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn;

function addBookToList(isbn) {
    "use strict";
    
    $.when(
        $.ajax({
            url: "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn, // + ":keyes&key=AIzaSyDNoBh8E3DyB1PTktxBE2ZLpIK2kIPipS4",
            dataType: "json",
            type: 'GET'
        }).done(function (data) {
                var csrftoken = Cookies.get('csrftoken');
                $.ajax({
                    type: 'POST',
                    url: '',
                    data: {
                        title: data.items[0].volumeInfo.title,
                        isbn: data.items[0].volumeInfo.industryIdentifiers[1].identifier,
                        author: data.items[0].volumeInfo.authors,
                        image: data.items[0].volumeInfo.imageLinks.smallThumbnail,
                        description: data.items[0].volumeInfo.description,
                        avgRating: data.items[0].volumeInfo.averageRating,
                        pageCount: data.items[0].volumeInfo.pageCount,
                        csrfmiddlewaretoken: csrftoken,
                    },
                    cache: false,
                    traditional: true,
                    success: function (data){
                        $('.alert-success').fadeIn() //or fadeIn
                        setTimeout(function() {
                            $('.alert-success').fadeOut(); //or fadeOut
                        }, 4000);
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        console.log('ERROR==-=-=-=-=-=-=-=-=-=-=-=-=-=-')
                        $('.alert-danger').fadeIn() //or fadeIn
                        setTimeout(function() {
                            $('.alert-danger').fadeOut(); //or fadeOut
                        }, 4000);
                        
                    },
                });
            }

        )
    ).then(
        function (response) {
            console.log('Success');
        },
    )

}