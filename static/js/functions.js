function AddToElement(price){
  document.getElementById("price").innerHTML = price;
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







// function myFunction(labels, figures) {
//   var ctx = document.getElementById('myChart');
// //
// //   var stars = figures;
// //   var frameworks = labels;
// //   var myChart = new Chart(ctx, {
// //           type: 'bar',
// //           data: {
// //               labels: frameworks,
// //               datasets: [{
// //                   label: 'Number Of Purchases',
// //                   data: stars
// //               }]
// //           }
// //           options: {
// //             scales: {
// //               y: {
// //                 suggestedMin: 0
// //         }
// //     }
// // }
// //   })
// // }
//
// var chart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//         datasets: [{
//             label: 'Number Of Purchases',
//             data: figures
//         }],
//         labels: labels
//     },
//     options: {
//         scales: {
//           y: {
//             beginAtZero: true
//           }
//         }
//     }
// });
// }
