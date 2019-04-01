/* 1:
	Smíðið trigger fyrir insert into Restrictors skipunina. 
	Triggernum er ætlað að koma í veg fyrir að einhver áfangi sé undanfari eða samfari síns sjálfs. 
	með öðrum orðum séu courseNumber og restrictorID með sama innihald þá stoppar triggerinn þetta með
	því að kasta villu og birta villuboð.
	Dæmi um insert sem triggerinn á að stoppa: insert into Restrictors values('GSF2B3U','GSF2B3U',1);
*/
delimiter $$
drop trigger if exists check_restrictor_id $$

create trigger check_restrictor_id
before insert on restrictors
for each row
begin
     declare msg varchar(255);
	 -- tímagildin úr insert skipuninni skoðuð
     if (new.restrictorID <= new.courseNumber) then
			-- Villuskilaboðin undirbúin og sett í breytuna msg
            set msg = 'restrictorID ma ekki vera sa sami og CourseNumber';
			-- Villu er kastað og villuskilaboðin birt
            signal sqlstate '45000' set message_text = msg;
     end if;
end $$
delimiter ;

insert into Restrictors values('GSF2B3U','GSF2B3U',1);

-- 2:
-- Skrifið samskonar trigger fyrir update Restrictors skipunina.
delimiter $$
drop trigger if exists check_update_restrictor_id $$

create trigger check_update_restrictor_id
before update on restrictors
for each row
begin
     declare msg varchar(255);
	 -- tímagildin úr insert skipuninni skoðuð
     if (new.restrictorID <= new.courseNumber) then
			-- Villuskilaboðin undirbúin og sett í breytuna msg
            set msg = 'restrictorID ma ekki vera sa sami og CourseNumber';
			-- Villu er kastað og villuskilaboðin birt
            signal sqlstate '45000' set message_text = msg;
     end if;
end $$
delimiter ;

/*
	3:
	Skrifið stored procedure sem leggur saman allar einingar sem nemandinn hefur lokið.
    Birta skal fullt nafn nemanda, heiti námsbrautar og fjölda lokinna eininga(
	Aðeins skal velja staðinn áfanga. passed = true
*/
delimiter $$
drop procedure if exists studentCreds $$

create procedure studentCreds(stud_id int(11))
begin
	select concat(students.firstName, ' ', students.lastName) as fullName, tracks.trackName as 'namsbraut' ,sum(courses.courseCredits) as 'fjoldi lokinna eininga'
	from registration
    inner join trackcourses on (registration.trackID = trackcourses.trackID)
	inner join courses on (courses.courseNumber = trackcourses.courseNumber)
    inner join students on (registration.studentID = students.studentID)
    inner join tracks on (tracks.trackId = trackcourses.trackID)
	where trackcourses.trackID = registration.trackID and registration.passed = 1 and registration.studentId = stud_id
    group by courses.courseNumber
    limit 1;
end $$
delimiter ;

call studentCreds(2);
/*
	4:
	Skrifið 3 stored procedure-a:
    AddStudent()
    AddMandatoryCourses()
    Hugmyndin er að þegar AddStudent hefur insertað í Students töfluna þá kallar hann á AddMandatoryCourses() sem skráir alla
    skylduáfanga á nemandann.
    Að endingu skrifið þið stored procedure-inn StudentRegistration() sem nota skal við sjálfstæða skráningu áfanga nemandans.
*/
delimiter $$
drop procedure if exists AddStudent $$

create procedure AddStudent(f_name varchar(55), l_name varchar(55), date_ob date, start_semester int(11))
begin
	declare stud_id int(11);

	insert into Students(firstName,lastName,dob,startSemester) 
    values (f_name,l_name,date_ob,start_semester);
    
    select studentID 
    into stud_id
    from Students
    where firstName = f_name and lastName = l_name and dob = date_ob and startSemester = start_semester;
    
    call AddMandatoryCourses(stud_id, start_semester);
end $$
delimiter ;

call AddStudent('fyrstnafn', 'eftirnafn', '1999-01-01', 9);

delimiter $$
drop procedure if exists AddMandatoryCourses $$

create procedure AddMandatoryCourses(stud_id int(11), start_semester int(11))
begin
	insert into Registration(studentID,trackID,courseNumber,registrationDate,passed,semesterID)
    values	(stud_id,9,'STÆ103',curdate(),false,start_semester),
			(stud_id,9,'EÐL103',curdate(),false,start_semester),
			(stud_id,9,'STÆ203',curdate(),false,start_semester+1),
			(stud_id,9,'EÐL203',curdate(),false,start_semester+1),
			(stud_id,9,'STÆ303',curdate(),false,start_semester+2),
			(stud_id,9,'GSF2A3U',curdate(),false,start_semester+3),
			(stud_id,9,'FOR3G3U',curdate(),false,start_semester+3),
			(stud_id,9,'GSF2B3U',curdate(),false,start_semester+4),
			(stud_id,9,'GSF3B3U',curdate(),false,start_semester+4),
			(stud_id,9,'FOR3D3U',curdate(),false,start_semester+4);
end $$
delimiter ;

delimiter $$
drop procedure if exists StudentRegistration $$

create procedure StudentRegistration(student_id int(11), course_number char(10), semester_id int(11))
begin
	declare track_id int(11);
    set track_id = 0;
    
	if exists(
	select restrictorID
    from Restrictors res
    inner join Registration reg
    on res.restrictorID = reg.courseNumber
    where res.courseNumber = course_number and reg.passed = 1 and reg.studentID = student_id)
    then
    
    select trackID
    into track_id
    from trackcourses
    where courseNumber = course_number;
    
    insert into Registration(studentID,trackID,courseNumber,registrationDate,passed,semesterID)
    values
    (student_id,track_id,course_number,curdate(),false,semester_id);
    
    end if;
end $$
delimiter ;

call StudentRegistration(7, 'STÆ403', 5);