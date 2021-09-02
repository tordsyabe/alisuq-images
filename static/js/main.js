function previewImages(files) {
  const imagePreview = $("#imagePreview");
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

$(document).ready(function () {
  $("#images").on("change", function () {
    const files = [...$(this).prop("files")];
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
    });
  });
});
