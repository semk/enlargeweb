<%inherit file="base.mako"/>

<%def name="title()">
	Change ${str(c.user)}'s Password
</%def>

<%def name="body()">
	<form name="password_details" action="/account/applypass">
	
		<span class="title">
			<h4>Change ${c.user.first_name}'s Password</h4>
		</span>
	
		<input type="hidden" name="user_id" value="${c.user.id}"/>
		<table width="100%" cellspacing="5" cellpadding="2" border="0">
			<tr>
				<td class="name">Current Password:</td>
				<td class="value">
					<input type="password" name="current_password" value="" autocomplete="off"/>
				</td>
					
				<td class="name">New Password:</td>
				<td class="value">
					<input type="password" name="new_password" value="" autocomplete="off"/>
				</td>
			</tr>
			<tr>
				<td>
				<input type="Submit" value="Save">
				</td>
			</tr>
		</table>
		
	</form>
	
</%def>
