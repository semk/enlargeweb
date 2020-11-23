<%inherit file="base.mako"/>
<%namespace name="controls" file="controls.mako" import="*"/>

<%def name="title()">
${str(c.appl.name)}
</%def>

<%def name="body()">
  <table cellspacing="0" border="0" cellpadding="2" class="actions">
    <tr>
      <!-- Edit -->
      <td><a href="/appliance/edit/${c.appl.id}"><img src="/images/edit.gif" alt="" border="0" /></a></td>
      <td class="text"><a href="/appliance/edit/${c.appl.id}">Edit</a></td>
      <!-- Delete -->
      <td><a href="/appliance/delete/${c.appl.id}"><img src="/images/delete.gif" alt="" border="0" /></a></td>
      <td class="text"><a href="/appliance/delete/${c.appl.id}">Delete</a></td>
    </tr>
  </table>

  <span class="title">
      <h2>${str(c.appl.name)} Details</h2>
  </span>
  <img src="${c.appl.icon}" border="0" />
  <table class="details" width="100%" cellspacing="5" cellpadding="2">
    <tr>
    	<td class="name">Plugin:</td>
    	<td class="value">
			${c.appl.get_plugin()}
    	</td>
    </tr>
    <tr>
    	<td class="name">Architecture:</td>
    	<td class="value">${c.appl.arch}</td>
    </tr>
    <tr>
	    <td class="name">Name:</td>
	    <td class="value">${c.appl.name}</td>
	</tr>
    <tr>
	    <td class="name">Comments:</td>
      	<td class="value">${c.appl.description}</td>
    </tr>
  </table>
  
  <span class="title">
      <h2>${str(c.appl.name)} Properties</h2>
  </span>
    
  <table class="details" width="100%" cellspacing="5" cellpadding="2">
	%for prop in c.appl.properties:
    <tr>
    	<td class="name">${prop.prop_name}:</td>
    	<td class="value">${prop.value}</td>
    </tr>
    %endfor
  </table>
  
  <span class="title">
      <h3>Dependences</h3>
  </span>
  %if len(c.appl.depends_on) > 0:
	  <table class="actions" cellspacing="0" border="0" cellpadding="2">
	  	%for appl in c.appl.depends_on:
		    <tr>
		    	<td>
		    		<a href="/appliance/info/${appl.id}"><img src="${appl.icon}" border="0" /></a>
		    	</td>
		    	<td>
		    		<a href="/appliance/info/${appl.id}">${appl.name}</a>
		    	</td>
		    </tr>
	    %endfor
	</table>
  %else:
  	${controls.message('No dependences.')}
  %endif
  
  <span class="title">
      <h3>Deployed on</h3>
  </span>
  %if len(c.hosts) > 0:
	  <table class="actions" cellspacing="0" border="0" cellpadding="2">
	  	%for srv in c.hosts:
		    <tr>
		    	<td>
		    		<a href="/host/info/${srv.id}"><img src="/images/computer.png" border="0" /></a>
		    	</td>
		    	<td>
		    		<a href="/host/info/${srv.id}">${srv.name} - ${srv.department}</a>
		    	</td>
		    </tr>
	    %endfor
	</table>
  %else:
  	${controls.message('Not deployed anywhere yet.')}
  %endif
</%def>
