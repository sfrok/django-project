makeOrderBtn = document.querySelector('#make-order');
quitWithFormBtn = document.querySelector('#modal-quit');

makeOrderBtn.onclick = modalWindowShow;
quitWithFormBtn.onclick = modalWindowQuit;

formInstance = document.querySelector('#modal-form');
overlay = document.querySelector('.hide');

function modalWindowShow() {
    formInstance.style.display = 'block';
    overlay.classList.remove('hide')
}

function modalWindowQuit() {
    overlay.classList.add('hide');
    formInstance.style.display = 'none';
}