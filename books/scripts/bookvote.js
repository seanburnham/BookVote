$(function(){

    $('[data-toggle="tooltip"]').tooltip();

    $(document).on('click', '#removeUserBtn', function(evt){
        
        $('#groupMembers').load('/books/bookvote.removeGroupMember/' + $('#groupGreeting').data('group') + '/' + $(this).data('user') + '/');
        evt.preventDefault();
        
    });

    $(document).on('click', '#acceptBtn', function(evt){
        
        $('#memberStuff').load('/books/bookvote.pendingApproval/' + $('#groupGreeting').data('group') + '/' + $(this).data('user') + '/' + $(this).data('id') + '/');
        evt.preventDefault();
        
    });

    $(document).on('click', '#rejectBtn', function(evt){
        
        $('#memberStuff').load('/books/bookvote.pendingApproval/' + $('#groupGreeting').data('group') + '/' + $(this).data('user') + '/' + $(this).data('id') + '/');
        evt.preventDefault();
        
    });

    $(document).on('click', '#upVote', function (evt){

        $('#bookStuff').load('/books/bookvote.upVote/' + $('#groupGreeting').data('group') + '/' + $(this).data('id') + '/');
        evt.preventDefault();

    });

    $(document).on('click', '#downVote', function (evt){

        $('#bookStuff').load('/books/bookvote.downVote/' + $('#groupGreeting').data('group') + '/' + $(this).data('id') + '/');
        evt.preventDefault();

    });

    $(document).on('click', '#addAdminBtn', function (evt){

        userID = $('input[name=userListBtn]:checked').val();
        
        if (userID){
            $('#newAdminModal').modal('hide');

            $('#memberStuff').load('/books/bookvote.addAdminUser/' + $('#groupGreeting').data('group') + '/' + userID + '/');
            evt.preventDefault();
        }

        

    });


    $(document).on('click', '.btn-warning', function (evt){

        //This isn't catching errors correctly and needs to be fixed. 
        //Also there needs to be an alert that is triggered when someone 
        //   tries to add a book they have already added or voted on for that group.

        $('#bookStuff').load('/books/bookvote.addToList/' + $(this).data('group')+ '/' + $(this).data('book')  + '/');
        $('.alert-success').fadeIn()
        setTimeout(function() {
            $('.alert-success').fadeOut(); 
        }, 4000);
        evt.preventDefault();

        // $('.alert-danger').fadeIn() //or fadeIn
        // setTimeout(function() {
        //     $('.alert-danger').fadeOut(); //or fadeOut
        // }, 4000);

    });

})



function bookSearch() {
    document.getElementById('resultsDiv').style.display = "block";
    var groupID = $('#groupGreeting').data('group')
    var search = document.getElementById('search').value;
    document.getElementById('searchResults').innerHTML = "";

    // $.getJSON('http://www.whateverorigin.org/get?url=' + encodeURIComponent('http://google.com') + '&callback=?', function(data){
    //     alert(data.contents);
    // });

    // var url = "https://www.goodreads.com/search?q=" + search + "&format=xml&key=Te7ahdToiP8n7iV3Lpgw6g";

    var url = "https://www.goodreads.com/search.xml?key=Te7ahdToiP8n7iV3Lpgw6g&q=" + encodeURI(search);

    // $.get('http://cors-anywhere.herokuapp.com/' + url, function(xml){
    //     console.log(xmlToJson(xml)['GoodreadsResponse']['search']['results']['work']);
    // });


    $.get("http://cors-anywhere.herokuapp.com/" + url, 
        function (xml) {
            // contains XML with the following structure:
            // <query>
            //   <results>
            //     <GoodreadsResponse>
            //        ...
            // console.log(JSON.stringify(xmlToJson(xml)))

            var books = xmlToJson(xml)['GoodreadsResponse']['search']['results']['work']
            for (b in books){
                // var aveRating = books[b]['average_rating']['#text'];
                var bookID = books[b]['best_book']['id']['#text'];
                var title = books[b]['best_book']['title']['#text'];
                var author = books[b]['best_book']['author']['name']['#text'];
                var imageURL = books[b]['best_book']['small_image_url']['#text'];

                searchResults.innerHTML += '<li class="list-group-item list-group-item"> <img src="' +
                imageURL + '"/>' + '<div class="titleDiv align-middle"> <p>' + title + ' - ' +
                author + '</p> </div>' + '<button class="btn btn-warning" data-group="' + groupID + '" data-book="' + bookID  + '">+</button> </li>';

            }
        }
    );


    // $.ajax({
    //     //https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=yourAPIKey
    //     // https://www.goodreads.com/search.xml?key=" + goodReadsKey + "&q=" + isbn
    //     // url: "https://www.googleapis.com/books/v1/volumes?q=" + search + "&key=AIzaSyDNoBh8E3DyB1PTktxBE2ZLpIK2kIPipS4",
    //     url: "https://www.goodreads.com/search.xml?key=Te7ahdToiP8n7iV3Lpgw6g&q=" + search,
    //     dataType: "xml",
    //     cache: false,
    //     csrfmiddlewaretoken: $("input[name='csrfmiddlwaretoken']").val(),

    //     success: function (data) {
    //         console.log(data)
    //         // for (i = 0; i < data.items.length; i++) {
    //         //     if(data.items[i].volumeInfo.industryIdentifiers[0].type == 'ISBN_13'){
    //         //         var isbn = data.items[i].volumeInfo.industryIdentifiers[0].identifier;
    //         //     }
    //         //     else{
    //         //         var isbn = data.items[i].volumeInfo.industryIdentifiers[1].identifier;
    //         //     }
    //         //     // var isbn = data.items[i].volumeInfo.industryIdentifiers[0].identifier;
    //         //     searchResults.innerHTML += '<li class="list-group-item list-group-item"> <img src="' +
    //         //         data.items[i].volumeInfo.imageLinks.smallThumbnail + '"/>' + '<div class="titleDiv align-middle"> <p>' + data.items[i].volumeInfo.title + ' - ' +
    //         //         data.items[i].volumeInfo.authors + '</p> </div>' + '<button class="btn btn-warning" data-group="' + groupID +  '" data-id="'+ isbn + '">+</button> </li>';
    //         // }
    //     },
    //     type: 'GET'
    // });

}
 
// Changes XML to JSON
function xmlToJson(xml) {

    // Create the return object
    var obj = {};

    if (xml.nodeType == 1) { // element
        // do attributes
        if (xml.attributes.length > 0) {
            obj["@attributes"] = {};
            for (var j = 0; j < xml.attributes.length; j++) {
                var attribute = xml.attributes.item(j);
                obj["@attributes"][attribute.nodeName] = attribute.nodeValue;
            }
        }
    } else if (xml.nodeType == 3) { // text
        obj = xml.nodeValue;
    }

    // do children
    if (xml.hasChildNodes()) {
        for (var i = 0; i < xml.childNodes.length; i++) {
            var item = xml.childNodes.item(i);
            var nodeName = item.nodeName;
            if (typeof (obj[nodeName]) == "undefined") {
                obj[nodeName] = xmlToJson(item);
            } else {
                if (typeof (obj[nodeName].push) == "undefined") {
                    var old = obj[nodeName];
                    obj[nodeName] = [];
                    obj[nodeName].push(old);
                }
                obj[nodeName].push(xmlToJson(item));
            }
        }
    }
    return obj;
};