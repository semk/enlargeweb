<%inherit file="base.mako"/>
<%namespace name="controls" file="controls.mako" import="*"/>

<%def name="title()">
${str(c.user.first_name)}
</%def>

<%def name="body()">
  <table cellspacing="0" border="0" cellpadding="2" class="actions">
    <tr>
      <!-- Edit -->
      <td><a href="/account/edit/${c.user.id}"><img src="/images/edit.gif" alt="" border="0" /></a></td>
      <td class="text"><a href="/account/edit/${c.user.id}">Edit</a></td>
      <!-- Delete -->
      <td><a href="/account/delete/${c.user.id}"><img src="/images/delete.gif" alt="" border="0" /></a></td>
      <td class="text"><a href="/account/delete/${c.user.id}">Delete</a></td>
      <!-- Change Password -->
      <td><a href="/account/changepass/${c.user.id}"><img src="/images/refresh.gif" alt="" border="0" /></a></td>
      <td class="text"><a href="/account/changepass/${c.user.id}">Change Password</a></td>
    </tr>
  </table>

  <span class="title">
      <h2>${str(c.user.first_name)}'s Details</h2>
  </span>
  <table class="details" width="100%" cellspacing="5" cellpadding="2">
    <tr>
    	<td class="name">Login:</td>
    	<td class="value">
			${c.user.login}
    	</td>
    </tr>
    <tr>
    	<td class="name">First Name:</td>
    	<td class="value">${c.user.first_name}</td>
    </tr>
    <tr>
	    <td class="name">Second Name:</td>
	    <td class="value">${c.user.second_name}</td>
	</tr>
    <tr>
	    <td class="name">Department:</td>
      	<td class="value">${c.user.department}</td>
    </tr>
  </table>
  
  <span class="title">
      <h2>${str(c.user.first_name)}'s Attributes</h2>
  </span>
    
  <table class="details" width="100%" cellspacing="5" cellpadding="2">
	%for attr in c.user.attributes:
    <tr>
		%if attr.name == "rights":
    	<td class="name">Rights:</td>
    	<td class="value">${attr.value}</td>
		%elif attr.name == "k7_id":
		<td class="name">Platform Support:</td>
    	<td class="value">Enabled</td>
		%endif
    </tr>
    %endfor
  </table>
</%def>
