var orderDivOpen = 0;
var itemName;
var totalPrice = 0.00;

document.addEventListener('DOMContentLoaded', () => {

  //when user clicks order now, open up order form
  Array.from(document.getElementsByClassName('order-now')).forEach(button => {
    button.onclick = () => {

      itemName = button.getAttribute('data-itemName');

      //determine size options to add to order popup
      var dropdown = document.getElementById("sizeDropdown");
      for (i=0; i<items.length; i++) {
        if (items[i].fields.name == itemName) {
          var maxToppings = items[i].fields.maxToppings;
          var sizeName = getSizeName(items[i].fields.size)
          dropdown.options[dropdown.options.length] = new Option(sizeName,sizeName);
        }
      }

      var itemID = findItemId();
      var hiddenItem = document.getElementById('itemIdInput');
      hiddenItem.value = itemID;


      //add addition options
      findAdds();

      //add topping dropdowns
      var toppingSection = document.getElementById('toppingSection');
      if (maxToppings > 0) {
        var toppingHeader = document.createElement('h4');
        toppingHeader.innerHTML = "Choose Toppings";
        toppingSection.appendChild(toppingHeader);
        toppingSection.style.display = 'block';
      }

      for (k=0; k < maxToppings; k++) {

        //create form row
        var row = document.createElement('div');
        row.classList.add('row');
        row.classList.add('my-1');
        row.classList.add('form-row');
        row.classList.add('justify-content-center');
        toppingSection.appendChild(row);

        //create topping dropdown
        var select = document.createElement('select');
        select.classList.add('form-control');
        select.id = 'topping_' + k;
        select.name = 'topping_' + k;
        for (l=0; l<toppings.length; l++) {
          select.options[select.options.length] = new Option(toppings[l].fields.name, toppings[l].pk);
        }
        row.appendChild(select);
      }

      //display hidden form
      document.getElementById("coverLayer").style.display = "block";
      document.getElementById("orderHeader").innerHTML = itemName;
      document.getElementById("orderDiv").style.display = "block";
      document.getElementById("sizeDropdown").focus();
      orderDivOpen = 1;
      calcPrice();
    }
  });

  //close orderDiv if user clicks outside orderDiv
  document.querySelector('#coverLayer').onclick = () => {
    if (orderDivOpen == 1) {
      hideOrderDiv();
    }
  };

  //close orderDiv if user hits cancel button
  document.querySelector('#cancelButton').onclick = () => {
    if (orderDivOpen == 1) {
      hideOrderDiv();
    }
  };

  //close orderDiv if user hits escape key
  document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode == 27) {
      if (orderDivOpen == 1) {
        hideOrderDiv();
      }
    }
  };

  //update item price when user changes size dropdown
  document.querySelector('#sizeDropdown').onchange = () => {
    var itemID = findItemId();
    var hiddenItem = document.getElementById('itemIdInput');
    hiddenItem.value = itemID;
    findAdds();
    calcPrice();
  };

  // //close orderDiv if user clicks outside orderDiv
  // document.querySelector('#addToCart').onclick = () => {
  //
  //   // find itemID
  //   var itemID = findItemId();
  //
  //
  //
  //   //
  //   var checks = Array.from(document.getElementsByClassName('extraCheckbox'));
  //   var extras = [];
  //   for (i = 0; i<checks.length;i++) {
  //     if (checks[i].checked == true) {
  //       extras.append(checks[i].value);
  //     }
  //   }
  // };

});

//find the name of a size given the primary key
function getSizeName(pk) {
  for (j=0; j<sizes.length; j++) {
    if (pk == sizes[j].pk) {
      return sizes[j].fields.name;
    }
  }
  return 'invalid';
}

//hide the orderDiv
function hideOrderDiv () {
  //hide order form
  document.getElementById("coverLayer").style.display = "none";
  document.getElementById("orderDiv").style.display = "none";

  //clear size dropdown options
  var dropdown = document.getElementById("sizeDropdown");
  for (i in dropdown.options) {
    dropdown.options.remove(0);
  }

  //clear topping dropdown rows
  var toppingSection = document.getElementById("toppingSection");
  while (toppingSection.firstChild) {
    toppingSection.removeChild(toppingSection.firstChild);
  }

  orderDivOpen = 0;
}

//determine addition options for this item
function findAdds () {

  var extrasSection = document.getElementById("extrasSection");
  var numExtras = 0;

  //remove existing additions
  while(extrasSection.firstChild) {
    extrasSection.removeChild(extrasSection.firstChild);
  }
  extrasSection.style.display = "none";

  // find itemID
  var itemID = document.getElementById('itemIdInput').value;

  //use itemID to find additions and add to form
  for (j=0; j<additions.length; j++) {
    if (additions[j].fields.item == itemID) {
      if (numExtras == 0) {
        var extrasHeader = document.createElement('h4');
        extrasHeader.innerHTML = "Choose Extras";
        extrasSection.appendChild(extrasHeader);
      }

      //create row
      var row = document.createElement('div');
      row.id = 'row_' + additions[j].pk
      row.classList.add('d-flex');
      row.classList.add('my-1');
      row.classList.add('form-row');
      document.getElementById('extrasSection').appendChild(row);

      //create checkbox
      var key = additions[j].pk;
      var addName = additions[j].fields.name
      var checkbox = document.createElement('input');
      checkbox.type = "checkbox";
      checkbox.id = 'check_' + numExtras;
      checkbox.value = key;
      checkbox.name = 'check_' + numExtras;
      checkbox.dataset.price = additions[j].fields.additionPrice;
      checkbox.classList.add('mx-1');
      checkbox.classList.add('extraCheckbox');
      checkbox.classList.add('form-check-input');
      checkbox.onclick = () => {
        calcPrice();
      }

      //create label
      var newLabel = document.createElement("label");
      newLabel.htmlFor = 'check_' + numExtras;
      newLabel.name = 'label_' + addName;
      newLabel.classList.add('mx-1');
      newLabel.classList.add('form-check-label');

      //add to form
      document.getElementById('row_' + key).appendChild(checkbox);
      newLabel.appendChild(document.createTextNode(addName));
      document.getElementById('row_' + key).appendChild(newLabel);
      numExtras += 1;
    }
  }
  if (numExtras > 0) {
    extrasSection.style.display = "block";
  }
}

//calculate price based on parameters on orderDiv
function calcPrice () {
  totalPrice = 0.00;


  //calculate base price
  var dropdown = document.getElementById("sizeDropdown");
  var selectedSize = dropdown.options[dropdown.selectedIndex].value;
  for (i=0; i<items.length; i++) {
    if (items[i].fields.name == itemName) {
      if (getSizeName(items[i].fields.size) == selectedSize) {
        var basePrice = items[i].fields.basePrice;
        totalPrice += parseFloat(basePrice);
        break;
      }
    }
  }

  //calculate addition/extra Price
  var checks = Array.from(document.getElementsByClassName('extraCheckbox'));
  for (i = 0; i<checks.length;i++) {
    if (checks[i].checked == true) {
      totalPrice += parseFloat(checks[i].dataset.price);
    }
  }

  document.getElementById("price").innerHTML = totalPrice.toFixed(2);
  document.getElementById("itemPrice").value = totalPrice;
}

// find itemID
function findItemId() {
  var dropdown = document.getElementById("sizeDropdown");
  var selectedSize = dropdown.options[dropdown.selectedIndex].value;
  for (i=0; i<items.length; i++) {
    if (items[i].fields.name == itemName) {
      if (getSizeName(items[i].fields.size) == selectedSize) {
        var itemID = items[i].pk;
        return itemID;
      }
    }
  }
}
