document.addEventListener('DOMContentLoaded', () => {

  //when user clicks order now, open up order form
  Array.from(document.getElementsByClassName('displayButton')).forEach(button => {
    button.onclick = () => {

      //clear topping dropdown rows
      var orderSection = document.getElementById("orderSection");
      while (orderSection.firstChild) {
        orderSection.removeChild(orderSection.firstChild);
      }

      //determine selected order status
      var dropdown = document.getElementById("chooseStatus");
      var selectedStatus = dropdown.options[dropdown.selectedIndex].value;

      //add order details and options for each order
      var dropdown = document.getElementById("sizeDropdown");
      for (i=0; i<orders.length; i++) {
        if (orders[i].fields.status == selectedStatus) {
          //create container
          var orderRow = document.createElement('div');
          orderRow.classList.add('row');
          orderRow.classList.add('justify-content-center');
          orderSection.appendChild(orderRow);

          var container = document.createElement('div');
          container.classList.add('col-md-4');
          container.classList.add('my-2');
          container.classList.add('mx-1');
          container.classList.add('border');
          container.classList.add('border-success');
          container.classList.add('rounded');
          container.classList.add('justify-content-center');
          orderRow.appendChild(container);

          var buttonContainer = document.createElement('div');
          buttonContainer.classList.add('col-md-2');
          buttonContainer.classList.add('my-2');
          buttonContainer.classList.add('mx-1');
          buttonContainer.classList.add('justify-content-center');
          orderRow.appendChild(buttonContainer);

          //delete button
          var deleteRow = document.createElement('div');
          deleteRow.classList.add('row');
          deleteRow.classList.add('my-1');
          buttonContainer.appendChild(deleteRow);

          var deleteButton = document.createElement('div');
          deleteButton.classList.add('btn');
          deleteButton.classList.add('btn-danger');
          deleteButton.classList.add('submitButton');
          deleteButton.dataset.action = "delete";
          deleteButton.dataset.ordernum = orders[i].pk;
          deleteButton.innerHTML = "Delete";
          deleteRow.appendChild(deleteButton);

          //view button
          var viewRow = document.createElement('div');
          viewRow.classList.add('row');
          viewRow.classList.add('my-1');
          buttonContainer.appendChild(viewRow);

          var viewOrder = document.createElement('div');
          viewOrder.classList.add('btn');
          viewOrder.classList.add('btn-primary');
          viewOrder.classList.add('submitButton');
          viewOrder.dataset.action = "view";
          viewOrder.dataset.ordernum = orders[i].pk;
          viewOrder.innerHTML = "View";
          viewRow.appendChild(viewOrder);

          if (selectedStatus != "Complete") {
            //complete button
            var completeRow = document.createElement('div');
            completeRow.classList.add('row');
            completeRow.classList.add('my-1');
            buttonContainer.appendChild(completeRow);

            var markComplete = document.createElement('div');
            markComplete.classList.add('btn');
            markComplete.classList.add('btn-success');
            markComplete.classList.add('submitButton');
            markComplete.dataset.action = "complete";
            markComplete.dataset.ordernum = orders[i].pk;
            markComplete.innerHTML = "Mark Complete";
            completeRow.appendChild(markComplete);
          }

          //add customer row
          var row3 = document.createElement('div');
          row3.classList.add('row');
          row3.classList.add('mx-1');
          var b3 = document.createElement("B");
          b3.innerHTML = 'Customer:' + String.fromCharCode(160);
          var customer = document.createTextNode(getEmail(orders[i].fields.user));
          row3.appendChild(b3);
          row3.appendChild(customer);
          container.appendChild(row3);

          //add timestamp row
          var row = document.createElement('div');
          row.classList.add('row');
          row.classList.add('mx-1');
          var b = document.createElement("B");
          b.innerHTML = 'Ordered:' + String.fromCharCode(160);
          var t = new Date(orders[i].fields.timestamp);
          var time = document.createTextNode(t);
          //getMonth(t) + ' ' + getDate(t) + ', ' + getFullYear(t) + ' ' + getHours(t) + ":" + getMinutes(t)
          row.appendChild(b);
          row.appendChild(time);
          container.appendChild(row);

          //add price row
          var row1 = document.createElement('div');
          row1.classList.add('row');
          row1.classList.add('mx-1');
          var b1 = document.createElement("B");
          b1.innerHTML = 'Price:' + String.fromCharCode(160);
          var price = document.createTextNode('$' + orders[i].fields.totalPrice);
          row1.appendChild(b1);
          row1.appendChild(price);
          container.appendChild(row1);

          //add status row
          var row2 = document.createElement('div');
          row2.classList.add('row');
          row2.classList.add('mx-1');
          var b2 = document.createElement("B");
          b2.innerHTML = 'Status:' + String.fromCharCode(160);
          var status = document.createTextNode(orders[i].fields.status);
          row2.appendChild(b2);
          row2.appendChild(status);
          container.appendChild(row2);
        }
      }

      Array.from(document.getElementsByClassName('submitButton')).forEach(button => {
        button.onclick = () => {
          document.getElementById('actionInput').value = button.dataset.action;
          document.getElementById('ordernumInput').value = button.dataset.ordernum;
          document.getElementById('orderForm').submit();
        }
      });

    }
  });
});

function getEmail(pk) {
  for(j=0; j<users.length; j++) {
    if (pk == users[j].pk) {
      return users[j].fields.email;
    }
  }
}
