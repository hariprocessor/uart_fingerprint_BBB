use fingerprint
drop table user;
create table user (
       uid int not null primary key,
       name varchar(15),
       phone varchar(15),
       stamp int
);
