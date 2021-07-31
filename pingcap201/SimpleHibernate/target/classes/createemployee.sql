create database employeedb;
use employeedb;

create table EMPLOYEE (
   id INT NOT NULL auto_increment,
   first_name VARCHAR(20) default NULL,
   last_name  VARCHAR(20) default NULL,
   level    INT  default NULL,
   PRIMARY KEY (id)
);
