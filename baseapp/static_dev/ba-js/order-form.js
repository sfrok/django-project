makeOrderBtn = document.querySelector('#make-order');
quitWithFormBtn = document.querySelector('#modal-quit');
orderEffect = document.querySelector('#order-effect');

makeOrderBtn.onclick = modalWindowShow;
quitWithFormBtn.onclick = modalWindowQuit;

formInstance = document.querySelector('#modal-form');

function modalWindowShow() {
    formInstance.style.display = 'block';
    orderEffect.style.backgroundColor = 'rgba(0,0,0,0.5)';
    orderEffect.style.position = 'absolute';
    orderEffect.style.width = '100%';
    orderEffect.style.height = '100%';

}

function modalWindowQuit() {
    formInstance.style.display = 'none';
    orderEffect.style.backgroundColor = '';
}