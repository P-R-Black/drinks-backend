const navBarMenu = document.querySelector('.navbar_menu'); //primaryNav
const hamburger = document.querySelector('.hamburger_menu'); //NavToggle


hamburger.addEventListener('click', (e) =>{
    e.preventDefault()
    const visibility = navBarMenu.getAttribute('data-visible')
    if(visibility === "false"){
        navBarMenu.setAttribute('data-visible', 'true')
        hamburger.setAttribute('aria-expanded', 'true')
    } else {
        visibility === "true"
        navBarMenu.setAttribute('data-visible', 'false')
        hamburger.setAttribute('aria-expanded', 'false')
    }
});

