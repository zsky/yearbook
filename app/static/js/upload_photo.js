$(document).ready(function(){

    var files = document.getElementById("photo_input");
    var preview = document.getElementById("preview");
    files.addEventListener("change", handleFiles, false);
    function handleFiles(){
        preview.style.display = "block";
        var fileList = this.files;
        for(var i = 0, numFiles = fileList.length; i < numFiles; i++){
            file = fileList[i];
            console.log(file);
            var img = document.createElement("img");
            img.classList.add("preview_img");
            img.file = file;
            preview.appendChild(img);
            var reader = new FileReader();
            reader.onload = (function(aImag) { return function(e){
                aImag.src = e.target.result;};})(img);
            reader.readAsDataURL(file);

        }
    }

    var crop_div = $('.crop_div');
    $(function(){
        $('.crop_div').draggable({containment: $('#preview')});
    });

    $('.upload_photo').on('click', function(){
        var preview_img = $('.preview_img');
        var crop_x = crop_div.offset().left - preview_img.offset().left; 
        var crop_y = crop_div.offset().top - preview_img.offset().top; 
        var crop_width = crop_div.width();
        var crop_height = crop_div.height();

        var img_width = preview_img.width();
        var img_height = preview_img.height();
        var img = preview_img[0];
        var formData = new FormData();
        formData.append('user_image', img.file);
        formData.append('crop_x', crop_x/img_width);
        formData.append('crop_y', crop_y/img_height);
        formData.append('crop_width', crop_width/img_width);
        formData.append('crop_height', crop_height/img_height);
        $.ajax({
            type: "POST",
            url: "/update_photo",
            processData: false,
            contentType: false,
            data: formData
        }).done(function(image_url){
            preview.style.display = "none";
            $('.user_avatar').attr('src', image_url);

        });


    });
})
