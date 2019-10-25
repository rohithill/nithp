// This code is from w3schools
function shimSort(table_id, n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(table_id);
  rows = table.rows;
  var ascending = true,descending=true;
  for(i=1;i<rows.length -1;i++) {
    if (rows[i].getElementsByTagName("TD")[n].innerHTML.toLowerCase() > rows[i+1].getElementsByTagName("TD")[n].innerHTML.toLowerCase()) {
      ascending = false;
      break;
    }
  }
  if (ascending == true) {
    mergeSort(table_id,n,1,rows.length,function(a,b) {
      a.innerHTML.toLowerCase() > b.innerHTML.toLowerCase();
    });
  } else {
    mergeSort(table_id,n,1,rows.length,function(a,b) {
      a.innerHTML.toLowerCase < b.innerHTML.toLowerCase();
    });
  }
  // console.log(flag);
  // switching = true;
  // Set the sort
}
function merge(table_id,n,start,last,fn) {
  
}
function mergeSort(table_id,n,start,last,fn) {
  var table,rows;
  table = document.getElementById(table_id);
  rows = table.rows;
  // for(var sz=2;sz < rows.length;sz = sz*2) {
  //   for(var i = 1;)
  // }
  console.log("SUCCESS");
}
function sortTable(table_id, n, reverse=1) {
  var col = n;
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(table_id);
  rows = table.rows;
  var ascending = true,descending=true;
  for(i=1;i<rows.length -1;i++) {
    if (rows[i].getElementsByTagName("TD")[n].innerHTML.toLowerCase() > rows[i+1].getElementsByTagName("TD")[n].innerHTML.toLowerCase()) {
      ascending = false;
      break;
    }
  }
  if (ascending == true) reverse = -1;
  var tb = document.getElementById(table_id), // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
      tr = Array.prototype.slice.call(tb.rows, 1), // put rows into array
      i;
  
  // reverse = -((+reverse) || -1);
  tr = tr.sort(function (a, b) { // sort rows
      return reverse // `-1 *` if want opposite order
          * (a.cells[col].textContent.trim() // using `.textContent.trim()` for test
              .localeCompare(b.cells[col].textContent.trim())
             );
  });
  for(i = 0; i < tr.length; ++i) tb.appendChild(tr[i]); // append each row in order
}
function sortTable2(table_id, n) {
  console.log(shimSort(table_id,n));
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(table_id);
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];

      // To prevent integers being compared as string 
      var int = Number;
      if (isNaN(x.innerHTML.toLowerCase())) int = function (x) { return x; }
      
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      //   console.log("Dsadfaskdlfjaslkdf\n");
      if (dir == "asc") {
        // console.log(int(x.innerHTML.toLowerCase()));
        if (int(x.innerHTML.toLowerCase()) > int(y.innerHTML.toLowerCase())) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;

        }
      } else if (dir == "desc") {
        if (int(x.innerHTML.toLowerCase()) < int(y.innerHTML.toLowerCase())) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}