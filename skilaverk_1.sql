-- 1:
-- Birtið lista af öllum áföngum sem geymdir eru í gagnagrunninum.
-- Áfangarnir eru birtir í stafrófsröð
delimiter $$
drop procedure if exists CourseList $$

create procedure CourseList()
begin
	select courseName
    from Courses;
end $$
delimiter ;

call CourseList();
-- 2:
-- Birtið upplýsingar um einn ákveðin áfanga.
delimiter $$
drop procedure if exists SingleCourse $$

create procedure SingleCourse(courseNumb char(10))
begin
	select *
    from Courses
    where courseNumber = courseNumb;
end $$
delimiter ;

call SingleCourse('STÆ603');
-- 3:
-- Nýskráið áfanga í gagnagrunninn.
-- Það þarf að skrá áfanganúmerið, áfangaheitið og einingafjöldann
delimiter $$
drop procedure if exists NewCourse $$

create procedure NewCourse(courseNumb char(10), courseNam varchar(75), courseCreds tinyint(4))
begin
	insert into Courses(CourseNumber, courseName, courseCredits)
    values (courseNumb, courseNam, courseCreds);
end $$
delimiter ;

call NewCourse('STÆ703', 'test', 5);

-- 4:
-- Uppfærið réttan kúrs.
-- row_count() fallið er hér notað til að birta fjölda raða sem voru uppfærðar.
delimiter $$
drop procedure if exists UpdateCourse $$

create procedure UpdateCourse(course_numb char(10), course_name varchar(75), course_creds tinyint(4))
begin
	update courses
    set courseName = course_name, courseCredits = course_creds
    where courseNumber = course_numb;
    
	select row_count() as 'Afangar uppfaerdir';
end $$
delimiter ;

call UpdateCourse('FOR3D3U', 'Alvoru leikjaforritun', '5')

-- 5:
-- ATH: Ef verið er að nota áfangann einhversstaðar(sé hann skráður á TrackCourses töfluna) þá má EKKI eyða honum.
-- Sé hins vegar hvergi verið að nota hann má eyða honum úr bæði Courses og Restrictor töflunum.
delimiter $$
drop procedure if exists DeleteCourse $$

create procedure DeleteCourse(courseNumb char(10))
begin
	if (select courseNumber from TrackCourses where courseNumber = courseNumb) then
    
		select 'afangi i notkun';
    
    else
		
        delete from Courses where courseNumber = courseNumb;
	
    end if;
        
end $$
delimiter ;

call DeleteCourse('STÆ703');

-- 6:
-- fallið skilar heildarfjölda allra áfanga í grunninum
delimiter $$
drop function if exists NumberOfCourses $$
    
create function NumberOfCourses()
returns int
begin
	declare fjoldi int;
    set fjoldi = 0;
    
	select count(*) into fjoldi
    from Courses;
    
    return fjoldi;
end $$
delimiter ;

select NumberOfCourses();

-- 7:
-- Fallið skilar heildar einingafjölda ákveðinnar námsleiðar(Track)
-- Senda þarf brautarNumer inn sem færibreytu
delimiter $$
drop function if exists TotalTrackCredits $$
    
create function TotalTrackCredits(brautarNumer int)
returns int
begin
	declare heildarEin int;
    set heildarEin = 0;
    
    select sum(courseCredits) into heildarEin
	from courses
	inner join trackcourses on (courses.courseNumber = trackcourses.courseNumber)
	where trackcourses.trackID = brautarNumer;
    
    return heildarEin;
end $$
delimiter ;

select TotalTrackCredits(9);

-- 8: 
-- Fallið skilar heildarfjölda áfanga sem eru í boði á ákveðinni námsleið
delimiter $$
drop function if exists TotalNumberOfTrackCourses $$
    
create function TotalNumberOfTrackCourses(brautarNumer int)
returns int
begin
	declare fjAfanga int;
    set fjAfanga = 0;
    
    select count(*) into fjAfanga
	from courses
	inner join trackcourses on (courses.courseNumber = trackcourses.courseNumber)
	where trackcourses.trackID = brautarNumer;
    
    return fjAfanga;
end $$
delimiter ;

select TotalNumberOfTrackCourses(9);

-- 9:
-- Fallið skilar true ef áfanginn finnst í töflunni TrackCourses
delimiter $$
drop function if exists CourseInUse $$
    
create function CourseInUse(brautarNumer int)
returns int
begin
	declare afangaCheck int;
    set afangaCheck = 0;
    
    select count(*) 
    into afangaCheck
    from trackcourses
    where trackid = brautarNumer;
    if afangaCheck = 0 then
    
		return 0;
	
    else
    
		return 1;
        
	end if;
    
end $$
delimiter ;

select CourseInUse(9);

-- 10:
-- Fallið skilar true ef +arið er hlaupár annars false
delimiter $$
drop function if exists IsLeapyear $$

create function IsLeapYear(ar int)
returns boolean
begin
	declare leapYear boolean;
    
    if (select mod(ar, 4) = 0) and (select mod(ar, 100) != 0) then
		set leapYear = True;
	elseif (select mod(ar, 400) = 0) then
		set leapYear = True;
	else
		set leapYear = False;
	end if;
    
    return leapYear;
end $$
delimiter ;

select IsLeapYear(1900);

-- 11:
-- Fallið reiknar út og skilar aldri ákveðins nemanda
delimiter $$
drop function if exists StudentAge $$
    
create function StudentAge(nemId int)
returns int
begin
	declare aldur int;
    
    select year(from_days(datediff(now(), dob)))
    into aldur
    from students
    where studentID = nemId;
    
    return aldur;
end $$
delimiter ;

select StudentAge(1);

-- 12:
-- Fallið skilar fjölda þeirra eininga sem nemandinn hefur tekið(lokið)
delimiter $$
drop function if exists StudentCredits $$
    
create function StudentCredits(nemId int)
returns int
begin
	declare fjEin int;
    set fjEin = 0;
    
    select sum(courses.courseCredits)
    into fjEin
	from registration
    inner join trackcourses on (registration.trackID = trackcourses.trackID)
	inner join courses on (courses.courseNumber = trackcourses.courseNumber)
	where trackcourses.trackID = registration.trackID and registration.passed = 1 and registration.studentId = nemId
    group by courses.courseNumber
    limit 1;
    
    return fjEin;
end $$
delimiter ;

select StudentCredits(2);

-- 13:
-- Hér þarf að skila Brautarheiti, heiti námsleiðar(Track) og fjölda áfanga
-- Aðeins á að birta upplýsingar yfir brautir sem hafa námsleiðir sem innihalda áfanga.
delimiter $$
drop procedure if exists TrackTotalCredits $$

create procedure TrackTotalCredits()
begin
	select trackName, sum(courses.courseCredits)
    from tracks
    inner join trackcourses on (tracks.trackID = trackcourses.trackID)
    inner join courses on (trackcourses.courseNumber = courses.courseNumber)
    group by trackName;
end $$
delimiter ;

call TrackTotalCredits();

-- 14:
-- Hér þarf skila lista af öllum áföngum ásamt restrictorum og tegund þeirra.
-- Hafi áfangi enga undanfara eða samfara þá birtast þeir samt í listanum.
delimiter $$
drop procedure if exists CourseRestrictorList $$

create procedure CourseRestrictorList()
begin
	select *, restrictors.courseNumber as restrictor, restrictors.restrictorType as restrType 
    from courses
	left outer join restrictors
    on (courses.courseNumber = restrictors.courseNumber);
end $$
delimiter ;

call courseRestrictorList();

-- 15:
-- RestrictorList birtir upplýsingar um alla restrictora ásamt áföngum.
-- Með öðrum orðum: Gemmér alla restrictora(undanfara, samfara) og þá áfanga sem þeir hafa áhrif á.
delimiter $$
drop procedure if exists RestrictorList $$

create procedure RestrictorList()
begin
    select restrictorID as 'undanfari/samfari', group_concat(courseNumber) as 'hefur ahrif a'
    from restrictors
    group by restrictorID;
end $$
delimiter ;

call RestrictorList();