/*
1:
	Skrifið stored procedure: StudentListJSon() sem notar cursor til að breyta vensluðum gögnum í JSon string.
	JSon-formuð gögnin eru listi af objectum.
	OBS: StudentListJSon skilar texta sem þið hafið formað.

	Niðurstöðurnar ættu að líta einhvern vegin svona út:

	[
		  {"first_name": "Guðrún", "last_name": "Ólafsdóttir", "date_of_birth": "1999-03-31"},
		  {"first_name": "Andri Freyr", "last_name": "Kjartansson", "date_of_birth": "2000-11-01"},
		  {"first_name": "Tinna Líf", "last_name": "Björnsson", "date_of_birth": "1998-08-14"},
		  {"first_name": "Magni Þór", "last_name": "Sigurðsson", "date_of_birth": "2000-05-27"},
		  {"first_name": "Rheza Már", "last_name": "Hamid-Davíðs", "date_of_birth": "2001-09-17"},
		  {"first_name": "Hadría Gná", "last_name": "Schmidt", "date_of_birth": "1999-07-29"},
		  {"first_name": "Jasmín Rós", "last_name": "Stefánsdóttir", "date_of_birth": "1996-02-29"}
	]
*/
delimiter $$
drop procedure if exists StudentListJSon $$

create procedure StudentListJSon()
begin
	select concat(
    '[',
    group_concat(json_object('f_name', firstName, 'l_name', lastName, 'date_of_birth', dob)),
    ']'
    ) as tes
    from students;
end $$
delimiter ;

call StudentListJSon();

/*
	2:
	Skrifið nú SingleStudentJSon()þannig að nemandinn innihaldi nú lista af þeim áföngum sem hann hefur tekið.
	Śé nemandinn enn við nám þá koma þeir áfangar líka með.
	ATH: setjið nemandann sem object.
	Líkleg niðurstaða:

	{
		"student_id": "1",
		"first_name": "Guðrún",
		"last_name": "Ólafsdóttir",
		"date_of_birth": "1999-03-31",
		"courses" :[
		  {"course_number": "STÆ103","course_credits": "5","status": "pass"},
		  {"course_number": "EÐL103","course_credits": "5","status": "pass"},
		  {"course_number": "STÆ203","course_credits": "5","status": "pass"},
		  {"course_number": "EÐL203","course_credits": "5","status": "pass"},
		  {"course_number": "STÆ303","course_credits": "5","status": "pass"},
		  {"course_number": "GSF2A3U","course_credits": "5","status": "pass"},
		  {"course_number": "FOR3G3U","course_credits": "5","status": "pass"},
		  {"course_number": "GSF2B3U","course_credits": "5","status": "pass"},
		  {"course_number": "GSF3B3U","course_credits": "5","status": "fail"},
		  {"course_number": "FOR3D3U","course_credits": "5","status": "fail"}
		]
	}
*/

-- án cursor
delimiter $$
drop procedure if exists SingleStudentJSon $$

create procedure SingleStudentJSon(student_id int(11))
begin
	select json_object('s_id', r.studentID, 'f_name', s.firstName, 'l_name', s.lastName, 'date_of_b', s.dob, 'course_list', concat(
    '[',
    group_concat(json_object('c_number', c.courseNumber, 'c_credits', c.courseCredits, 'course_status', r.passed)),
    ']'
    ) )
    from registration r
    inner join students s on r.studentID = s.studentID
    inner join courses c on r.courseNumber = c.courseNumber
    where s.studentID = student_id;
end $$
delimiter ;

-- með cursor
delimiter $$
drop procedure if exists SingleStudentJSon $$

create procedure SingleStudentJSON(student_id int(11))
begin
	declare student_json text;
	DECLARE done INT DEFAULT FALSE;
	DECLARE sid int(11);
	DECLARE f_name, l_name varchar(55);
    declare date_of_b date;
    declare courses longtext;
    
	DECLARE s_info CURSOR FOR select r.studentID, s.firstName, s.lastName, s.dob, 
							group_concat(json_object('c_number', c.courseNumber, 'c_credits', c.courseCredits, 'course_status', r.passed))
    from registration r
    inner join students s on r.studentID = s.studentID
    inner join courses c on r.courseNumber = c.courseNumber
    where s.studentID = student_id;
    
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
    set student_json = '';
    
	OPEN s_info;
	
	read_loop: LOOP
		FETCH s_info INTO sid, f_name, l_name, date_of_b, courses;
		IF done THEN
			LEAVE read_loop;
		END IF;
        set student_json = (select json_object('s_id', sid, 'f_name', f_name, 'l_name', l_name, 'date_of_b', date_of_b, 'course_list', concat('[', courses, ']')));
	END LOOP;

  CLOSE s_info;
  
  select student_json;
end $$
delimiter ;

call SingleStudentJSon(1);


/*
	3:
	Skrifið stored procedure: SemesterInfoJSon() sem birtir uplýsingar um ákveðið semester.
	Semestrið inniheldur lista af nemendum sem eru /hafa verið á þessu semestri.
	Og að sjálfsögðu eru gögnin á JSon formi!

	Gæti litið út einhvern veginn svona(hérna var semesterID 8 notað á original gögnin:
	[
		{"student_id": "1", "first_name": "Guðrún", "last_name": "Ólafsdóttir", "courses_taken": "2"},
		{"student_id": "2", "first_name": "Andri Freyr", "last_name": "Kjartansson", "courses_taken": "1"},
		{"student_id": "5", "first_name": "Rheza Már", "last_name": "Hamid-Davíðs", "courses_taken": "2"},
		{"student_id": "6", "first_name": "Hadríra Gná", "last_name": "Schmidt", "courses_taken": "2"}
	]
*/

-- án cursor
delimiter $$
drop procedure if exists SemesterInfoJSon $$

create procedure SemesterInfoJSon(semester_id int(11))
begin
	select concat(
    '[', 
	group_concat(
			distinct(
				json_object(
				's_id', r.studentID, 'f_name', s.firstName, 'l_name', s.lastName, 'courses_taken', (select count(*) from registration where passed = 1 and semesterID = semester_id and studentid = s.studentid)
				)
			) 
		),
	']'
	) as test
	from registration r
    inner join students s on r.studentID = s.studentID
    where r.semesterID = semester_id;
end $$
delimiter ;

-- með cursor
delimiter $$
drop procedure if exists SemesterInfoJSon $$

create procedure SemesterInfoJSon(semester_id int(11))
begin
	declare student_json text;
	DECLARE done INT DEFAULT FALSE;
	DECLARE sid int(11);
	DECLARE f_name, l_name varchar(55);
    declare c_taken int;
    
	DECLARE s_info CURSOR FOR select distinct(r.studentID), s.firstName, s.lastName, (select count(*) from registration where passed = 1 and semesterID = semester_id and studentid = s.studentid)
    from registration r
    inner join students s on r.studentID = s.studentID
    where r.semesterID = semester_id;
    
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
    set student_json = '[';
    
	OPEN s_info;
	
	read_loop: LOOP
		FETCH s_info INTO sid, f_name, l_name, c_taken;
		IF done THEN
			LEAVE read_loop;
		END IF;
        set student_json = concat(student_json, json_object('s_id', sid, 'f_name', f_name, 'l_name', l_name, 'courses_taken', c_taken), ',');
	END LOOP;
    set student_json = concat(trim(trailing ',' from student_json), ']');

  CLOSE s_info;
  
  select student_json;
end $$
delimiter ;

call SemesterInfoJSon(8);

-- ACHTUNG:  2 og 3 nota líka cursor!