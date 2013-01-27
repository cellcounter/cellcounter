$(document).ready(function() {

       $('.modaldialog').click(function() {
			
                        var $link = $(this);
                        alert("foo");
                        var $dialog = $('<div></div>')
			.load($link.attr('href'))
			.dialog({
				autoOpen: false,
				title: $link.attr('title'),
				width: 840,
				height: 600
			});
                        $dialog.dialog('open');
			return false;
		});
});
