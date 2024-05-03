
window.addEventListener('selectstart', function(e){ e.preventDefault(); });
$(document).ready(function () {
    //Disable cut copy paste
    $('body').bind('select cut copy paste', function (e) {
        e.preventDefault();
    });
    
    //Disable mouse right click
    $("body").on("contextmenu",function(e){
        return false;
    });
});
/** TO DISABLE SCREEN CAPTURE **/
document.addEventListener('keyup', (e) => {
if (e.key == 'PrintScreen') {
navigator.clipboard.writeText('');
alert('Screenshots disabled!');
}
});

/** TO DISABLE PRINTS WHIT CTRL+P **/
document.addEventListener('keydown', (e) => {
if (e.ctrlKey && e.key == 'p') {
    alert('This section is not allowed to print or export to PDF');
    e.cancelBubble = true;
    e.preventDefault();
    e.stopImmediatePropagation();
}
});

