/**
 * Created by dipanjan on 27/12/15.
 */
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function extractDomain(url) {
    var domain;
    //find & remove protocol (http, ftp, etc.) and get domain
    if (url.indexOf("://") > -1) {
        domain = url.split('/')[2];
    }
    else {
        domain = url.split('/')[0];
    }

    //find & remove port number
    domain = domain.split(':')[0];

    return domain;
}

var positive_coverage_count = 0;
var negative_coverage_count = 0;
var mixed_coverage_count = 0;
var positive_coverage = [];
var negative_coverage = [];
var mixed_coverage = [];

var target = getParameterByName('subject').toLowerCase();
var ajaxUrl = '/data?subject='+target;
$.get(ajaxUrl, function(data, status){
    for(var i = 0; i< data.length; i++)
    {
        var temp = data[i];
        temp.concepts = eval(temp.concepts);
        temp.entities = eval(temp.concepts);
        temp.sentiment = JSON.parse(temp.sentiment);
        data[i] = temp;
    }

    // clean object from here

    for(var i = 0; i< data.length; i++)
    {
        var temp = data[i];
        var domain = extractDomain(temp.url);
        var senti = temp.sentiment;
        if(senti.mixed == 0)
        {
            if(senti.typ == "positive"){

                positive_coverage_count += 1;
                if(domain in positive_coverage)
                {
                    positive_coverage[domain] +=1;
                }
                else {
                    positive_coverage[domain] = 1;
                }
            }
            if(senti.typ == "negative"){
                negative_coverage_count += 1;
                if(domain in negative_coverage)
                {
                    negative_coverage[domain] += 1;
                }
                else {
                    negative_coverage[domain] = 1;
                }
            }
        }
        else {
            mixed_coverage_count += 1;
            if(domain in mixed_coverage)
            {
                mixed_coverage[domain] += 1;
            }
            else{
                mixed_coverage[domain] = 1;
            }
        }

    }

    var total_object = data.length;
    $('#total_occurance').html(data.length);
    // construct presenter object
    var overall_coverage_data = [{
        value: positive_coverage_count,
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Positive Coverage"
    },
    {
        value: negative_coverage_count,
        color:"#F7464A",
        highlight: "#FF5A5E",
        label: "Negative Coverage"
    },
    {
        value: mixed_coverage_count,
        color: "#FDB45C",
        highlight: "#FFC870",
        label: "Mixed Coverage"
    }];
    var ctx = $("#overall-chart").get(0).getContext("2d");
    options = {
    //Boolean - Whether we should show a stroke on each segment
        segmentShowStroke : true,

        //String - The colour of each segment stroke
        segmentStrokeColor : "#fff",

        //Number - The width of each segment stroke
        segmentStrokeWidth : 2,

        //Number - The percentage of the chart that we cut out of the middle
        percentageInnerCutout : 50, // This is 0 for Pie charts

        //Number - Amount of animation steps
        animationSteps : 100,

        //String - Animation easing effect
        animationEasing : "easeOutBounce",

        //Boolean - Whether we animate the rotation of the Doughnut
        animateRotate : true,

        //Boolean - Whether we animate scaling the Doughnut from the centre
        animateScale : false,

        //String - A legend template
        legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"

    };
    $('#overall-waiting').hide();
    var myDoughnutChart_overall = new Chart(ctx).Doughnut(overall_coverage_data,options);
    var positive_coverage_data = [];
    var pos_count = 0;
    for (var key in positive_coverage) {
      var current_color = '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
      if (positive_coverage.hasOwnProperty(key)) {

		var temp = {
			value: positive_coverage[key],
			color: current_color,
			highlight: current_color,
			label: key
		};
          pos_count += positive_coverage[key];
		positive_coverage_data.push(temp);
      }
    }


    var htm2 = Math.floor((pos_count*100)/ total_object).toString()
        + '<sup style="font-size: 20px">%</sup>';
    $('#positive_percentage').html(htm2);
    var ctx1 = $("#positive-chart").get(0).getContext("2d");
    var myDoughnutChart_positive = new Chart(ctx1).Doughnut(positive_coverage_data,options);
    var target = $('#positive_entry_list');
    var temp = '';

    for (var i = 0; i < positive_coverage_data.length; i++){
        temp += '<li></i><a href="#"><span'+
            'class="pull-right text-red"><i class="fa fa-circle-o" style="color:'+
                positive_coverage_data[i].color +
            ';"></i> &nbsp; &nbsp; '+ positive_coverage_data[i].value+
            '</span> &nbsp; &nbsp; &nbsp;'+ positive_coverage_data[i].label +' </a></li>';
    }
    target.html(temp);

    var negative_coverage_data = [];
    var neg_count = 0;
    for (var key in negative_coverage){
		var current_color = '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
		if(negative_coverage.hasOwnProperty(key))
        {
			var temp = {
				value: negative_coverage[key],
				color: current_color,
				highlight: current_color,
				label: key
			};
			negative_coverage_data.push(temp);
            neg_count += negative_coverage[key];
		}
    }
    var temp = '';
    for (var i = 0 ; i < negative_coverage_data.length; i++)
    {
        temp += '<li></i><a href="#"><span'+
            'class="pull-right text-red"><i class="fa fa-circle-o" style="color:'+
                negative_coverage_data[i].color +
            ';"></i> &nbsp; &nbsp; '+ negative_coverage_data[i].value+
            '</span> &nbsp; &nbsp; &nbsp;'+ negative_coverage_data[i].label +' </a></li>';
    }
    var target_negative = $('#negative_entry_list');
    target_negative.html(temp);
    var htm1 = Math.floor((neg_count*100)/ total_object).toString()
        + '<sup style="font-size: 20px">%</sup>';
    $('#negative_percentage').html(htm1);
    var ctx2 = $("#negative-chart").get(0).getContext("2d");
    var myDoughnutChart_negative = new Chart(ctx2).Doughnut(negative_coverage_data, options);

    var mixed_coverage_data = [];
    for (var key in mixed_coverage){
        if(mixed_coverage.hasOwnProperty(key)){
            var current_color = '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
            var temp = {
                value: mixed_coverage[key],
				color: current_color,
				highlight: current_color,
				label: key
            };
            mixed_coverage_data.push(temp);
        }
    }
    var target_mixed = $('#mixed_entry_list');
    var temp = '';
    for (var i = 0; i < mixed_coverage_data.length ; i++){
        temp += '<li></i><a href="#"><span'+
            'class="pull-right text-red"><i class="fa fa-circle-o" style="color:'+
                mixed_coverage_data[i].color +
            ';"></i> &nbsp; &nbsp; '+ mixed_coverage_data[i].value+
            '</span> &nbsp; &nbsp; &nbsp;'+ mixed_coverage_data[i].label +' </a></li>';
    }
    target_mixed.html(temp);

    var ctx3 = $("#mixed-chart").get(0).getContext("2d");
    var myDoughnutChart_mixed = new Chart(ctx3).Doughnut(mixed_coverage_data, options);
});