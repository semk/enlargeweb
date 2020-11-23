<%inherit file="base.mako"/>

<%def name="title()">
%if c.appl.id: 
	Edit ${str(c.appl)}
%else:
	${str(c.appl)}
%endif
</%def>

<%def name="body()">
	%if not c.stage:
	%if c.appl.id:
	<form name="appliance_details" action="/appliance/edit/${c.appl.id}/stage_2">
	%else:
	<form name="appliance_details" action="/appliance/edit/0/stage_2">
	%endif
	
		<span class="title">
			<h4>${str(c.appl)} General information</h4>
		</span>
	
		<input type="hidden" name="appl_id" value="${c.appl.id}"/>
		<table width="100%" cellspacing="5" cellpadding="2" border="0">
			<tr>
				<td class="name">Plugin:</td>
				<td class="value">
				%if c.appl.id:
					${c.appl.get_plugin()}
					<input type="hidden" name="appl_plugin_id" value="${c.appl.plugin_id}" />
				%else:
					<select name="appl_plugin_id">
					%for p_info in c.plugins:
						<option value="${p_info.type_id}" > ${p_info.type_name} </option>
					%endfor
					</select>
				%endif
				</td>
					
				<td class="name">Name:</td>
				<td class="value">
					<input type="text" name="appl_name" value="${c.appl.name}" />
				</td>
			</tr>
			<tr>
				<td class="name">Archtiecture:</td>
				<td class="value">
					<select name="appl_arch">
					%for arch in ['i386', 'x86_64', 'ia64']:
						%if c.appl.arch == arch:
							<option value="${arch}" selected="selected"> ${arch} </option>
						%else:
							<option value="${arch}"> ${arch} </option>
						%endif
					%endfor				
					</select>
				</td>
			</tr>
		</table>
		<h4>Comments:</h4>
			<div id="comments_area">
				<textarea name="appl_description" rows="3" >${c.appl.description}</textarea>
			</div>
		<input type="submit" value="Properties >" />
	</form>
	
	%elif c.stage == 'stage_2':
	
	<script type="text/javascript">
  	$(document).ready(function(){
  		var select_depend = $("#depend_item0").clone()
  		$("#remove-last-one").hide()
  		
	  	$("#add-another-one").click(function () {
	  		items_count = $(".depend_list").children('div').length
	  		
	  		if (items_count >= 10)
	  		{
	  			alert('Cannot have more than 10 dependences.')
	  			return
	  		}
	  		
	  		if (items_count >= 1)
	  			$("#remove-last-one").show()
	  		else
		  		$("#remove-last-one").hide()
	  		
	  		cloned = select_depend.clone()
	  		cloned.attr('id', 'depend_item' + items_count)
	  		cloned.children('select').attr('name', 'depend' + items_count)
	  		cloned.appendTo($(".depend_list"))
	  		return true;
	  	});
	  
	  $("#remove-last-one").click(function() {
	  		items_count = $(".depend_list").children('div').length
	  		$("#depend_item" + (items_count-1)).remove()
	  		
	  		if (items_count-2 >= 1)
	  			$("#remove-last-one").show()
	  		else
		  		$("#remove-last-one").hide()
	  });
  	});
  </script>
	
	<form name="appliance_options" action="/appliance/save" >
		<input type="hidden" name="appl_id" value="${c.appl_id}" />
		<input type="hidden" name="appl_plugin_id" value="${c.appl_plugin_id}" />
		<input type="hidden" name="appl_name" value="${c.appl_name}" />
		<input type="hidden" name="appl_arch" value="${c.appl_arch}" />
		<input type="hidden" name="appl_description" value="${c.appl_description}" />

		<span class="title">
			<h4>${str(c.appl)} Dependences</h4>
		</span>
		
		Select required appliance from list:
		<div class="depend_list">
			<div id="depend_item0">
				<select name="depend0">
					<option value="">-- select --</option>
				%for appl in c.appls:
					%if appl.id != c.appl_id:
					<option value="${appl.id}"> ${appl.name} </option>
					%endif
				%endfor
				</select>
			</div>
		</div>
		<br/>
		<a href="#" id="add-another-one">&nbsp;+ Add another one</a>
		<a href="#" id="remove-last-one">&nbsp;- Remove last one</a>
		<br/>
		
		<span class="title">
			<h4>${str(c.appl)} Properties</h4>
		</span>
		
		<table width="100%" cellspacing="0" border="0" cellpadding="5">
		%for opt in c.options:				
			<tr>
				<td>${opt.opt_desc}</td>
				<td>
				%if opt.opt_type == 'text':
					%if c.appl.id:
						<input type="text" name="${opt.opt_name}" value="${c.appl.get_prop(opt.opt_name)}" /input>
					%elif opt.variants:
						<input type="text" name="${opt.opt_name}" value="${opt.variants}"/>
					%else:
						<input type="text" name="${opt.opt_name}" value=""/>
					%endif
				%elif opt.opt_type == 'enum':
					<select name="${opt.opt_name}">
						<option value="">-- please select --</option>
						%for v in opt.variants:
							%if c.appl.id and c.appl.get_prop(opt.opt_name) == v:
								<option value="${v}" selected="selected" >${v}</option>
							%else:
								<option value="${v}">${v}</option>
							%endif
						%endfor
					</select>
				%endif
				</td>
			</tr>
		%endfor
		</table>
		<input type="submit" value="Save" />
	</form>
	
	%endif
</%def>
