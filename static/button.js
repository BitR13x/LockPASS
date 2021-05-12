function darkmode() {
  var element = document.body;
  element.classList.toggle("white-mode");

  //var texth1 = document.getElementById("text")
  //texth1.classList.toggle("textdark")

}

function toggleSwitch(event) {
  // console.log(event.keyCode)

  if (event.keyCode === 112) {
    document.getElementById("checkb").click()

  }
}
