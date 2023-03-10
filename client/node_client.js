import fetch from "node-fetch";

async function testDF() {
	var url = "https://ultralytics.com/images/zidane.jpg"
	var type = 'jpg'
	var imgData = await fetch(url).then(r => r.buffer()).then(buf => `data:image/${type};base64,` + buf.toString('base64'));

	const response = await fetch('http://127.0.0.1:1234/analyze',
		{
			method: 'POST', body: JSON.stringify({
				"actions": [
					"race"
				],
				"img": [
					imgData,
					imgData
				]
			}),
			"headers": {
				"content-type": "application/json"
			}
		}
	);
	const data = await response.json();

	console.log(data);
}

await testDF()