var filelist;

function listFile(type) {
    var getFileListRequest = new XMLHttpRequest();
    getFileListRequest.open("GET", "https://share.greyishsong.ink/filelist", true);
    getFileListRequest.send(null);
    getFileListRequest.onload = function () {
        filelist = this.responseText;
        filelist = JSON.parse(filelist);
        uptoDate = true;
        var board = document.getElementsByClassName("board")[0];
        board.innerHTML = "";
        board.style.justifyContent = "flex-start";
        board.style.alignItems = "flex-start";
        board.style.alignContent = "flex-start";
        for (let i = 0; i < filelist.length; i++) {
            const file = filelist[i];
            if (type == "all" || (type != "all" && file.type == type)) {
                board.innerHTML = `${board.innerHTML}
                    <a class=\"file\" href=\"https://share.greyishsong.ink/download/${file.filename}\" download=\"${file.filename}\">
                    <img class=\"file\" src=\"/static/icon/${file.type}.png\" alt=\"${file.type}\">
                    <p>${file.filename}</p>
                    </a>`;
            }
        }
    }
}

function selectFile() {

}
