delimiter $$
drop procedure if exists UpdateStudent $$

create procedure UpdateStudent(student_id int(11), start_sem int(11))
begin
	update students
    set startSemester = start_sem
    where studentID = student_id;
    
end $$
delimiter ;

call UpdateStudent(1, 6);


delimiter $$
drop procedure if exists DeleteStudent $$

create procedure DeleteStudent(student_id int(11))
begin
	
    delete from registration where studentID = student_id;
	delete from students where studentID = student_id;

end $$
delimiter ;

call DeleteStudent(8);


delimiter $$
drop procedure if exists AddSchool $$

create procedure AddSchool(school_name varchar(75))
begin

	insert into schools(schoolName) 
    values (school_name);
    
end $$
delimiter ;

call AddSchool('test');


delimiter $$
drop procedure if exists SingleSchool $$

create procedure SingleSchool(school_id int(11))
begin
	select *
    from schools
    where schoolID = school_id;
end $$
delimiter ;

call SingleSchool(2);


delimiter $$
drop procedure if exists UpdateSchool $$

create procedure UpdateSchool(school_id int(11), school_name varchar(75))
begin
	update schools
    set schoolName = school_name
    where schoolID = school_id;
    
end $$
delimiter ;

call UpdateSchool(2, 'test 2');



delimiter $$
drop procedure if exists DeleteSchool $$

create procedure DeleteSchool(school_id int(11))
begin

	delete from schools where schoolID = school_id;

end $$
delimiter ;

call DeleteSchool(4);


insert into divisions(divisionName, schoolID) values('test', 4);

delete from divisions where schoolID = 3;

delete from schools where schoolID = 3;



