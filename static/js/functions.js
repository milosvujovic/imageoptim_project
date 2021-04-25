function myFunction(labelsNumber, figuresNumber,labelRev, figuresREv,labelLength, figureLength ) {
  var dataNumber = {
  labels: labelsNumber,
  datasets: [{
    label: 'Purchase History',
    data: figuresNumber,
    backgroundColor:
      'rgba(255, 99, 132, 0.2)',
    borderColor:
      'rgb(255, 99, 132)',
    borderWidth: 1
  }]
};

  var ctx = document.getElementById('numberChart');
  var numberChart = new Chart(ctx, {
    type: 'bar',
    data: dataNumber,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  var dataRevenue = {
  labels: labelRev,
  datasets: [{
    label: 'Revenue',
    data: figuresREv,
    backgroundColor:
      'rgba(255, 99, 132, 0.2)',
    borderColor:
      'rgb(255, 99, 132)',
    borderWidth: 1
  }]
};

  var chartRevenue = document.getElementById('revenueChart');
  var numberChart = new Chart(chartRevenue, {
    type: 'line',
    data: dataRevenue,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  var dataLength = {
    labels: labelLength,
      datasets: [{
        label: 'Number of Purchase for length',
        data: figureLength,
        backgroundColor:
          'rgba(255, 99, 132, 0.2)',
        hoverOffset: 4
      }]
};

  var chartLength = document.getElementById('lengthChart');
  var lengthChart = new Chart(chartLength, {
    type: 'pie',
    data: dataLength,
  });
};
function AddToElement(price){
  document.getElementById("price").innerHTML = '$' +  price;
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
