CREATE TABLE users (
  userid int(11) NOT NULL AUTO_INCREMENT,
  username varchar(45) NOT NULL,
  password varchar(45) NOT NULL,
  PRIMARY KEY (userid),
  UNIQUE KEY username_UNIQUE (username)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

CREATE TABLE movieinfo (
  movieid int(11) NOT NULL AUTO_INCREMENT,
  title varchar(255) DEFAULT NULL,
  releaseYear int(11) DEFAULT NULL,
  runtime int(11) DEFAULT NULL,
  genre varchar(255) DEFAULT NULL,
  PRIMARY KEY (movieid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE rated (
  userid int(11) NOT NULL,
  movieid int(11) NOT NULL,
  rating int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;