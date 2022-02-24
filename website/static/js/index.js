function deleteNote(noteId){
    fetch('delete-note',{
        method: 'POST',
        body: JSON.stringify({ noteId: noteId})
    }).then((_res)=>{
        window.location.href= "/note";
    });
}


var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  })


function deleteNote(noteId){
    fetch('delete-note',{
        method: 'POST',
        body: JSON.stringify({ noteId: noteId})
    }).then((_res)=>{
        window.location.href= "/";
    });
}