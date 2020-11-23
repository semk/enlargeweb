<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<title>EnlargeWeb : ${self.title()}</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<link rel="stylesheet" type="text/css" href="/style.css" />
		
		<script src="/jquery.js" type="text/javascript"></script>
		<script src="/jquery.corner.js" type="text/javascript"></script>
		<script type="text/javascript">
			$(document).ready(function(){
				$(".round").corner();
			});
		</script>
		
		%if hasattr(self, 'script'):
			<script type="text/javascript">
				${self.script()}
			</script>
		%endif
		
		<%namespace name="controls" file="controls.mako" import="*"/>
		<link rel="stylesheet" type="text/css" href="/controls.css" />
		
	</head>
  <body>
     <div>
		<ul id="menu">
            <li>
                <a href="/account/logout" title="Log out current user">
                	<% current_user = h.get_current_user() %>
                    ${current_user.first_name} ${current_user.second_name}
                     from <strong>${current_user.department}</strong>
                </a>
            </li>
            
            %if h.is_admin_user():
            <li><a href="/account/list" title="User Accounts configuration">Accounts</a></li>
            <li><a href="/config/dashboard" title="Configuration">Configuration</a></li>
            <li></li>
            %endif
            
	        <li><a href="/host/list" title="Servers">Servers</a></li>
	        <li><a href="/host/my" title="My Servers">My Servers</a></li>
	        <li></li>
	        <li><a href="/appliance/list" title="Appliances">Appliances</a></li>
   	        <li></li>
	        <li><a href="/activity/list" title="Activities">Activities</a></li>
   	        <li><a href="/activity/running" title="Running Activities">Running Activities</a></li>
	        <li><a href="/activity/my" title="My Activities">My Activities</a></li>
        </ul>
     </div>
     
    %if len(c.error) > 0:
    	${controls.error(c.error)}
    %endif
     
     <div class="box w60">
            <div class="box-inner round">
                ${self.body()}
                <div style="text-align: right; vertical-align: bottom;">
                	<a href="http://code.google.com/p/enlargeweb/"> <small>Copyright EnlargeWeb 2009.</small> </a>
                </div>
            </div>
     </div>
  </body>
</html>
