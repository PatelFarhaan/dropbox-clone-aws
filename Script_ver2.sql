use master
GO
if exists (select * from master.sys.databases where name = 'ats')
  drop database ats
GO
create database ats
GO
use ats
GO

create table department
	(deptid				varchar(5),
	 name				varchar(20),
	 primary key (deptid)
	);
	
create table applicant
	(app_id			varchar(8), 
	psw				varchar(15) not null,
	emailid			varchar(20) not null,
	name			varchar(20) not null,
	gender			varchar(10)
		check (gender in ('Female', 'Male', 'Unknown')),
	birth_dt		date,
	status			varchar(10)
		check (status in ('Active', 'Inactive')),      
	 primary key (app_id)
	);

create table resume
	(res_id			varchar(8), 
	 resume			varchar(250), 
	 app_id		    varchar(8),
	 primary key (res_id),
	 foreign key (app_id) references applicant(app_id)
	);
	
create table employee
	(emplid			varchar(8), 
	 name			varchar(20) not null, 
	 hire_dt		date,
	 status			varchar(10) not null
	 	check (status in ('Active', 'Inactive')),
	 salary			numeric(8,2) check (salary > 29000),
	 email			varchar(20),
	 deptid			varchar(5), 	 
	 primary key (emplid),
	 foreign key (deptid) references department(deptid)
		on delete set null
	);

create table user_ats
	(userid			varchar(8), 
	 psw			varchar(15) not null, 
	 type			varchar(20)
	 	check (type in ('Hiring Manager', 'Recruiter', 'Administrator')),
	 emplid			varchar(8),
	 deptid			varchar(5),
	 primary key (userid),
	 foreign key (deptid) references department(deptid)
		on delete set null,
	 foreign key (emplid) references employee(emplid)
		on delete set null
	);

create table job
	(jobid			varchar(8), 
	 open_dt		date,
	 status			varchar(8)
	 	check (status in ('Open', 'Closed', 'Cancelled')), 
	 title			varchar(30),
	 salary_min		numeric(8,2) check (salary_min > 29000),
	 salary_max		numeric(8,2) check (salary_max < 1000000),
	 descr			varchar(100),
	 location		varchar(50),
	 visibility		varchar(1)
	 	check (visibility in ('Y', 'N')),
	 deptid			varchar(5),
	 primary key (jobid),
	 foreign key (deptid) references department(deptid)
		on delete set null
	);

create table application
	(appl_id		varchar(8), 
	 appl_dt		date,
	 status			varchar(15)
	 	check (status in ('Applied', 'Reviewed', 'Reject', 'Interview', 'Offer', 'Hired')),
	 app_id			varchar(8),
	 jobid			varchar(8),
	 primary key (appl_id),
	 foreign key (app_id) references applicant(app_id)
		on delete set null,
	 foreign key (jobid) references job(jobid)
		on delete set null
	);

create table interview
	(int_id			varchar(8), 
	 int_dt			date,
	 status			varchar(20)
	 	check (status in ('Pending', 'Recommend for offer', 'Reject')),
	 comments		varchar(200),
	 appl_id		varchar(8),
	 primary key (int_id),
	 foreign key (appl_id) references application(appl_id)
		on delete set null
	);
	
	create table offer
	(ofr_id			varchar(8),
	 ofr_dt			date,
	 status			varchar(15)
	 	check (status in ('Submitted', 'Accepted', 'Rejected')), 
	 salary			numeric(8,2) check (salary > 29000),
	 start_dt		date,
	 int_id			varchar(8),
	 emplid			varchar(8),
	 primary key (ofr_id),
	 foreign key (int_id) references interview(int_id)
		on delete set null,
	 foreign key (emplid) references employee(emplid)
		on delete set null
	);

GO

delete from department;
delete from applicant;
delete from resume;
delete from employee;
delete from user_ats;
delete from job;
delete from application;
delete from interview;
delete from offer;

insert into department values ('1', 'Engineering');
insert into department values ('2', 'Finance');
insert into department values ('3', 'HR');
insert into department values ('4', 'Marketing');

insert into applicant values ('1', 'encrypted1', 'marianne@gmail.com', 'Marianne Paulson', 'Female', '1984-03-03', 'Active');
insert into applicant values ('2', 'encrypted2', 'mikey@gmail.com', 'Mikey Paulson', 'Male', '2001-12-21', 'Active');
insert into applicant values ('3', 'encrypted3', 'nicholas@gmail.com', 'Nicholas Paulson', 'Male', '1996-06-01', 'Active');
insert into applicant values ('4', 'encrypted4', 'thomas@gmail.com', 'Thomas Paulson', 'Male', '1997-04-07', 'Active');
insert into applicant values ('5', 'encrypted5', 'jim@gmail.com', 'Jim Paulson', 'Male', '1966-10-31', 'Active');

insert into resume values ('1', 'resume1', '1');
insert into resume values ('2', 'resume2', '1');
insert into resume values ('3', 'resume1', '2');

insert into employee values ('1', 'John Kennedy', '2019-03-13', 'Active', '100000', 'Kennedy@gmail.com', '1');
insert into employee values ('2', 'Mary Jones', '2018-03-01', 'Active', '85000', 'Mary@gmail.com', '2');
insert into employee values ('3', 'Hans Iverson', '2017-04-15', 'Active', '100000', 'Hans@gmail.com', '3');

insert into user_ats values ('1', 'Encrypted1', 'Hiring Manager', '1', '1');
insert into user_ats values ('2', 'Encrypted2', 'Recruiter', '2', '2');
insert into user_ats values ('3', 'Encrypted3', 'Administrator', '3', '3');

insert into job values ('1', '2019-09-15', 'Open', 'Software Engineer', '50000', '10000', 'Design and write code', 'San Francisco', 'Y', '1');
insert into job values ('2', '2019-09-18', 'Open', 'Java Programmer', '40000', '90000', 'Write Java Code', 'San Francisco', 'Y', '1');

insert into application values ('1', '2019-09-22', 'Interview', '1', '1');
insert into application values ('2', '2019-09-23', 'Applied', '2', '1');
insert into application values ('3', '2019-09-24', 'Applied', '3', '1');
insert into application values ('4', '2019-09-22', 'Applied', '4', '2');
insert into application values ('5', '2019-09-23', 'Offer', '5', '2');

insert into interview values ('1', '2019-09-24', 'Pending', null, '1');
insert into interview values ('2', '2019-09-25', 'Recommend for offer', 'Exceeds all requirements', '5');

insert into offer values ('1', '2019-09-25', 'Accepted', '90000', '2019-10-07', '2', null);

select * from applicant