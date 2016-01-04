/**
 * Created by dipanjan on 3/1/16.
 */
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
var targetLink = '/keywords?subject='+getParameterByName('subject');
$('#entity-link').attr("href", targetLink);
var senti_link = '/?subject='+getParameterByName('subject');
$('#sentiment-link').attr('href', senti_link);
var raw_link = '/raw_data?subject='+getParameterByName('subject');
$('#raw-link').attr('href', raw_link);
$('.m-info-box').attr('href', raw_link);
var csv_link = '/download?subject='+getParameterByName('subject');
$('#csv-link').attr('href', csv_link);