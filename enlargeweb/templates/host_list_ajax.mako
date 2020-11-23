	<%  from enlargeweb.model.srv import Server  %>
	
	%if len(c.hosts) > 0:
		<p class="pager">${c.hosts.pager("Page $page of $page_count - ~5~", onclick="$('#page-area').load('%s'); return false;")}</p>
		<div class="filter">
		    <nobr>
			    %if len(c.filter_dept)>0:
			        Filter:
    			    <a href="/host/list">&nbsp;All&nbsp;</a>
				    <input type="hidden" name="filter_dept" value="${c.filter_dept}" />
			    %else:
       		        Filter:
    			    <a href="/host/list">&nbsp;<strong>All</strong>&nbsp;</a>
    			%endif
    			
			    %for dept in Server.list_departments():
				    %if dept[0] != c.filter_dept:
					    <a href="/host/list?filter_dept=${dept[0]}">&nbsp;${dept[0]}&nbsp;</a>
				    %else:
					    <a href="/host/list?filter_dept=${dept[0]}">&nbsp;<strong>${dept[0]}</strong>&nbsp;</a>				
				    %endif
			    %endfor
		    </nobr>
		</div>
		<table class="list" width="100%" cellspacing="0" border="0" cellpadding="5">
			<tr>
				<th/>
				<th>Name</th>
				<th>OS</th>
				<th>Network</th>
				<th>Architecture</th>
				<th>Activity</th>
				<th>Ownership</th>
				<th>Location</th>
			</tr>
			% for srv in c.hosts:
				<tr>
					<td><a href='/host/info/${srv.id}'><img src="/images/computer.png" alt="" border="0" /></a></td>
					<td><a href='/host/info/${srv.id}'>${srv.name}</a></td>
					<td>
						${srv.get_os()}
					</td>
					<td>${srv.get_main_nic_text()}</td>
					<td>${srv.get_type()} ${srv.get_arch()}</td>				
					%if len(srv.get_activities()[0])>0:
						<td> ${str(srv.get_activities()[0][0])} ${srv.get_activities()[0][0].get_start_time()} </td>
					%else:
						<td>Free</td>
					%endif
					<td>${srv.owner}, ${srv.department}</td>
					<td>${srv.location}</td>
				</tr>
			% endfor
		</table>
	%else:
		<div id="message" text-align: center; vertical-align: middle;">
			<p>
				<a style="color: orange;" href="/host/add"><h2>No Servers registered yet. Add one?</h2></a>
			</p>
		</div>
	%endif
