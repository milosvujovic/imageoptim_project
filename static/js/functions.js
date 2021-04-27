function AddToElement(price){
  document.getElementById("price").innerHTML = "Price " + ' $ ' +  price;
};
function readPrice() {
  //   var command = '/GetPrices';
  var command = '/GetPrices/'  + document.forms["typeOfLicence"]["tier"].value +'/' +document.forms["typeOfLicence"]["length"].value;
  // alert(command);
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", command, true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState === 4) {
      if (xhttp.status === 200) {
        var text = xhttp.responseText;
        var price = JSON.parse(text);
        AddToElement(price);
        }
        else {
        console.error(xhttp.statusText);
      }
    }
  };
  xhttp.send();
  return false;
};
function alertUser(message) {
  if (message.length > 0){
    alert(message);
  }
}
