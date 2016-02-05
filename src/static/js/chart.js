queue()
    .defer(d3.json, "/admin/dashboard/ditems")
    .await(makeGraphs);
function makeGraphs(error, ditemsJson){
console.log(ditemsJson);
var ditems = ditemsJson;
var dateFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
ditems.forEach(function(d) {

    var datetemp = new Date(d['_id']['$date'])
    d["date_posted"] = datetemp; //_id is the date_posted from json returned
    d["date_posted"].setDate(1);
    d["total_items"] = +d["count"];
});

//Create a Crossfilter instance
	var ndx = crossfilter(ditems);

//Define Dimensions
	var dateDim = ndx.dimension(function(d) {
	var temp = d['_id']
    var datetemp = new Date(temp['$date'])
	return datetemp;
	});
    var totalItemsDim  = ndx.dimension(function(d) { return d["count"]; });

//Calculate metrics
	var numItemsByDate = dateDim.group();
	var totalItemsByDate = dateDim.group().reduceSum(function(d) {
		return d["count"];
	});

	var all = ndx.groupAll();
	var totalItems = ndx.groupAll().reduceSum(function(d) {return d["count"];});

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["_id"]['$date'];
	var maxDate = dateDim.top(1)[0]["_id"]['$date'];
	//Charts
	var timeChart = dc.barChart("#time-chart");
	var numberItemsND = dc.numberDisplay("#number-items-nd");
	var totalItemsND = dc.numberDisplay("#total-items-nd");

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
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numItemsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Year")
		.yAxis().ticks(4);
        timeChart.xAxis().ticks(5);
		//timeChart.xAxis().ticks(5).tickFormat(function (v) { var monthNameFormat = d3.time.format("%A"); return monthNameFormat(new Date(v));  });


		   dc.renderAll();

};

