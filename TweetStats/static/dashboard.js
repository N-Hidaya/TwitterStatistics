
//Function to draw twitter barchart
function drawChart(bottom, leftside) {
    const years = bottom
    const data = {
        labels: years,
        datasets: [{
            label: '# of Twitter Messages Per Year',
            data: leftside,
            backgroundColor: 'rgb(175, 134, 45)',
            borderColor: 'rgb(175, 134, 45)',
            borderWidth: 1
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    var twitterChart = new Chart (
        document.getElementById('twitterChart'),
        config
    );
    return twitterChart
    

} //end of function



$.ajax({
    url: "/dashboard",
    method: "POST",
    data: {fromYear: 2013, toYear: 2021},
    error: function() {
        alert("Error");
    },
    success: function(data, status, xhr) {
        var months = [];
        for (var label of data.months){
            months.push(label);
        }

        var tweets = [];
        for (var info of data.tweets){
            tweets.push(info);
        }

        
        drawChart(months, tweets);
    }
});
