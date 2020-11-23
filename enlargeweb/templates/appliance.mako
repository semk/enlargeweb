<%inherit file="base.mako"/>

<%def name="title()">
Deploy appliance ${c.srv.name} [${c.srv.id}] - ${c.srv.department}
</%def>

<%def name="script()">
	<%include file="host_info.js" />
	
	
</%def>

<%def name="body()">
	<a href=""></a>
	<div id="page-area">
		<%include file="host_info_ajax.mako" />
	</div>
	
	<br/>
	<span class="title">
    	<h3>Select appliance to deploy</h3>
    </span>
    
    %if c.appl_plugin_id:
    	<% from enlargeweb.model.appl import Appliance %>
        <h4>
        	<span class="title">
        		Selected type:
        	</span> ${Appliance.get_plugin_for(c.appl_plugin_id)}<br/>
        </h4>
    %endif
    
    <div id="example" />
    
    %if c.conflict:
    	<div id="example" />
    %endif
	
	%if not c.stage:
	
	<form name="appliance_type_selection" action="/operate/appliance/${c.srv.id}/stage_2" method="post" >
		
			<span class="title">
				<h4>Please select type:</h4>
			</span>			
			
			<select name="appl_plugin_id">
				<option value="" selected="True">
					--select type--
				</option>
				%for appl_type in c.appl_types:
					<option value='${appl_type.type_id}'>
						${appl_type.type_name} (${appl_type.class_name})
					</option>
				%endfor
			</select>
			<input type="submit" value="Next >" />
	</form>
	
	%elif c.stage == 'stage_2':
	
	<form name="appliance_selection" action="/operate/appliance/${c.srv.id}/stage_3">
			<span class="title">
				<h4>Please select appliance:</h4>
			</span>	
			
			<input type="hidden" name="appl_plugin_id" value="${c.appl_plugin_id}" />
			<select name="appl_id">
				<option value="" selected="True">
					-- select appliance --
				</option>
				%for appl in c.appliances:
					<option value='${appl.id}'>
						${appl.name} (${appl.arch})
					</option>
				%endfor
			</select>
			<input type="submit" value="Deploy" />
	</form>
	%endif
</%def>
