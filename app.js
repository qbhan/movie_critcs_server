const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const db = require('./queries')
const port = 3000
   

// DB Connect String
// var connection = "postgres://postgres:1234@localhost/week4db";

// Body Parser Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));


app.get('/', function(req, res) {
	console.log('TEST');
	res.json({info: 'Node.js, Express, and Postgres API'})
});


// app.get('/users', db.getUsers)
// app.get('/users/:id', db.getUserById)
// app.post('/users', db.createUser)
// app.put('/users/:id', db.updateUser)
// app.delete('/users/:id', db.deleteUser)
app.get('/current_movie', db.getCurrentMovie)
app.get('/pre_movies', db.getPreMovie)
app.get('/current_movie/:genre', db.getGenreCurrentMovie)


// Server
app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})
