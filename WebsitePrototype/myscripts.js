var sidebarOpen = false

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    if(sidebarOpen){
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("main").style.marginLeft = "0";
        sidebarOpen = false;
    } else {
        document.getElementById("mySidenav").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
        sidebarOpen = true;
        doSomething(0);
    }
    
}
  
/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
} 

var wrap = document.getElementById("wrap");

function doSomething() {
  if (document.getElementById("wrap").scrollTop > 197) {
    document.getElementById("wrap").className = 'wrap fix-search';
  } else {
    document.getElementById("wrap").className = 'wrap';
  }
}

