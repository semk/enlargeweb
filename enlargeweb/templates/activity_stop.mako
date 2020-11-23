<%inherit file="base.mako"/>

<%def name="title()">
${c.action.capitalize()} ${c.activity.description}
</%def>

<%def name="body()">
    %if len(c.error)>0:
    <snap style="color:red;">${c.error}</span>
    %endif
	<form name="stop_activity" action="/activity/${c.action}/${c.activity.id}" >
		<input type="hidden" name="action" value="" />
		You are going to ${c.action} ${c.activity.description} activity with id ${c.activity.id} so please specify a reason.
        <br/>
  		<textarea name="message" rows="3" >No Reason</textarea>
        <br/>
		<input type="submit" value="${c.action.capitalize()} activity" />
	</form>
</%def>
