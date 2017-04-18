/*
jonathanperron.fr Webserver - Avril 2017
*/

// Import part
var fs = require('fs');
var express = require('express');
var hogan = require('hogan-express');

// Express
const app = express()
app.engine('html', hogan)
app.set('views', __dirname + '/views')
app.use('/static', express.static(__dirname + '/public'))
app.set('port', (process.env.PORT || 8081))

app.get('/cv',(req, res) => {
	var file = './public/PERRON_CV.pdf';
	fs.readFile(file, function(error,data){
		res.contentType("application/pdf");
		res.status(200).send(data);
	})

})

app.get('*',(req, res) => {
	res.status(200).render('index.html');
})

app.listen(app.get('port'))