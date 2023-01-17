const navBar = document.querySelector(".nav-container");
const menuMobile = document.querySelector(".container-menu-mobile");
const listMenu = document.querySelector(".list-menu");
let stateOfMenu = false;
menuMobile.addEventListener("click", openMenu);
    
function openMenu() {
    if (stateOfMenu) {
        navBar.style.width = "3px";
        menuMobile.style.left = "0";
        stateOfMenu = false;
    } else {
        menuMobile.style.left = "150px";
        navBar.style.width = "150px";
        stateOfMenu = true;
    }
}

function deleteRecipe() {
    // pega todos os botões de deletar do formulário
    const forms = document.querySelectorAll('.RA__delete_button');

    // laço for of
    for (const form of forms) {
        // adiciona evento de submit em cada botão
        form.addEventListener('submit', function(event) {
            // isso previne o envio padão do formulário ao servidor
            event.preventDefault();

            // criamos um alert de confirmação no navegador
            const toConfirm = confirm('Deseja realmente deletar a receita?');
    
            // se for confirmado, o formulário é enviado ao servidor e a receita
            // é deletada
            if (toConfirm) {
                form.submit();
            };

        })
    }
};

// chama a função
deleteRecipe();

document.addEventListener("click", function(event) {
    const element = event.target;

    if (element.classList.contains("messages_element")) {
        element.parentElement.remove();
    }
})