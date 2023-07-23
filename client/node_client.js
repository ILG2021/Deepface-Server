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
					imgData
				]
			}),
			"headers": {
				"content-type": "application/json"
			}
		}
	);
	const data = await response.json();
	console.log(JSON.stringify(data, null, 2));
}

await testDF()

async function yolo() {
    var url = "https://ultralytics.com/images/zidane.jpg"
    var type = 'jpg'
    var imgData = await fetch(url).then(r => r.buffer()).then(buf => `data:image/${type};base64,`+buf.toString('base64'));

    var response = await fetch('http://127.0.0.1:1234/persons',
        {method: 'POST', body: JSON.stringify({
            "img": [
              url
            ]
          }),
          "headers": {
            "content-type": "application/json"
           }
        }
    );
    var data = await response.json();

    console.log("persons:" , data);

    var response = await fetch('http://127.0.0.1:1234/objects',
        {method: 'POST', body: JSON.stringify({
            "img": [
              url
            ]
          }),
          "headers": {
            "content-type": "application/json"
           }
        }
    );
    var data = await response.json();

    console.log("objects:" , data);
}

await yolo()