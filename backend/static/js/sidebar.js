var selected = -1;
var buttons = document.getElementsByClassName("filter");

window.onload = function() {
    var win = document.getElementsByTagName("body")[0];
    win.style.width = window.screen.availWidth;
    win.style.height = window.screen.availHeight;
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].onclick = function () {
            for (let i = 0; i < buttons.length; i++) {
                if (buttons[i].name == this.name) {
                    selected = i;
                    buttons[i].style.backgroundColor = "rgb(47, 47, 189)";
                }
                else {
                    buttons[i].style.backgroundColor = "royalblue";
                }
            }
            listFile(buttons[i].name);
        };
        buttons[i].onmouseover = function () {
            this.style.backgroundColor = "rgb(47, 47, 189)";
        };
        buttons[i].onmouseout = function () {
            if (selected < 0 || this.name != buttons[selected].name) {
                this.style.backgroundColor = "royalblue";
            }
        };
    }
    listFile('all');
};