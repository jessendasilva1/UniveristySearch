const config = {
	use: {
	   baseURL: 'https://131.104.49.113/api/',
	   headless: true,
	   browserName: 'chromium',
	   ignoreHTTPSErrors: true,
	 },
	 reporter: [
	   ['json', {  outputFile: 'test-results.json' }]
	 ],
   };
   
   module.exports = config;