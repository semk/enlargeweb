function update() 
{
	$("#page-area").load("/host/info/${c.srv.id}?partial=1");
}

function show_history(mode)
{
	$("#activities-history").animate({ height: 'show', opacity: 'show' }, 'slow');  
	$("#hide-history").show();
	$("#show-history").show();
	
	if (mode)
	{
		$("#show-history").hide();
	}
	else
	{
		$("#activities-history").animate({ height: 'hide', opacity: 'hide' }, 'slow');  
		$("#hide-history").hide();
	}
}

function show_activities(mode)
{
	$("#activities-running").animate({ height: 'show', opacity: 'show' }, 'slow');  
	$("#show-activities").show();
	$("#hide-activities").show();
	
	if (mode)
	{
		$("#show-activities").hide();
	}
	else
	{
		$("#activities-running").animate({ height: 'hide', opacity: 'hide' }, 'slow');  
		$("#hide-activities").hide();
	}
}

function show_network(mode)
{
	$("#server-network").animate({ height: 'show', opacity: 'show' }, 'slow');  
	$("#show-network").show();
	$("#hide-network").show();
	
	if (mode)
	{
		$("#show-network").hide();
	}
	else
	{
		$("#server-network").animate({ height: 'hide', opacity: 'hide' }, 'slow');  
		$("#hide-network").hide();
	}
}

function show_cpu(mode)
{
	$("#server-cpu").animate({ height: 'show', opacity: 'show' }, 'slow');  
	$("#show-cpu").show();
	$("#hide-cpu").show();
	
	if (mode)
	{
		$("#show-cpu").hide();
	}
	else
	{
		$("#server-cpu").animate({ height: 'hide', opacity: 'hide' }, 'slow');  
		$("#hide-cpu").hide();
	}
}

function show_hdd(mode)
{
	$("#server-hdd").animate({ height: 'show', opacity: 'show' }, 'slow');  
	$("#show-hdd").show();
	$("#hide-hdd").show();
	
	if (mode)
	{
		$("#show-hdd").hide();
	}
	else
	{
		$("#server-hdd").animate({ height: 'hide', opacity: 'hide' }, 'slow');  
		$("#hide-hdd").hide();
	}
}

function show_appls(mode)
{
	$("#server-appls").animate({ height: 'show', opacity: 'show' }, 'slow');  
	$("#show-appls").show();
	$("#hide-appls").show()
	
	if (mode)
	{
		$("#show-appls").hide();
	}
	else
	{
		$("#server-appls").animate({ height: 'hide', opacity: 'hide' }, 'slow');  
		$("#hide-appls").hide();
	}
}
		
$(document).ready(function()
{
	show_history(false)
	
	%if c.partial:
	
	show_activities(false)
	show_appls(false)
	show_network(false)
	show_cpu(false)
	show_hdd(false)
	
	%else:
	
	show_activities(true)
	show_appls(true)
	show_network(true)
	show_cpu(true)
	show_hdd(true)
	
	%endif
});
