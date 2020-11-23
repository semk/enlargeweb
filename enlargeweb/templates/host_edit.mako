<%inherit file="base.mako"/>
<%def name="title()">
%if c.srv.id:
  ${c.srv.name} [${c.srv.id}] - ${c.srv.department}
%else:
  Add new server
%endif
</%def>

<%def name="body()">
	<span class="title">
		<h2>${str(c.srv)} Properties</h2>
	</span>
  
  <script type="text/javascript">
  	$(document).ready(function(){
  		$("#dept-text").hide();
  		
	  	$("#switch-dept-text").click(function () {
	  		$("#dept-selection").hide();
	  		$("#dept-text").show();
	  		return true;
	  	});
	  	$("#switch-dept-selection").click(function () {
	  		$("#dept-text").hide();
	  		$("#dept-selection").show();
	  		return true;
	  	});
  	
  	});
  </script>
  
  <form method="post" action="/host/save">
    <table class="details" width="100%" cellspacing="5" cellpadding="2">
      <tr>
	%if c.srv.id:
        <td class="name">ID:</td>
        <td class="value">
        	<input type="text" id="srv_id" name="srv_id" value="${c.srv.id}" disabled="disabled"/>
        	<input type="hidden" id="srv_id" name="srv_id" value="${c.srv.id}" />
        </td>
    %else:
		<td/>
		<td/>
    %endif
        <td class="name">Location:</td>
        <td class="value"><input type="text" name="host_location" value="${c.srv.location}"/></td>
      </tr>

      <tr>
        <td class="name">Name:</td>
        <td class="value"><input type="text" name="host_name" value="${c.srv.name}"/></td>
        <td class="name">Owner:</td>
        %if c.srv.id:
            <td class="value"><input type="text" name="host_owner" value="${c.srv.owner}"/></td>
        %else:
            <td class="value"><input type="text" name="host_owner" value=""/></td>
        %endif
      </tr>
      <tr>
        <td class="name">Type:</td>
        <td class="value">
		  	<select name="host_type">
		      	<option value="PC" selected="selected">PC</option>
		      	<option value="Mac">Mac</option>	      
		  	</select>
		</td>
        <td class="name">Department:</td>
        <td class="value">
        
        <% from enlargeweb.model.srv import Server %>

	    	<div id="dept-selection">
	        	<select name="host_dept">
			     	%for dept in Server.list_departments():
			     		%if c.srv.department == dept[0]:
			      			<option value="${dept[0]}" selected="selected" >${dept[0]}</option>
			      		%else:
			      			<option value="${dept[0]}">${dept[0]}</option>
			      		%endif
			      	%endfor
			  	</select>
			  	<br/>
			  	<a href="#" id="switch-dept-text">+New department</a>
			</div>
			
			<div id="dept-text">
			    %if c.srv.id:
    	        	<input type="text" name="host_new_dept" value=""/>
	        	%else:
    	        	<input type="text" name="host_new_dept" value=""/>	        	
	        	%endif
	        	<br/>
	        	<a href="#" id="switch-dept-selection">+Pick existing</a>
        	</div>
        	
        </td>
      </tr>
    </table>
    
    <div id="comments_area">
     <span class="title">
        <h5>Comments</h5>
     </span>
      <textarea name="host_comments" rows="3">${c.srv.comments}</textarea>
    </div>
    <div style="text-align: right; margin-top: 10px;">
    	%if c.srv.id:
      		<input type="submit" value="Save changes"/>
      	%else:
      		<input type="submit" value="Add server"/>
      	%endif
    </div>
  </form>
  
  %if c.srv.id:
  
  	<span class="title">
		<h5>CPU</h5>
	</span>
 
    <table class="list" width="100%" cellspacing="0" border="0" cellpadding="2">
    	<tr>
    		<th>Model</th>
    		<th>Arch</th>
    		<th>Speed</th>
			<th></th>
    		%if len(c.srv.cpus) > 0:
			<th></th>
			%endif
    	</tr>
    	
    	%for cpu in c.srv.cpus:
    		<tr>
    			<form method="post" action="/host/edit_cpu">
					<input type="hidden" name="srv_id" value="${c.srv.id}" />
					<input type="hidden" name="cpu_id" value="${cpu.id}" />
					<td>
						<input type="text" name="cpu_model" value="${cpu.model}" />
					</td>
					<td>
						<select name="cpu_arch">
							%for arch in ['i386', 'x86_64', 'ia64' ]:
								%if arch == cpu.arch:
									<option value="${arch}" selected="selected">${arch}</option>
								%else:
									<option value="${arch}" >${arch}</option>
								%endif
							%endfor
				  	</select>
					</td>
					<td>
						<input type="text" name="cpu_speed" value="${cpu.speed}" />
					</td>
					<td>
				  		<input type="submit" value="Save"/>
					</td>
				</form>
				<form method="post" action="/host/delete_cpu">
					<td>
						<input type="hidden" name="srv_id" value="${c.srv.id}"/>
						<input type="hidden" name="cpu_id" value="${cpu.id}"/>
				  		<input type="submit" value="Delete"/>
				  	</td>
				</form>
			</tr>
   		%endfor
	   		<form method="post" action="/host/add_cpu">
				<input type="hidden" name="srv_id" value="${c.srv.id}" />
				<td>
					<input type="text" name="cpu_model" />
				</td>
				<td>
					<select name="cpu_arch">
						<option value="">-- select --</option>
					  	<option value="i386">i386</option>
					  	<option value="x86_64">x86_64</option>
					  	<option value="ia64">ia64</option>
				  	</select>
				</td>
				<td>
					<input type="text" name="cpu_speed" />
				</td>
				<td>
			  		<input type="submit" value="Add"/>
				</td>
			</form>
    </table>
  
 <span class="title">
    <h5>Network</h5>
 </span>
 
    <table class="list" width="100%" cellspacing="0" border="0" cellpadding="2">
      <tr>
		<th>Mac</th>
		<th>Ip Address</th>
		<th>Net Mask</th>
		<th>Port</th>
		<th>Main</th>
		<th></th>
		%if len(c.srv.nics) > 0:
		<th></th>
		%endif
      </tr>
      %for n in c.srv.nics:
      <tr>
      <form method="post" action="/host/edit_nic">
      	<input type="hidden" name="srv_id" value="${c.srv.id}" />
			
				<td>
					<input type="hidden" name="nic_mac" value="${n.mac}" /> 
			    	<input type="text" value="${n.mac}" size="17" maxlength="17" disabled="disabled"/>
			  	</td>
				<td>
					<input type="text" name="nic_ip_address" value="${n.ip_address}" size="15" maxlength="15"/>
				</td>
				<td>
					<input type="text" name="nic_ip_mask" value="${n.ip_mask}" size="15" maxlength="15"/>
				</td>
				<td>
					<input type="text" name="nic_ssh_port" value="${n.ssh_port}" size="5" maxlength="5"/>
				</td>
				%if n.main:
			  		<td><input type="checkbox" name="nic_main" checked="checked"/></td>
			  	%else:
			    	<td><input type="checkbox" name="nic_main" /></td>
			  	%endif
				<td>
					<input type="submit" value="Save"/>
				</td>
	   </form>
		<form method="post" action="/host/delete_nic">
			<td>
				<input type="hidden" name="srv_id" value="${c.srv.id}"/>
				<input type="hidden" name="nic_mac" value="${n.mac}"/>
		  		<input type="submit" value="Delete"/>
		  	</td>
    	</form> 
		</tr>
		%endfor
		<form method="post" action="/host/add_nic">
		<input type="hidden" name="srv_id" value="${c.srv.id}" />
			<tr>
			  <td>
			    <input type="text" name="nic_mac" value="" size="17" maxlength="17"/>
			  </td>
			  <td><input type="text" name="nic_ip_address" value="" size="15" maxlength="15"/></td>
			  <td><input type="text" name="nic_ip_mask" value="" size="15" maxlength="15"/></td>
			  <td><input type="text" name="nic_ssh_port" value="22" size="5" maxlength="5"/></td>
			  %if len(c.srv.nics) > 0:
			  	<td><input type="checkbox" name="nic_main"/></td>
			  %else:
			  	<td><input type="checkbox" name="nic_main" checked="checked"/></td>
			  %endif
			  	<td>
			  		<input type="submit" value="Add"/>
			  	</td>
			  %if len(c.srv.nics) > 0:
			  	<td></td>
			  %endif
			</tr>
      </form>
    </table>

 <span class="title">
    <h5>Hard Disk</h5>
 </span>
 
    <table class="list" width="100%" cellspacing="0" border="0" cellpadding="2">
      <tr>
		<th>Device</th>
		<th>Size</th>
		<th></th>
		%if len(c.srv.hdds) > 0:
		<th></th>
		%endif
      </tr>
      %for hdd in c.srv.hdds:
      <tr>
      <form method="post" action="/host/edit_hdd">
      	<input type="hidden" name="srv_id" value="${c.srv.id}" />
			
				<td>
					<input type="hidden" name="hdd_device" value="${hdd.device}" /> 
			    	<input type="text" value="${hdd.device}" size="17" maxlength="17" disabled="disabled"/>
			  	</td>
				<td>
					<input type="text" name="hdd_size" value="${hdd.size}" size="15" maxlength="15"/>
				</td>
				<td>
					<input type="submit" value="Save"/>
				</td>
	   </form>
		<form method="post" action="/host/delete_hdd">
			<td>
				<input type="hidden" name="srv_id" value="${c.srv.id}"/>
				<input type="hidden" name="hdd_device" value="${hdd.device}"/>
		  		<input type="submit" value="Delete"/>
		  	</td>
    	</form> 
		</tr>
		%endfor
		<form method="post" action="/host/add_hdd">
		<input type="hidden" name="srv_id" value="${c.srv.id}" />
			<tr>
			  <td>
			    <input type="text" name="hdd_device" value="" size="17" maxlength="17"/>
			  </td>
			  <td><input type="text" name="hdd_size" value="" size="5" maxlength="5"/></td>
			  	<td>
			  		<input type="submit" value="Add"/>
			  	</td>
			  %if len(c.srv.nics) > 0:
			  	<td></td>
			  %endif
			</tr>
      </form>
    </table>
  
  %endif
  
</%def>
