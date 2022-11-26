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