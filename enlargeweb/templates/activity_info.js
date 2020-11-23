function update() 
{
	$("#page-area").load("/activity/info/${c.activity.id}?partial=1");
}