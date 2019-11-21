// // This code is from w3schools
// function shimSort(table_id, n) {
//   var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
//   table = document.getElementById(table_id);
//   rows = table.rows;
//   var ascending = true,descending=true;
//   for(i=1;i<rows.length -1;i++) {
//     if (rows[i].getElementsByTagName("TD")[n].innerHTML.toLowerCase() > rows[i+1].getElementsByTagName("TD")[n].innerHTML.toLowerCase()) {
//       ascending = false;
//       break;
//     }
//   }
//   if (ascending == true) {
//     mergeSort(table_id,n,1,rows.length,function(a,b) {
//       a.innerHTML.toLowerCase() > b.innerHTML.toLowerCase();
//     });
//   } else {
//     mergeSort(table_id,n,1,rows.length,function(a,b) {
//       a.innerHTML.toLowerCase < b.innerHTML.toLowerCase();
//     });
//   }
//   // console.log(flag);
//   // switching = true;
//   // Set the sort
// }
// function merge(table_id,n,start,last,fn) {
  
// }
// function mergeSort(table_id,n,start,last,fn) {
//   var table,rows;
//   table = document.getElementById(table_id);
//   rows = table.rows;
//   // for(var sz=2;sz < rows.length;sz = sz*2) {
//   //   for(var i = 1;)
//   // }
//   console.log("SUCCESS");
// }
// function sortTable(table_id, n, reverse=1) {
//   var col = n;
//   var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
//   table = document.getElementById(table_id);
//   rows = table.rows;
//   var ascending = true,descending=true;
//   for(i=1;i<rows.length -1;i++) {
//     if (rows[i].getElementsByTagName("TD")[n].innerHTML.toLowerCase() > rows[i+1].getElementsByTagName("TD")[n].innerHTML.toLowerCase()) {
//       ascending = false;
//       break;
//     }
//   }
//   if (ascending == true) reverse = -1;
//   var tb = document.getElementById(table_id), // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
//       tr = Array.prototype.slice.call(tb.rows, 1), // put rows into array
//       i;
  
//   // reverse = -((+reverse) || -1);
//   tr = tr.sort(function (a, b) { // sort rows
//       return reverse // `-1 *` if want opposite order
//           * (a.cells[col].textContent.trim() // using `.textContent.trim()` for test
//               .localeCompare(b.cells[col].textContent.trim())
//              );
//   });
//   for(i = 0; i < tr.length; ++i) tb.appendChild(tr[i]); // append each row in order
// }
// function sortTable2(table_id, n) {
//   console.log(shimSort(table_id,n));
//   var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
//   table = document.getElementById(table_id);
//   switching = true;
//   // Set the sorting direction to ascending:
//   dir = "asc";
//   /* Make a loop that will continue until
//   no switching has been done: */
//   while (switching) {
//     // Start by saying: no switching is done:
//     switching = false;
//     rows = table.rows;
//     /* Loop through all table rows (except the
//     first, which contains table headers): */
//     for (i = 1; i < (rows.length - 1); i++) {
//       // Start by saying there should be no switching:
//       shouldSwitch = false;
//       /* Get the two elements you want to compare,
//       one from current row and one from the next: */
//       x = rows[i].getElementsByTagName("TD")[n];
//       y = rows[i + 1].getElementsByTagName("TD")[n];

//       // To prevent integers being compared as string 
//       var int = Number;
//       if (isNaN(x.innerHTML.toLowerCase())) int = function (x) { return x; }
      
//       /* Check if the two rows should switch place,
//       based on the direction, asc or desc: */
//       //   console.log("Dsadfaskdlfjaslkdf\n");
//       if (dir == "asc") {
//         // console.log(int(x.innerHTML.toLowerCase()));
//         if (int(x.innerHTML.toLowerCase()) > int(y.innerHTML.toLowerCase())) {
//           // If so, mark as a switch and break the loop:
//           shouldSwitch = true;
//           break;

//         }
//       } else if (dir == "desc") {
//         if (int(x.innerHTML.toLowerCase()) < int(y.innerHTML.toLowerCase())) {
//           // If so, mark as a switch and break the loop:
//           shouldSwitch = true;
//           break;
//         }
//       }
//     }
//     if (shouldSwitch) {
//       /* If a switch has been marked, make the switch
//       and mark that a switch has been done: */
//       rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
//       switching = true;
//       // Each time a switch is done, increase this count by 1:
//       switchcount++;
//     } else {
//       /* If no switching has been done AND the direction is "asc",
//       set the direction to "desc" and run the while loop again. */
//       if (switchcount == 0 && dir == "asc") {
//         dir = "desc";
//         switching = true;
//       }
//     }
//   }
// }

// https://insights.stackoverflow.com/survey/2018/#technology-most-loved-dreaded-and-wanted-semesters
const sample = [
    {
      semester: '1st',
      value: 6.57,
      color: '#000000'
    },
    {
      semester: '2nd',
      value: 6.47,
      color: '#00a2ee'
    },
    {
      semester: '3rd',
      value: 8.23,
      color: '#fbcb39'
    },
    {
      semester: '4th',
      value: 9.14,
      color: '#ff6e52'
    },
    {
      semester: '5th',
      value: 10,
      color: '#f9de3f'
    },
  ];

  const svg = d3.select('svg');
  const svgContainer = d3.select('#container');
  
  const margin = 100;
  const width = 700 - 2 * margin;
  const height = 500 - 2 * margin;

  const chart = svg.append('g')
    .attr('transform', `translate(${margin}, ${margin})`);

  const xScale = d3.scaleBand()
    .range([0, width])
    .domain(sample.map((s) => s.semester))
    .padding(0.3)
  
  const yScale = d3.scaleLinear()
    .range([height, 0])
    .domain([0, 10]);

  // vertical grid lines
  // const makeXLines = () => d3.axisBottom()
  //   .scale(xScale)

  const makeYLines = () => d3.axisLeft()
    .scale(yScale)

  chart.append('g')
    .attr('transform', `translate(0, ${height})`)
    .call(d3.axisBottom(xScale));

  chart.append('g')
    .call(d3.axisLeft(yScale));

  // vertical grid lines
  // chart.append('g')
  //   .attr('class', 'grid')
  //   .attr('transform', `translate(0, ${height})`)
  //   .call(makeXLines()
  //     .tickSize(-height, 0, 0)
  //     .tickFormat('')
  //   )

  chart.append('g')
    .attr('class', 'grid')
    .call(makeYLines()
      .tickSize(-width, 0, 0)
      .tickFormat('')
    )

  const barGroups = chart.selectAll()
    .data(sample)
    .enter()
    .append('g')

  barGroups
    .append('rect')
    .attr('class', 'bar')
    .attr('x', (g) => xScale(g.semester))
    .attr('y', (g) => yScale(g.value))
    .attr('height', (g) => height - yScale(g.value))
    .attr('width', xScale.bandwidth())
    .on('mouseenter', function (actual, i) {
      d3.selectAll('.value')
        .attr('opacity', 0)

      d3.select(this)
        .transition()
        .duration(300)
        .attr('opacity', 0.6)
        .attr('x', (a) => xScale(a.semester) - 5)
        .attr('width', xScale.bandwidth() + 10)

      const y = yScale(actual.value)

      line = chart.append('line')
        .attr('id', 'limit')
        .attr('x1', 0)
        .attr('y1', y)
        .attr('x2', width)
        .attr('y2', y)

      barGroups.append('text')
        .attr('class', 'divergence')
        .attr('x', (a) => xScale(a.semester) + xScale.bandwidth() / 2)
        .attr('y', (a) => yScale(a.value) + 30)
        .attr('fill', 'white')
        .attr('text-anchor', 'middle')
        .text((a, idx) => {
          const divergence = (a.value - actual.value).toFixed(1)
          
          let text = ''
          if (divergence > 0) text += '+'
          text += `${divergence}%`

          return idx !== i ? text : '';
        })

    })
    .on('mouseleave', function () {
      d3.selectAll('.value')
        .attr('opacity', 1)

      d3.select(this)
        .transition()
        .duration(300)
        .attr('opacity', 1)
        .attr('x', (a) => xScale(a.semester))
        .attr('width', xScale.bandwidth())

      chart.selectAll('#limit').remove()
      chart.selectAll('.divergence').remove()
    })

  barGroups 
    .append('text')
    .attr('class', 'value')
    .attr('x', (a) => xScale(a.semester) + xScale.bandwidth() / 2)
    .attr('y', (a) => yScale(a.value) + 30)
    .attr('text-anchor', 'middle')
    .text((a) => `${a.value}%`)
  
  svg
    .append('text')
    .attr('class', 'label')
    .attr('x', -(height / 2) - margin)
    .attr('y', margin / 2.4)
    .attr('transform', 'rotate(-90)')
    .attr('text-anchor', 'middle')
    .text('Progress (%)')

  svg.append('text')
    .attr('class', 'label')
    .attr('x', width / 2 + margin)
    .attr('y', height + margin * 1.7)
    .attr('text-anchor', 'middle')
    .text('Semesters')

    cury = new Date()
    cuy = cury.getFullYear()
  svg.append('text')
    .attr('class', 'title')
    .attr('x', width / 2 + margin)
    .attr('y', 40)
    .attr('text-anchor', 'middle')
    .text(`your progress Report Until ${cuy}`)

  svg.append('text')
    .attr('class', 'source')
    .attr('x', width - margin / 2)
    .attr('y', height + margin * 1.7)
    .attr('text-anchor', 'start')
    // .text('Source: Stack Overflow, 2018')
