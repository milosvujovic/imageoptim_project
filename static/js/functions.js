function myFunction(label, figure,title, type) {
  $("#chart-container").empty();
  var canvas = document.createElement('canvas'),
      div = document.getElementById("chart-container");
  canvas.id     = "chart";
  canvas.class     = 'img-responsive';
  div.appendChild(canvas);

  var dataNumber = {
  labels: label,
  datasets: [{
    label: title,
    data: figure,
    backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
    ],
    borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
    ],
    borderWidth: 1
  }]
};

  var ctx = document.getElementById('chart');
  var numberChart = new Chart(ctx, {
    type: type,
    data: dataNumber,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });


};
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
};
