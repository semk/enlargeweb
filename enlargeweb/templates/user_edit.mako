<%inherit file="base.mako"/>

<%def name="title()">
%if c.user.id: 
	Edit ${str(c.user)}
%else:
	Add new Account
%endif
</%def>

<%def name="body()">
	%if c.user.id:
	<form name="account_details" action="/account/save">
	%else:
	<form name="account_details" action="/account/save">
	%endif
	
		<span class="title">
			%if c.user.id:
			<h4>Edit ${c.user.first_name} account</h4>
			%else:
			<h4>Provide Account Information</h4>
			%endif
		</span>
	
		<input type="hidden" name="user_id" value="${c.user.id}"/>
		<table width="100%" cellspacing="5" cellpadding="2" border="0">
			<tr>
				<td class="name">Login:</td>
				<td class="value">
					%if c.user.id:
					${c.user.login}
					<input type="hidden" name="account_name" value="${c.user.login}" />
					%else:
					<input type="text" name="account_name" value=""/>
					%endif
				</td>
				
				%if not c.user.id:	
				<td class="name">Password:</td>
				<td class="value">
					%if c.user_id:
					<input type="password" name="account_pwd" value="" autocomplete="off"/>
					%else:
					<input type="password" name="account_pwd" value="" autocomplete="off"/>
					%endif
				</td>
				%endif
			</tr>
			<tr>
				<td class="name">First Name:</td>
				<td class="value">
					<input type="text" name="first_name" value="${c.user.first_name}" />
				</td>
				<td class="name">Second Name:</td>
				<td class="value">
					<input type="text" name="second_name" value="${c.user.second_name}" />
				</td>
			</tr>
			<tr>
				<td class="name">Department:</td>
				<td class="value">
					<input type="text" name="department" value="${c.user.department}" />
				</td>
				<td class="name">Rights:</td>
				<td class="value">
					<select name="rights">
						%for r in ['admin', 'user']:
							%if c.user.id:
							%if c.user.get_attr('rights').value == r:
								<option value="${r}" selected="selected"> ${r} </option>
							%else:
								<option value="${r}"> ${r} </option>
							%endif
							%else:
								<option value="${r}"> ${r} </option>
							%endif
						%endfor
					</select>
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
