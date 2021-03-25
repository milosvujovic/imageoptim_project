// function addToBasket(licenceID) {
//   var tier = document.forms["typeOfLicence"]["tier"].value;
//   var length = document.forms["typeOfLicence"]["length"].value;
//   params = 'licenceID='+licenceID+'&tier='+tier+'&length='+length;
//   var xhttp = new XMLHttpRequest();
//   xhttp.open("POST", '/gatherLicenceData', true);
//   xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//   xhttp.onreadystatechange = function() {
//     if (xhttp.readyState === 4 && xhttp.status === 200) {
//       console.log(xhttp.responseText);
//     } else {
//       console.log(xhttp.statusText);
//     }
//   };
//   xhttp.send(params);
//   // window.location.href = location.origin + "/"
//   return false;
// }
