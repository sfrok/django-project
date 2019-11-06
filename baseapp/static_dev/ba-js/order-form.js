makeOrderBtn = document.querySelector('#make-order');
quitWithFormBtn = document.querySelector('#modal-quit');

makeOrderBtn.onclick = modalWindowShow;
quitWithFormBtn.onclick = modalWindowQuit;

formInstance = document.querySelector('#modal-form');
overlay = document.querySelector('.hide');


counterPlusProductCart = document.querySelector('.plus');
counterMinusProductCart = document.querySelector('.minus');

let clickPlus = counterPlusProductCart.onclick = plusProduct;
let clickMinus = counterMinusProductCart.onclick = minusProduct;

function modalWindowShow() {
    formInstance.style.display = 'block';
    overlay.classList.remove('hide')
}

function modalWindowQuit() {
    overlay.classList.add('hide');
    formInstance.style.display = 'none';
}

function plusProduct() {
    let upCounter = document.querySelector('#product-count');
    let makeInt = parseInt(upCounter.value);
    if (clickPlus && makeInt){
        makeInt += 1;
        upCounter.value= makeInt;


        let upMainCounter = document.querySelector('#main-count');
        let makeMainInt = parseInt(upMainCounter.innerText);
        makeMainInt += 1;
        upMainCounter.innerText = makeMainInt;
    }

}

function minusProduct() {
    let upCounter = document.querySelector('#product-count');
    let makeInt = parseInt(upCounter.value);
    if (clickMinus && makeInt > 1){
        makeInt -= 1;
        upCounter.value = makeInt;

        let upMainCounter = document.querySelector('#main-count');
        let makeMainInt = parseInt(upMainCounter.innerText);
        makeMainInt -= 1;
        upMainCounter.innerText = makeMainInt;
    }
}