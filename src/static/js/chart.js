queue()
    .defer(d3.json, "/admin/dashboard/ditems")
    .await(makeGraphs);

var items_json_modified;

function makeGraphs(error, ditemsJson){
    var ditems = ditemsJson;
    var dateFormat = d3.time.format("%Y-%m-%d %H:%M:%S");

    //Get items returned- number of days where posting happened
    //var x = crossfilter(ditems);
    //var n = x.groupAll().reduceCount().value();
    //console.log("There are " + n + " days returned.");


    ditems.forEach(function(d) {

        d["date_posted"] = new Date(d['_id']['$date']); //_id is the date_posted from json returned
        d["total_items"] = +d["count"];



    });

    items_json_modified = ditems;

    //Create a Crossfilter instance
        var ndx = crossfilter(ditems);
        //var facts = crossfilter(ditems); //same as above different naming.

    //Define Dimensions
        var dateDim = ndx.dimension(function(d) {return new Date(d['_id']['$date']);	});
        var totalItemsDim  = ndx.dimension(function(d) { return d["count"]; });

        var volumeByHour = ndx.dimension(function(d) {
          var day_temp = new Date(d['_id']['$date']);
          return day_temp.getDate();
            });

    //Calculate metrics
        var entriesInGroup = dateDim.group();

    //	tolEntries = entriesInGroup.size()
    //	console.log("total entries "+tolEntries+" Numer of items by date dateDim.group() " + entriesInGroup.top(tolEntries)[0].value)


        var sumOfEntries = dateDim.group().reduceSum(function(d) {
            return d["count"];
        });
        //console.log("Sum of items by date total.group() " + sumOfEntries.top(4)[0].value)

         var volumeByHourGroup = volumeByHour.group().reduceCount(function(d) {
         var day_temp = new Date(d['_id']['$date']);
         return day_temp; });


        var all = ndx.groupAll();
        var totalItems = ndx.groupAll().reduceSum(function(d) {return d["count"];});
        //console.log ("Sum of items count " + totalItems.value)

        //Define values (to be used in charts)
        var minDate = dateDim.bottom(1)[0]["_id"]['$date'];
        var maxDate = dateDim.top(1)[0]["_id"]['$date'];
        //Charts
        var timeChart = dc.barChart("#time-chart");
        var numberItemsND = dc.numberDisplay("#number-items-nd");
        var totalItemsND = dc.numberDisplay("#total-items-nd");
        var timeChart2 = dc.lineChart("#dc-time-chart");

        numberItemsND
            .formatNumber(d3.format("d"))
            .valueAccessor(function(d){return d; })
            .group(all);

        totalItemsND
            .formatNumber(d3.format("d"))
            .valueAccessor(function(d){return d; })
            .group(totalItems)
            .formatNumber(d3.format(".3s"));

        timeChart
            .width(500)
            .height(200)
            .margins({top: 10, right: 50, bottom: 30, left: 50})
            .dimension(dateDim)
            .group(sumOfEntries)
            .transitionDuration(500)
            .x(d3.time.scale().domain([minDate, maxDate]))
            .elasticY(true)
            .xAxisLabel("Period")
            .yAxis().ticks(4);
            timeChart.xAxis().ticks(6);
            //timeChart.xAxis().ticks(5).tickFormat(function (v) { var monthNameFormat = d3.time.format("%A"); return monthNameFormat(new Date(v));  });

         // time graph
              timeChart2.width(960)
                .height(150)
                .margins({top: 10, right: 10, bottom: 20, left: 40})
                .dimension(volumeByHour)
                .group(sumOfEntries)
                .transitionDuration(500)
                .elasticY(true)
                .x(d3.time.scale().domain([minDate, maxDate]))
                .xAxis();


               dc.renderAll();

};




    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 30, bottom: 30, left: 50},
        width = 490 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;



    // Set the ranges
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
                                .orient("bottom").ticks(5);
    var yAxis = d3.svg.axis().scale(y)
                                .orient("left").ticks(5);

    // Define the line
    var valueline = d3.svg.line()
                                .interpolate("basis")
                                .x(function(d) { return x(d.date); })
                                .y(function(d) { return y(d.count); });
     var valueline2 = d3.svg.line()
                                    .interpolate("basis")
                                    .x(function(d) { return x(d["date_posted"]); })
                                    .y(function(d) { return y(d["total_items"]); });
    // Adds the svg canvas
    var svg = d3.select("#dc-user-chart")
                                .append("svg")
                                .attr("width", width + margin.left + margin.right)
                                .attr("height", height + margin.top + margin.bottom)
                                .append("g")
                                .attr("transform",
                                "translate(" + margin.left + "," + margin.top + ")");

    // Get the data
    d3.json("/admin/dashboard/dusers", function(error, data) {
    data.forEach(function(d) {
    d.date =  new Date(d['_id']['$date']); //parseDate(d.date);
    d.count = +d.count; //change to integer
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return new Date(d['_id']['$date']); }));
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    // Add the valueline path.
    svg.append("path")
                    .attr("class", "line")
                    .attr("d", valueline(data));

    // Add the X Axis
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

    // Add the Y Axis
    svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

    //add y label
	svg.append("text")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("x",margin.top - (height / 2))
	.attr("dy", "1em")
	.style("text-anchor", "middle")
	.text("Users");

	//add headline
	svg.append("text")
    .attr("x", (width / 2))
    .attr("y", 0 - (margin.top / 2))
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text("User Signups vs Date Graph");

    });



//users Items


    // Adds the svg canvas
    var usersItemsSVG = d3.select("#dc-user-items-chart")
                                .append("svg")
                                .attr("width", width + margin.left + margin.right)
                                .attr("height", height + margin.top + margin.bottom)
                                .append("g")
                                .attr("transform",
                                "translate(" + margin.left + "," + margin.top + ")");

     var valueline2 = d3.svg.line()
                                        .interpolate("basis")
                                        .x(function(d) { return x(d["date_posted"]); })
                                        .y(function(d) { return y(d["total_items"]); });

    // Get the data
    d3.json("/admin/dashboard/dusers", function(error, data) {
    data.forEach(function(d) {
    d.date =  new Date(d['_id']['$date']); //parseDate(d.date);
    d.count = +d.count; //change to integer
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return new Date(d['_id']['$date']); }));
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    // Add the valueline path.
    usersItemsSVG.append("path")
                    .attr("class", "line")
                    .attr("d", valueline(data));

    usersItemsSVG.append("path")
                    .style("stroke", "green")
                    .attr("class", "line")
                    .attr("d", valueline2(items_json_modified));

    // Add the X Axis
    usersItemsSVG.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);



    // Add the Y Axis
    usersItemsSVG.append("g")
    .attr("class", "y axis")
    .call(yAxis);

    //add y label
	usersItemsSVG.append("text")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("x",margin.top - (height / 2))
	.attr("dy", "1em")
	.style("text-anchor", "middle")
	.text("Users | items");

	usersItemsSVG.append("text")
    .attr("x", (width / 2))
    .attr("y", 0 - (margin.top / 2))
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("text-decoration", "underline")
    .text("Users to Items posted Graph");
    console.log(data[data.length-1])

    usersItemsSVG.append("text")
		.attr("transform", "translate(" + (width-10) + "," + (6) + ")") //x,y
		.attr("dy", ".35em")
		.attr("text-anchor", "start")
		.style("fill", "steelblue")
		.text("Users");

    usersItemsSVG.append("text")
		.attr("transform", "translate(" + (width-10) + "," + (20) + ")")
		.attr("dy", ".35em")
		.attr("text-anchor", "start")
		.style("fill", "green")
		.text("Items");

    //display fots on users graph
    usersItemsSVG.selectAll("dot")
        .data(data)
        .enter().append("circle")
        .attr("r", 3.5)
        .attr("cx", function(d) { return x(new Date(d['_id']['$date'])); })
        .attr("cy", function(d) { return y(d.count); });

    //display dots on items graph
    usersItemsSVG.selectAll("dot")
        .data(items_json_modified)
        .enter().append("circle")
        .attr("r", 3.5)
        .attr("cx", function(d) { return x(new Date(d['date_posted'])); })
        .attr("cy", function(d) { return y(d['total_items']); });




    });