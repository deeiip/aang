
var target = getParameterByName('subject').toLowerCase();
var channel = getParameterByName('channel').toLowerCase();
var ajaxUrl = '/data?subject='+target+'&channel='+channel;
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
    var temp = '';
    for(var i = 0 ; i< data.length; i++)
    {
        temp += '<div class="alert alert-info alert-dismissable">'+
                    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
                    '<h4><i class="icon fa fa-info"></i> Alert!</h4>'+
                    'Info alert preview. This alert is dismissable.'+
                  '</div>';
    }
    target.html(temp);
}