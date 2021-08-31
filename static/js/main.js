$(document).ready(function () {
  $("#images").on("change", function () {
    const imagePreview = $("#imagePreview");
    images = "";

    const files = $(this).prop("files");

    for (let i = 0; i < files.length; i++) {
      images += `<img src="${URL.createObjectURL(files[i])}" alt="${
        files[i].name
      }" width="100" height="100"/><br />`;
    }

    imagePreview.append(images);
  });
});
