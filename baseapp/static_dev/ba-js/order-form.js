makeOrderBtn = document.querySelector('#make-order');
quitWithFormBtn = document.querySelector('#modal-quit');

makeOrderBtn.onclick = modalWindowShow;
quitWithFormBtn.onclick = modalWindowQuit;

formInstance = document.querySelector('#modal-form');

function modalWindowShow() {
    formInstance.style.display = 'block';
}

function modalWindowQuit() {
    formInstance.style.display = 'none';
}