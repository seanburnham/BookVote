function addGroup() {

    // alert($('input[name=groupListBtn]:checked').val())

    
    $('#groupListModal').modal('hide');
    $('#selectGroup').load('/homepage/index.addGroup/' + $('input[name=groupListBtn]:checked').val());
    
}


function myFunction() {

    var input = document.getElementById("myInput");
    var filter = input.value;
    gridContainer = document.getElementById("gridContainer");
    gridItems = gridContainer.getElementsByClassName("form-check");

    for (i = 0; i < gridItems.length; i++) {
        label = gridItems[i].getElementsByTagName("label")[0];
        if (label.innerHTML.toLowerCase().indexOf(filter) > -1) {
            gridItems[i].style.display = "";
        } else {
            gridItems[i].style.display = "none";

        }
    }
}