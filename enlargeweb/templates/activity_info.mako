<%inherit file="base.mako"/>
<%namespace name="controls" file="controls.mako" import="*"/>

<%def name="title()">
${c.activity.description}
</%def>

<%def name="script()">
	<%include file="activity_info.js"/>
</%def>

<%def name="body()">
	<table cellspacing="0" border="0" cellpadding="2" class="actions">
		<tr>
		    <!-- Refresh -->
            <td><a id="refresh" href=""javascript:update()"><img src="/images/refresh.gif" alt="" border="0" /></a></td>
            <td class="text"><a id="update" href=""javascript:update()">Refresh</a></td>
          	%if c.activity.status == 1:
			<!-- Cancel -->
			<td><a href="/activity/cancel/${c.activity.id}"><img src="/images/cancel.gif" alt="" border="0" /></a></td>
			<td class="text"><a href="/activity/cancel/${c.activity.id}">Cancel</a></td>
			<!-- Finish -->
			<td><a href="/activity/finish/${c.activity.id}"><img src="/images/finish.gif" alt="" border="0" /></a></td>
			<td class="text"><a href="/activity/finish/${c.activity.id}">Finish</a></td>
			%endif
		</tr>
	</table>
    <span class="title">
    	<h2>${c.activity.description} details</h2>
    </span>
	<img src="/images/info.png" border="0" />
	<table class="details" width="100%" cellspacing="5" cellpadding="2">
      	<tr>
      		<td class="name">Owner:</td>
      		<td class="value">${c.activity.owner}</td>
	    </tr>
      	<tr>
      		<td class="name">Status</td>
      		<td class="value">
      			${controls.activity_status(c.activity, style="width:30%")}
			</td>
	    </tr>
      	<tr>
      		<td class="name">Master:</td>
      		<td class="value">
      		% if c.activity.servers['master']:
      			<table class="actions" cellspacing="0" border="0" cellpadding="2">
			  		<tr>
						<td>
							<a href="/host/info/${c.activity.servers['master'][0].id}"><img src="/images/computer.png" border="0" /></a>
						</td>
						<td>
							<a href="/host/info/${c.activity.servers['master'][0].id}">${str(c.activity.servers['master'][0])}</a>
						</td>
					</tr>
				</table>
			% else:
				None
			% endif
      		</td>
	    </tr>
	    % if len(c.activity.servers['slaves']) > 0:
      	<tr>
      		<td class="name">Servers:</td>
	  		<td class="value">
	     		<table class="actions" cellspacing="0" border="0" cellpadding="2">
			  		% for s in c.activity.servers['slaves']:
						<tr>
							<td>
								<a href="/host/info/${s.id}"><img src="/images/computer.png" border="0" /></a>
							</td>
							<td>
								<a href="/host/info/${s.id}">${str(s)}</a>
							</td>
						</tr>
					% endfor
				</table>	
	  		</td>
	    </tr>
	    %endif
      	<tr>
      		<td class="name">Description:</td>
      		<td class="value">${c.activity.description}</td>
	    </tr>
      		% if c.activity.parent_id:
		  	<tr>
		  		<td class="name">Parent activity:</td>
		  		<td class="value">
		  			<table class="actions" cellspacing="0" border="0" cellpadding="2">
		  				<tr>
							<td>
								<a href="/activity/details/${c.activity.parent_id}"><img src="/images/info.png" border="0" /></a>
							</td>
							<td>
								<a href="/activity/details/${c.activity.parent_id}">${c.activity.parent_activity.description}</a>
							</td>
						</tr>
		  			</table>
		  		</td>
			</tr>
			% endif
      	<tr>
      		<td class="name">Started at:</td>
      		<td class="value">${c.activity.get_start_time()}</td>
	    </tr>
	    %if c.activity.end_time:
          	<tr>
          		<td class="name">Finished:</td>
          		<td class="value">${c.activity.get_end_time()}</td>
	        </tr>
        %endif
    </table>
	<!-- Children list -->
	
	% if len(c.activity.children)>0:
		<br/>
	    <span class="title">
		    <h3>Children:</h3>
        </span>
        <table class="actions" cellspacing="0" border="0" cellpadding="2">
        	% for child in c.activity.children:
			<tr>
				<td>
					<div style="width:30%">
						<div class="act-status-inner" style="color:${child.get_status_color()};">
							<strong>${child.get_status()}</strong>
						</div>
					</div>
				</td>
				<td>
					<a href="/activity/details/${child.id}">${child.description}</a>
				</td>
			</tr>
			% endfor
		</table>
	% endif
	
	<!-- Log table -->
	<span class="title">
    	<h3>Logs:</h3>
    </span>
	<table class="list" width="100%" cellspacing="0" border="0" cellpadding="5">
		<tr>
			<th>Time</th>
			<th>Message</th>
		</tr>
		<% from enlargeweb.model.act import Activity %>
		%for log in c.activity.logs:
			<tr>
				<td>${Activity.format_datetime(log.timestamp)}</td>
				<td>${log.message}</td>
			</tr>
		%endfor
	</table>
	
</%def>
