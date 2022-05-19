$(function(){

    // var url = getCurrentTab();
	// console.log(url);
    $('#keywordsubmit').click(function(){
                chrome.runtime.sendMessage(
					'get_summarised_reviews',
					function(response) {
						result = response.farewell;
						$('#positive_reviews').text(result.positive_review[0]);
						$('#negative_reviews').text(result.negative_review[0]);
						console.log(result)
						console.log(result.review[0])
						var notifOptions = {
                        type: "basic",
                        iconUrl: "icon48.png",
                        title: "WikiPedia Summary For Your Result",
                        message: result
						};
						
						chrome.notifications.create('WikiNotif', notifOptions);
						
					});
			
		$('#keyword').val('');
		
    });
});