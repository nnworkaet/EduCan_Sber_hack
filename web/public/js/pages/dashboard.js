var myDropzone = new Dropzone(".dropzone-div", { 
    url: "./src/Api/v1.php?uploadNewAudio",
    autoProcessQueue: false,
    acceptedFiles: "audio/*",
    uploadMultiple: false,
    maxFilesize: 100000000
});

myDropzone.on("sending", function(file, xhr, formData) {
    var lectureName = $('.lecture-name-input').val();
    formData.append('lectureName', lectureName);

    $(".upload-button").prop("disabled", true);
});

myDropzone.on("success", function(file, response) {
    appendDivWithScript(response);

    $(".upload-button").prop("disabled", false);
});

$('button').on('click', function() {
    var lectureName = $('.lecture-name-input').val();

    if (!lectureName) {
        addNotification("Ошибка загрузки", "Заполните поле с названием лекции!", "Danger");
    } else {
        myDropzone.processQueue();
    }
});

$(".dropzone-label").click((e) => {
    e.preventDefault();
});