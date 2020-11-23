<%inherit file="base.mako"/>

<%def name="title()">
${c.srv.name} [${c.srv.id}] - ${c.srv.department}
</%def>

<%def name="script()">
		<%include file="host_info.js" />
</%def>

<%def name="body()">
  <%include file="host_info_ajax.mako" />
</%def>
