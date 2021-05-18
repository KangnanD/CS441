Dropzone.autoDiscover = false;

// Dropzone class:
var myDropzone = new Dropzone("div#mydropzone",
    {
        url: "/files/upload/",
        addRemoveLinks:true,
        parallelUploads: 1
    });

// If you use jQuery, you can use the jQuery plugin Dropzone ships with:
//$("div#myDrop").dropzone({ url: "/file/post" });
$(document).ready(function() {
        $('.file-remove').on("click",function(){
            let id= $(this).attr('id');
             $.ajax({
                url: '/files/delete/',
                type:'POST',
                async: false,
                data: {
                  'id': id
                },
                dataType: 'json',
                success: function (response) {
                    window.location.reload(true);
                },
                error:function(response){
                    console.log("Error deleting files");
                }
              });

        });
});
