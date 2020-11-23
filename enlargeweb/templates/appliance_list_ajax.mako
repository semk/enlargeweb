	%if len(c.appliances) >0:
		<table class="actions" cellspacing="0" border="0" cellpadding="2">
		    <tr>
		      <!-- Register new appliance -->
		      <td><a href="/appliance/add"><img src="/images/edit.gif" alt="" border="0" /></a></td>
		      <td class="text"><a href="/appliance/add">Register new appliance</a></td>
		    </tr>
		  </table>
		<p class="pager">${c.appliances.pager("Page $page of $page_count - ~5~", onclick="$('#page-area').load('%s'); return false;")}</p>
		<table class="list" width="100%" cellspacing="0" border="0" cellpadding="5">
			<tr>
				<th></th>
				<th>Appliance</th>
				<th>Description</th>
				<th>Plugin</th>
			</tr>
			% for appl in c.appliances:
				<tr>
					<td><img src="${appl.icon}" border="0" /></td>
					<td><a href='/appliance/info/${appl.id}'>${appl.name} (${appl.arch})</a></td>
					<td>${appl.description}</td>
					<td>${appl.get_plugin()}</td>
				</tr>
			% endfor
		</table>
	%else:
		<div id="message" text-align: center; vertical-align: middle;">
		    <br/>
			<p>
				<a style="color: orange;" href="/appliance/add"><h2>No Appliances registered yet. Add one?</h2></a>
			</p>
		    <br/>
		</div>
	%endif
