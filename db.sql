drop table Tweet;
drop table Mention;
drop table Response;
drop table TweetResponse;

create table Tweet
(
    tweet_id varchar(100)      not null,
    text     text              not null,
    link     text default null null,
    constraint Tweet_pk
        primary key (tweet_id)
);

create unique index Tweet_tweet_id_uindex
    on Tweet (tweet_id);

create table Mention
(
    id         int auto_increment,
    mention_id varchar(100)                        not null,
    since_id   varchar(100)                        null,
    checked_at timestamp default current_timestamp null,
    constraint Mention_pk
        primary key (id)
);

create unique index Mention_id_uindex
    on Mention (id);

create table Response
(
    response_id int auto_increment,
    text        text null,
    constraint Response_pk
        primary key (response_id)
);

create table TweetResponse
(
    tweet_response_id int auto_increment,
    tweet_id          varchar(100) not null,
    response_id       int          null,
    constraint TweetResponse_pk
        primary key (tweet_response_id),
    foreign key (tweet_id) references Tweet (tweet_id),
    foreign key (response_id) references Response (response_id)
);
