const Pool = require('pg').Pool
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'week4db',
  password: '1234',
  port: 5432,
})

// 현재 상영중인 영화 
const getCurrentMovie = (req, res) => {
  pool.query("SELECT * FROM movies WHERE status = '0' ORDER BY movie_id ASC", (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
} 

// 영화 하나 정보
const getMovie = (req, res) => {
  const movie_id = String(req.params.movie_id)
  pool.query("SELECT * FROM movies WHERE movie_id = $1 ORDER BY movie_id ASC", [movie_id], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}


// 상영예정인 영화
const getPreMovie = (req, res) => {
  pool.query("SELECT * FROM movies WHERE status = '1' ORDER BY movie_id ASC", (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}


// 특정 장르인 현재개봉영화
const getGenreCurrentMovie = (req, res) => {
  const genre = String(req.params.genre)
  pool.query("SELECT * FROM movies WHERE status = '0' AND movies.genres ~ $1 ORDER BY movie_id ASC", [genre], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

//네이버 평점 순서
const getMovieOrderNaverScore = (req, res) => {
  pool.query("SELECT * FROM movies WHERE naver_score IS NOT NULL ORDER BY naver_score DESC", (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

//해당 영화 네이버 평론 가져오기
const getMovieCriticNaver = (req, res) => {
  const movie_id = String(req.params.movie_id)
  pool.query("SELECT * FROM movies_critics WHERE movie_id = $1", [movie_id], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

const getMovieCriticMeta = (req, res) => {
  const movie_id = String(req.params.movie_id)
  pool.query("SELECT * FROM movies_meta WHERE movie_id = $1", [movie_id], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

const getMovieCriticTomato = (req, res) => {
  const movie_id = String(req.params.movie_id)
  pool.query("SELECT * FROM movies_tomato WHERE movie_id = $1", [movie_id], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}


// //POST a new user
// const createUser = (req, res) => {
//   const { name, phone_number } = req.body

//   pool.query('INSERT INTO contacts (contact_name, phone_number) VALUES ($1, $2)', 
//   	[name, phone_number], (error, results) => {
//     if (error) {
//       throw error
//     }
//     res.status(201).send(`User added with ID: ${results.insertId}`)
//   })
// }

// // POST existing user
// const loginUser = (req, res) => {
// 	const { name, }

// 	pool.query('SELECT password FROM users WHERE ')
// }


// //PUT updated data in an existing user

// const updateUser = (req, res) => {
//   const id = parseInt(req.params.id)
//   const { name, phone_number } = req.body

//   pool.query(
//     'UPDATE contacts SET contact_name = $1, phone_number = $2 WHERE id = $3',
//     [name, phone_number, id],
//     (error, results) => {
//       if (error) {
//         throw error
//       }
//       res.status(200).send(`User modified with ID: ${id}`)
//     }
//   )
// }

// //DELETE a user
// const deleteUser = (req, res) => {
//   const id = parseInt(req.params.id)

//   pool.query('DELETE FROM contacts WHERE id = $1', [id], (error, results) => {
//     if (error) {
//       throw error
//     }
//     res.status(200).send(`User deleted with ID: ${id}`)
//   })
// }

module.exports = {
  getCurrentMovie,
  getMovie,
  getPreMovie,
  getGenreCurrentMovie,
  getMovieOrderNaverScore,
  getMovieCriticNaver,
  getMovieCriticMeta, 
  getMovieCriticTomato,
}
//////////////////////////////////////////////////////////////////////////