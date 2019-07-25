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
const getGenreMovie = (req, res) => {
  const genre = String(req.params.genre)
  pool.query("SELECT * FROM movies WHERE movies.genres ~ $1 ORDER BY movie_id ASC", [genre], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

const getGenresMovie = (req, res) => {
  const genre1 = String(req.params.genre1)
  const genre2 = String(req.params.genre2)
  pool.query("SELECT * FROM movies WHERE genres ~ $1 OR genres ~ $2 ORDER BY movie_id ASC", [genre1, genre2], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

const getMovieTitle = (req, res) => {
  const title = String(req.params.title)
  pool.query("SELECT * FROM movies WHERE title ~ $1 ORDER BY movie_id ASC", [title], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

const getMovieDirector = (req, res) => {
  const director = String(req.params.director)
  pool.query("SELECT * FROM movies WHERE directors ~ $1 ORDER BY movie_id ASC", [director], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

const getMovieCast = (req, res) => {
  const cast = String(req.params.cast)
  pool.query("SELECT * FROM movies WHERE casts ~ $1 ORDER BY movie_id ASC", [cast], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

//네이버 평점 순서
const getMovieOrderScore = (req, res) => {
  pool.query("SELECT * FROM movies WHERE (naver_score >= 7.5 and metascore >= 80) or (naver_score >= 7.5 and rottentomato >= 80) or (metascore >= 80 and rottentomato >= 80) ORDER BY naver_score DESC", (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

//해당 영화 네이버 기자 평론 가져오기
const getMovieReportNaver = (req, res) => {
  const movie_id = String(req.params.movie_id)
  pool.query("SELECT * FROM movies_critics WHERE movie_id = $1 AND content IS NOT NULL", [movie_id], (error, results) => {
    if (error) {
      throw error
    }
    res.status(200).json(results.rows)
  })
}

//해당 영화 네이버 일반 평론 가져오기
const getMovieCriticNaver = (req, res) => {
  const movie_id = String(req.params.movie_id)
  pool.query("SELECT * FROM movies_critics WHERE movie_id = $1 AND content IS NULL", [movie_id], (error, results) => {
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


const getMovieCertified = (req, res) => {

}

module.exports = {
  getCurrentMovie,
  getMovie,
  getPreMovie,
  getGenreMovie,
  getGenresMovie,
  getMovieTitle,
  getMovieDirector,
  getMovieCast,
  getMovieOrderScore,
  getMovieReportNaver,
  getMovieCriticNaver,
  getMovieCriticMeta, 
  getMovieCriticTomato,
}
//////////////////////////////////////////////////////////////////////////