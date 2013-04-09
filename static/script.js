$(function() {

    Highcharts.setOptions({
        global : {
            useUTC : false
        }
    });

    // Create the chart
    $('#container').highcharts('StockChart', {
        chart : {
            events : {
                load : function() {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function() {
                        //current time
                        $.getJSON("/temp", function(data){
                           // console.log(data);
			    var x = (new Date()).getTime(); 
                            series.addPoint([x, parseFloat(data.tmp)], true, true);
                        });
                    }, 1000);
                }
            }
        },

        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 5,
                type: 'minute',
                text: '5M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 0
        },

        title : {
            text : 'Temperatura'
        },

        exporting: {
            enabled: false
        },

        series : [{
            name : 'Random data',
            data : (function() {
//	return [null];                
// generate an array of random data
                				// generate an array of random data
				var data = [], time = (new Date()).getTime(), i;

				for( i = -99; i <= 0; i++) {
					//data.push([
						//time + i * 1000,
						//Math.round(Math.random() * 100)
					//]);
					data.push(null);
				}
				return data;
            })()
        }]
    });

});

