var serverhost = 'http://127.0.0.1:8000';

async function getCurrentTab() {
	let queryOptions = { active: true, currentWindow: true };
	let [tab] = await chrome.tabs.query(queryOptions);
	return tab;
  }

	chrome.runtime.onMessage.addListener(
		function(request, sender, sendResponse) {
		  
			  
			var url = serverhost + '/summarization/' ;
			
			console.log(url);
			let tab_url; 
			chrome.tabs.query({ active: true, lastFocusedWindow: true }, function (tabs) {
				// console.log("Tabs")
				// console.log(tabs[0].url);
				tab_url = tabs[0].url;
				//console.log(tab_url);
				sendRequest(tab_url)
			})
			function sendRequest(tab_url){
				console.log("Hello " + tab_url)
				const data = { "page_url" : tab_url };
				fetch(url,{
					method: 'POST',
					headers: {
					  'Content-Type': 'application/json',
					},
					body: JSON.stringify(data),
				} )
				.then(response => response.json())
				.then(response => sendResponse({farewell: response}))
				.catch(error => console.log(error))
			}
			//console.log(window.location.href)
			

			

						//var url = "http://127.0.0.1:8000/wiki/get_wiki_summary/?topic=%22COVID19%22"	
			
				
			return true;  // Will respond asynchronously.
		  
	});

	