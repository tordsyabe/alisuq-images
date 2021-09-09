$(document).ready(function () {
  function previewImages(files) {
    const imagePreview = $("#imagePreview");

    imagePreview.css("margin-top", "5rem");

    if (imagePreview.children()) {
      imagePreview.children().remove();
    }
    images = "";

    for (let i = 0; i < files.length; i++) {
      images += `
      <div class="upload-preview">
        <img src="${URL.createObjectURL(
          files[i]
        )}" class="upload-preview__img" data-img-idx="${i}" alt="${
        files[i].name
      }"/><span></span>
      </div>
      `;
    }
    imagePreview.append(images);
  }

  $("#uploadForm").submit(function (e) {
    e.preventDefault();

    $("#uploadBtn").attr("disabled", true);
    $("#uploadBtn").val("Processing images...");
    $(".upload-percentage").css("display", "block");
    const category = $("input[name=category").val();
    const usage = $("input[name=usage").val();

    var form_data = new FormData();
    var ins = document.getElementById("images").files.length;

    for (var x = 0; x < ins; x++) {
      form_data.append("images", document.getElementById("images").files[x]);
      form_data.append("category", category);
      form_data.append("usage", usage);
    }

    $.ajax({
      type: "POST",
      url: "/",
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      xhrFields: {
        responseType: "blob",
      },
      xhr: function () {
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener(
          "progress",
          function (evt) {
            if (evt.lengthComputable) {
              var percentComplete = (evt.loaded / evt.total) * 100;
              console.log(percentComplete);
              $(".upload-percentage__value").html(parseInt(percentComplete));
            }
          },
          false
        );
        return xhr;
      },
      success: function (blob) {
        var link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "masked_images_" + new Date() + "zip";
        link.click();
        $("#uploadBtn").attr("disabled", false);
        $("#uploadBtn").val("Mask & Resize");
        $(".upload-percentage").css("display", "none");
      },
      error: function (e) {
        $(".error-message span").css("display", "flex");
        $("#uploadBtn").attr("disabled", false);
        $("#uploadBtn").val("Mask & Resize");
      },
    });
  });

  $(".error-message span").on("click", function (e) {
    $(this).parent().css("display", "none");
  });

  $("#uploadBtn").attr("disabled", true);

  $("#images").on("change", function () {
    const files = [...$(this).prop("files")];
    $("#noOfImages").html(files.length);
    if (files.length > 0) {
      $("#uploadBtn").attr("disabled", false);
    }
    previewImages(files);
    console.log("IMAGES FILES", files);

    $(".upload-preview span").on("click", function (e) {
      e.stopPropagation();
      e.preventDefault();

      $(this).parent().remove();
      const imgIdx = $(this).prev().attr("img-idx");
      var uploader = document.getElementById("images");

      files.splice(imgIdx, 1);

      const newFileList = new DataTransfer();
      files.forEach((file) => {
        const newFile = new File(
          [new Blob([file], { type: file.type })],
          file.name
        );

        newFileList.items.add(newFile);
      });
      uploader.files = newFileList.files;
      if (uploader.files.length === 0) {
        $("#uploadBtn").attr("disabled", true);
        $("#imagePreview").css("margin-top", 0);
      }
      $("#noOfImages").text(uploader.files.length);
    });
  });
});
