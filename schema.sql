CREATE TABLE users (
  userid int(11) NOT NULL AUTO_INCREMENT,
  username varchar(45) NOT NULL,
  password varchar(45) NOT NULL,
  PRIMARY KEY (userid),
  UNIQUE KEY username_UNIQUE (username)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*
CREATE TABLE movieinfo (
  movieid int(11) NOT NULL AUTO_INCREMENT,
  title varchar(255) DEFAULT NULL,
  releaseYear int(11) DEFAULT NULL,
  runtime int(11) DEFAULT NULL,
  genre varchar(255) DEFAULT NULL,
  PRIMARY KEY (movieid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
*/
CREATE TABLE rated (
  userid int(11) NOT NULL,
  movieid int(11) NOT NULL,
  rating int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE moviedata(
	movieid int(11) NOT NULL AUTO_INCREMENT,
    title varchar(255) DEFAULT NULL,
    releaseYear int(11) DEFAULT NULL,
    duration int(11) DEFAULT NULL,
    rating float(11) DEFAULT NULL,
    numRatings int(11) DEFAULT NULL,
    numWins int(11) DEFAULT NULL,
    genre varchar(255) DEFAULT NULL,
    numGenres int(11) DEFAULT NULL,
    actionMovie int(11) DEFAULT NULL,
    adult int(11) DEFAULT NULL,
    adventure int(11) DEFAULT NULL,
    animation int(11) DEFAULT NULL,
    biography int(11) DEFAULT NULL,
    comedy int(11) DEFAULT NULL,
    crime int(11) DEFAULT NULL,
    documentary int(11) DEFAULT NULL,
    drama int(11) DEFAULT NULL,
    family int(11) DEFAULT NULL,
    fantasy int(11) DEFAULT NULL,
    filmNoir int(11) DEFAULT NULL,
    history int(11) DEFAULT NULL,
    horror int(11) DEFAULT NULL,
    mystery int(11) DEFAULT NULL,
    romance int(11) DEFAULT NULL,
    SciFi int(11) DEFAULT NULL,
    short int(11) DEFAULT NULL,
    sport int(11) DEFAULT NULL,
    thriller int(11) DEFAULT NULL,
    war int(11) DEFAULT NULL,
    western int(11) DEFAULT NULL,
    PRIMARY KEY (movieid)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;
