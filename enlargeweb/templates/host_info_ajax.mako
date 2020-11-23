<%namespace name="controls" file="controls.mako" import="activity_status, message"/>
	
<div id="#page-area">
	
	<table class="actions" cellspacing="0" border="0" cellpadding="2">
		<tr>
			<!-- Refresh -->
			<td><a id="update" href="javascript:update()"><img src="/images/refresh.gif" alt="" border="0" /></a></td>
			<td class="text"><a id="update" href=""javascript:update()">Refresh</a></td>
%if not c.partial:
			<!-- Edit -->
			<td><a href="/host/edit/${c.srv.id}"><img src="/images/edit.gif" alt="" border="0" /></a></td>
			<td class="text"><a href="/host/edit/${c.srv.id}">Edit</a></td>
			<!-- Delete -->
			<td><a href="/host/delete/${c.srv.id}"><img src="/images/delete.gif" alt="" border="0" /></a></td>
			<td class="text"><a href="/host/delete/${c.srv.id}">Delete</a></td>
			<!-- Appliance -->
			<td><a href="/operate/appliance/${c.srv.id}"><img src="/images/os.gif" alt="" border="0" /></a></td>
			<td class="text"><a href="/operate/appliance/${c.srv.id}">Install Appliance</a></td>
%endif
		</tr>
	</table>

	<span class="title">
		%if c.srv:
			<a href="/host/info/${c.srv.id}">
				<h2>${c.srv.name} Information</h2>
			</a>
		%else:
			<h2>${c.srv.name} Information</h2>
		%endif
	</span>
	${controls.server_status(c.srv.online)}
	<strong>Identity:</strong>${c.srv.name} - (id:${c.srv.id}) 
	<br/>
	<strong>Ownership:</strong>by ${c.srv.owner} from ${c.srv.department}
	<br/>
	<strong>Comments:</strong>
	%if len(c.srv.comments)>0:
		<br/>
		${c.srv.comments}
	%else:
		No Comments
	%endif
	<br/>
	
	<a href="javascript:show_network(true)" id="show-network">&nbsp + Show Network(${len(c.srv.nics)})</a>
	<a href="javascript:show_network(false)" id="hide-network">&nbsp - Hide Network</a>
	<div id="server-network" >
		<span class="title">
			<h3>Network</h3>
		</span>
			
		%if len(c.srv.nics) > 0:
			<table class="list" width="100%" cellspacing="0" border="0" cellpadding="1">
				<tr>
					<th></th>
					<th>Mac</th>
					<th>IP Address</th>
					<th>Net Mask</th>
					<th>SSH Port</th>
				</tr>
				%for n in c.srv.nics:
					%if n.main:
						<tr>
							<td>
								<img src="/images/finish.gif" alt="" border="0" />
							</td>
					%else:
						<tr>
							<td></td>
					%endif
							<td>${n.mac}</td>
							<td>${n.ip_address}</td>
							<td>${n.ip_mask}</td>
							<td>${n.ssh_port}</td>
						</tr>
				%endfor
			</table>
		%else:
			${controls.warning('No Network adapters configured.')}
		%endif
	</div>

	<a href="javascript:show_cpu(true)" id="show-cpu">&nbsp + Show CPU(${len(c.srv.cpus)})</a>
	<a href="javascript:show_cpu(false)" id="hide-cpu">&nbsp - Hide CPU</a>
	<div id="server-cpu" >
		<span class="title">
			<h3>CPU</h3>
		</span>
			
		%if len(c.srv.cpus) > 0:
			<table class="list" width="100%" cellspacing="0" border="0" cellpadding="1">
				<tr>
					<th>Model</th>
					<th>Architecture</th>
					<th>Speed</th>
				</tr>
				%for cpu in c.srv.cpus:
						<tr>
							<td>${cpu.model}</td>
							<td>${cpu.arch}</td>
							<td>${cpu.speed}</td>
						</tr>
				%endfor
			</table>
		%else:
			${controls.warning('No CPUs added.')}
		%endif
	</div>

	<a href="javascript:show_hdd(true)" id="show-hdd">&nbsp + Show Disks(${len(c.srv.hdds)})</a>
	<a href="javascript:show_hdd(false)" id="hide-hdd">&nbsp - Hide Disks</a>
	<div id="server-hdd" >
		<span class="title">
			<h3>Hard Disks</h3>
		</span>
			
		%if len(c.srv.hdds) > 0:
			<table class="list" width="100%" cellspacing="0" border="0" cellpadding="1">
				<tr>
					<th>Device</th>
					<th>Size</th>
				</tr>
				%for hdd in c.srv.hdds:
						<tr>
							<td>${hdd.device}</td>
							<td>${hdd.size}</td>
						</tr>
				%endfor
			</table>
		%else:
			${controls.warning('No Hard Disks added.')}
		%endif
	</div>
	
	<a href="javascript:show_appls(true)" id="show-appls">&nbsp + Show Appliances(${len(c.srv.appliances)})</a>
	<a href="javascript:show_appls(false)" id="hide-appls">&nbsp - Hide Appliances</a>
	<div id="server-appls" >
		<span class="title">
			<h3>Appliances</h3>
		</span>
		%if len(c.srv.appliances) > 0:
			<table class="actions" cellspacing="0" border="0" cellpadding="2">
			%for srv_appl in c.srv.appliances:
				<tr>
					<td>
						<a href="/appliance/info/${srv_appl.appliance_info.id}">
							<img src="${srv_appl.appliance_info.icon}" border="0" />
						</a>
					</td>
					<td>
						<a href="/appliance/info/${srv_appl.appliance_info.id}">
							${str(srv_appl.appliance_info)}
						</a>
					</td>
					<td>
						installed on
					</td>
					<td>
						<a href="/activity/info/${srv_appl.activity_info.id}">
							<img src="/images/info.png" border="0" />
						</a>
					</td>
					<td>
						<a href="/activity/info/${srv_appl.activity_info.id}">
							${srv_appl.activity_info.get_start_time()}
						</a>
					</td>
				</tr>
			%endfor
			</table>
		%else:
			${controls.warning('Noting applied yet.')}
		%endif
	</div>
	
	<a href="javascript:show_activities(true)" id="show-activities">&nbsp + Show Activities(${len(c.running_activities)})</a>
	<a href="javascript:show_activities(false)" id="hide-activities">&nbsp - Hide Activities</a>
	<div id="activities-running" >
		<span class="title">
			<h3>Activities</h3>
		</span>
		%if len(c.running_activities) == 0:
			${controls.message('Server is free.')}
		%else:
			<table class="list" width="100%" cellspacing="0" border="0" cellpadding="1">
				<tr>
					<th>Status</th>
					<th>Activity</th>
					<th>Owner</th>
					<th>Started on</th>
				</tr>
				%for act in c.running_activities:
					<tr>
						<td>
							${controls.activity_status(act)}
						</td>
						<td>
							<a href="/activity/info/${act.id}">${act.description}</a>
						</td>
						<td>
							${act.owner}
						</td>
						<td>
							${act.get_start_time()}
						</td>
					</tr>
				%endfor
			</table>
		%endif
	</div>
	
	<a href="javascript:show_history(true)" id="show-history">&nbsp + Show History(${len(c.history_activities)})</a>
	<a href="javascript:show_history(false)" id="hide-history">&nbsp - Hide History</a>
	<div id="activities-history">
		<span class="title">
			<h3>History</h3>
		</span>
		%if len(c.history_activities) == 0:
			${controls.message('Empty history.')}
		%else:
			<table class="list" width="100%" cellspacing="0" border="0" cellpadding="1">
				<tr>
					<th>Status</th>
					<th>Activity</th>			
					<th>Owner</th>
					<th>Finished on</th>
				</tr>
				%for act in c.history_activities:
					<tr>
						<td>
							${controls.activity_status(act)}
						</td>
						<td>
							<a href="/activity/info/${act.id}">${act.description}</a>
						</td>
						<td>
							${act.owner}
						</td>
						<td>
							${act.get_end_time()}
						</td>
					</tr>
				%endfor
			</table>
		%endif
	</div>
</div>
