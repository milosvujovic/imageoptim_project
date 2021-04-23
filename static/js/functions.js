function alertUser(message) {
  if (message.length > 0){
    alert(message);
  }
}
function myFunction(labels, figures) {
  var ctx = document.getElementById('myChart');
//
//   var stars = figures;
//   var frameworks = labels;
//   var myChart = new Chart(ctx, {
//           type: 'bar',
//           data: {
//               labels: frameworks,
//               datasets: [{
//                   label: 'Number Of Purchases',
//                   data: stars
//               }]
//           }
//           options: {
//             scales: {
//               y: {
//                 suggestedMin: 0
//         }
//     }
// }
//   })
// }

var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        datasets: [{
            label: 'Number Of Purchases',
            data: figures
        }],
        labels: labels
    },
    options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
    }
});
}
