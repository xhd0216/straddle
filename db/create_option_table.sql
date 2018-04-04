create table if not exists test_options(
  underlying VARCHAR(10) not null,
  strike float,
  expiration date,
  price float,
  bid float,
  ask float,
  last float,
  open_int int,
  query_time datetime,
  is_call BOOLEAN not null default 0,
  constraint symb_stri_exp_query primary key (underlying, strike, expiration, query_time, is_call));
