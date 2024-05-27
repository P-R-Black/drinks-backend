const navBarMenu = document.querySelector('.navbar_menu'); //primaryNav
const hamburger = document.querySelector('.hamburger_menu'); //NavToggle

const navBarDropdownArrow = document.querySelector('.navbar_link_dropdown');
const navBarDropdown = document.querySelector('.nav_dropdown');

hamburger.addEventListener('click', () =>{
    const visibility = navBarMenu.getAttribute('data-visible')
    if(visibility === "false"){
        navBarMenu.setAttribute('data-visible', 'true')
        hamburger.setAttribute('aria-expanded', 'true')
    } else {
        visibility === "true"
        navBarMenu.setAttribute('data-visible', 'false')
        hamburger.setAttribute('aria-expanded', 'false')
    }
})

navBarDropdownArrow.addEventListener('click', () => {
    navBarDropdown.classList.toggle('show')
})


navBarDropdown.addEventListener('click', () => {
    navBarDropdown.classList.remove('show')
})
