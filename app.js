const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const db = require('./queries')
const port = 3000

const cors = require('cors');
   

// CORS Policy
app.use(cors())


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
app.get('/movie/:movie_id', db.getMovie)
app.get('/pre_movie', db.getPreMovie)
app.get('/current_movie/:genre', db.getGenreCurrentMovie)
app.get('/movie_order_score', db.getMovieOrderNaverScore)
app.get('/movie_critic_naver/:movie_id', db.getMovieCriticNaver)
app.get('/movie_critic_meta/:movie_id', db.getMovieCriticMeta)
app.get('/movie_critic_tomato/:movie_id', db.getMovieCriticTomato)

// Server
app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})
