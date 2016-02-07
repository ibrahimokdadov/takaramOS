queue()
    .defer(d3.json, "/admin/dashboard/ditems")
    .await(makeGraphs);
function makeGraphs(error, ditemsJson){
console.log(ditemsJson);
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

