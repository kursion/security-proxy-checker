// Inject this code on http://nntime.com/proxy-updated-01.htm
// To get the txt list of proxy
var jq = document.createElement('script');
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);

var parser = function(){
  jQuery.noConflict();
  $ = jQuery;
  IPs = "";
  TRs = $("#proxylist > tbody").find("tr").each( function(el, i){
    var text = $(this).find("td:nth-child(2)").text()
    jsHackAddr = text.indexOf("document");
    addr = text.slice(0, jsHackAddr)
    jsHackPort = text.indexOf("):");
    port = text.slice(jsHackPort+2);
    IPs = IPs+addr+":"+port+"\n";
  });
  console.log(IPs);
}
setTimeout(parser, 1000);
