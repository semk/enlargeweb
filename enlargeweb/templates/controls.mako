<%def name="activity_status(act, style = '')">
	%if style:
		<div style="${style}">
   	%else:
      	<div>
	%endif
			<div class="act-status-inner round" style="color:${act.get_status_color()};">
				<strong>${act.get_status()}</strong>
			</div>
		</div>
</%def>

<%def name="message(text, style = '', img = '/images/message.png')">
	<div class="msg-border" style="width: 60%; margin: 0 auto;">
		<div class="msg-inner round" >
			<div style="${style}">
				<img src="${img}" border="0" /> ${text}
			</div>
		</div>
	 </div>
</%def>

<%def name="error(text, style = '')">
	${self.message(text, style = 'color:Red; font-weight:bold;', img = '/images/error.png')}
</%def>

<%def name="warning(text, style = '')">
	${self.message(text, style = 'color:Orange; font-weight:bold;', img = '/images/warning.png')}
</%def>

<%def name="server_status(status)">
	<table class="actions" cellspacing="0" border="0" cellpadding="2">
		%if status:
		<tr>
			<td>
				<img src="/images/online.png" border="0">
			</td>
			<td>
				Online
			</td>
		</tr>
		%else:
		<tr>
			<td>
				<img src="/images/offline.png" border="0">
			</td>
			<td>
				Offline
			</td>
		</tr>
		%endif
	</table>
</%def>
