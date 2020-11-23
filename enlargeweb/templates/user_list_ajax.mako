	%if len(c.users) >0:
		<%namespace name="controls" file="controls.mako" import="*"/>
		<table class="actions" cellspacing="0" border="0" cellpadding="2">
		    <tr>
		      <!-- add new user -->
		      <td><a href="/appliance/add"><img src="/images/edit.gif" alt="" border="0" /></a></td>
		      <td class="text"><a href="/account/add">Add user</a></td>
		    </tr>
		  </table>
		<p class="pager">${c.users.pager("Page $page of $page_count - ~5~", onclick="$('#page-area').load('%s'); return false;")}</p>
		<table class="list" width="100%" cellspacing="0" border="0" cellpadding="5">
			<tr>
				<th></th>
				<th>Login</th>
				<th>User</th>
				<th>Department</th>
				<th>Rights</th>
			</tr>
			% for user in c.users:
				<tr>
					<td><img src="/images/user.png" border="0" /></td>
					<td><a href='/account/info/${user.id}'>${user.login}</a></td>
					<td>${user.first_name} ${user.second_name}</td>
					<td>${user.department}</td>
					<td>${user.get_attr('rights').value}</td>
				</tr>
			% endfor
		</table>
	%else:
		${controls.error('No users registered but you are looking at this page?!')}
	%endif
