function openNav() {
  document.getElementById("sidenav").style.width = "23vw";
  document.getElementById("openbtn").style.opacity = "0";
  document.getElementById("closebtn").style.opacity = "100";
  
}

function closeNav() {
  document.getElementById("sidenav").style.width = "0";
  document.getElementById("openbtn").style.opacity = "100";
  document.getElementById("closebtn").style.opacity = "0";
}