function $_GET(q,s) {
    s = (s) ? s : window.location.search;
    var re = new RegExp('&amp;'+q+'=([^&amp;]*)','i');
    return (s=s.replace(/^\?/,'&amp;').match(re)) ?s=s[1] :s='';
}

window.onload
{
	var value = $_GET('query');

	console.log(window.location.href)
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "http://127.0.0.1:8000/?query="+value, false ); // false for synchronous request
    xmlHttp.send( null );

	var container = document.querySelector(".container"); 
	container.innerHTML = "";

/*
	var requestt = xmlHttp.responseText[0];
	console.log(xmlHttp.responseText); 
	console.log(requestt);*/
	var obj = JSON.parse(xmlHttp.responseText);
	console.log(xmlHttp.responseText)
	for (var i = 0; i < 3; i++) 
    {
    container.innerHTML +=  '<div class="wrap"><a href="' + obj.rec[i]['link'] + '"><div class="tile"><h3>' + obj.rec[i]['title'] + '</h3><div class="ellipsis"><div><p>' + obj.rec[i]['text'] + '</p></div></div></div></a><div class="accuracy"><h1>' + obj.rec[i]['accuracy'] + '%</h1></div>';
    }
}


