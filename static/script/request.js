//////////////////////////////////////////////////////
//Getting the right host adress depending 
//on were the page was loaded
//////////////////////////////////////////////////////

//////////////////////////////////////////////////////
function getHost()
{
	var host = window.location.host;
	return host
}

//////////////////////////////////////////////////////
function getServer()
{
	result = "http://"+getHost()+"";
	return result;
}

//////////////////////////////////////////////////////
function getCallType()
{
	if(location.host==getHost())
		return "json";
	else 
		return "jsonp";
}

//////////////////////////////////////////////////////
function postEvent(event, callback, url)
{
	$.ajax({
			type: 'POST',
			data: JSON.stringify(event),
			url: url,
			contentType: 'application/json; charset=utf-8',
			dataType: getCallType(),
			complete: callback
	});
}

//////////////////////////////////////////////////////
function handleKeyUp(event, index, task_id)
{
	if (event.keyCode==13)
	{
		var inp = $("#qa_"+index);
		var txt = inp[0].value;

		var result =
		{
			response:txt,
			index:index,
			task_id:task_id
		};

		postEvent(result, scoring, getServer()+"/response");

		var n = "";
		n+='<div id=qa_'+index+' class="response white">'+txt+'</div>';
		$("#qa_"+index).replaceWith(n);
	}

}

//////////////////////////////////////////////////////
function scoring(event)
{
	hit = $.parseJSON(event.responseText)

	var n = ""
	n+='<div id=qa_'+hit.index+' class="response white">'+hit.response+'</div>'
	n+= hit.feedback
	$("#qa_"+hit.index).replaceWith(n);

	if (hit.finished)
	{
		n = '<div id="content">'
		n += '<div class="payment">Thank you for solving this task. Use this reply code:<em>'+hit.reply+'</em> on the CrowdFlower website to collect your payment.</div>'
		n += '</div>'
		$("#content").replaceWith(n);
	}
}
