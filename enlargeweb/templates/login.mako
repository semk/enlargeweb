<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<title>Login</title>
		<link rel="stylesheet" type="text/css" href="/style.css" />
		
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<script src="/jquery.js" type="text/javascript"></script>
		<script src="/jquery.corner.js" type="text/javascript"></script>
		<script type="text/javascript">
			$(document).ready(function(){
				$(".round").corner();
			});
		</script>
		
		<%namespace name="controls" file="controls.mako" import="*"/>
		<link rel="stylesheet" type="text/css" href="/controls.css" />
	</head>
  <body>
	<div class="box w60">
		<div class="box-inner round">
			<center>
				<p>
					Welcome to EnlargeWeb Management Console
				</p>
				<form name="login_form" action="/account/submit">
					<table cellspacing="15" cellpadding="2">
					  <tr>
						<td>Username:</td>
						<td>
							<input name="login" type="text" />
						</td>
					  </tr>
					  <tr>
						<td>Password:</td>
						<td>
							<input name="password" type="password" />
						</td>
					  </tr>
					</table>
					
					%if len(c.error) > 0:
						${controls.error(c.error)}
					%endif
					
					<input type="submit" value="Log in" />
				</form>
			</center>
		</div>
	</div>
  </body>
</html>
