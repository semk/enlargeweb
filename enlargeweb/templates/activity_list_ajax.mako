	%if len(c.activities) > 0:
	<%namespace name="controls" file="controls.mako" import="*"/>
	<div class="pager">${c.activities.pager("Page $page of $page_count - ~5~", onclick="$('#page-area').load('%s'); return false;")}</div>
	<table class="list" width="100%" cellspacing="0" border="0" cellpadding="5">
		<tr>
			<th></th>
			<th>Status</th>
			<th>Description</th>
			<th>Start time</th>
		%if not c.list_origin == 'running':
			<th>End time</th>
		%endif
			<th>Owner</th>
		</tr>
		% for act in c.activities:
			<tr>
				<td><a href='/activity/info/${act.id}'>Details</a></td>
				<td>
				    <div>
            			<div class="act-status-inner round" style="color:orange;">
        					${controls.activity_status(act)}
        		        </div>
            		</div>
				</td>
				<td>${act.description}</td>
				<td>${act.get_start_time()}</td>
			%if not c.list_origin == 'running':
				<td>${act.get_end_time()}</td>
			%endif
				<td>${act.owner}</td>
			</tr>
		% endfor
	</table>
	
	%else:
		${controls.message('No known activity.')}
	%endif
    <script type="text/javascript">
        $(".round").corner();
    </script>
