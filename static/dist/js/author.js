function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
var target = getParameterByName('subject').toLowerCase();
var channel = getParameterByName('author');
var ajaxUrl = '/author_data?subject='+target+'&author='+channel;
$.get(ajaxUrl, function(data, status){
    for(var i = 0; i< data.length; i++)
    {
        var temp = data[i];
        temp.concepts = eval(temp.concepts);
        temp.entities = eval(temp.concepts);
        temp.sentiment = JSON.parse(temp.sentiment);
        data[i] = temp;
    }
    var target = $('#content-body');
    var htm = '';
    for(var i = 0 ; i< data.length; i++)
    {
        var target_class = 'alert-';
        if(data[i].sentiment.mixed == 1)
        {
            target_class += 'warning'
        }
        else {
            if (data[i].sentiment.typ == "positive") {
                target_class += 'success';
            }
            else if (data[i].sentiment.typ == "negative") {
                target_class += 'danger';
            }
            else {
                target_class += 'info';
            }
        }
        htm += '<div style="text-decoration:none!important;" class="alert '+ target_class+' alert-dismissable">'+
                    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                    '<a target="_blank" href="'+ data[i].url + '"> <h4><i class="icon fa fa-info"></i>'+ data[i].title +' </h4> </a>'+
                    data[i].author+
                  '</div>';
    }
    $('#content-body').html(htm);
});