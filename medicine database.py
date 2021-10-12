insert into medicine_det values('crosin',50,10);
insert into medicine_det values('ceplanin',50,65);
insert into medicine_det values('ovral-G',50,176);
insert into medicine_det values('Ranitidine',50,24);
insert into medicine_det values('Disprin',50,11);
insert into medicine_det values('Flagyl',50,13);
insert into medicine_det values('digine',50,17);
insert into medicine_det values('ciplox',50,22);


create table medicine_det(
Mname varchar(45) PRIMARY KEY,
Mquantity tinyint unsigned,
Mprice decimal(5,2)
);

