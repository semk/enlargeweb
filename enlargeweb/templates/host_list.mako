<%inherit file="base.mako"/>

<%def name="title()">
Hosts list
</%def>

<%def name="body()">
	%if len(c.hosts) > 0 :
	<table cellspacing="0" border="0" cellpadding="2" class="actions">
	    <tr>
	      <!-- Register new server -->
	      <td><a href="/host/add"><img src="/images/add.png" alt="" border="0" /></a></td>
	      <td class="text"><a href="/host/add">Register new server</a></td>
	    </tr>
  	</table>
  	%endif
	<a href=""></a>
	<div id="page-area">
		<%include file="host_list_ajax.mako"/>
	</div>
</%def>
