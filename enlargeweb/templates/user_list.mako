<%inherit file="base.mako"/>

<%def name="title()">
Users
</%def>

<%def name="body()">
	<a href=""></a>
	<div id="page-area">
		<%include file="user_list_ajax.mako"/>
	</div>
</%def>