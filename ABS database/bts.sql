create table landuse_16 as select * from (select c.*,d.spd_2016,d.opd_2016 from 
(select a.*,b.erp_2016 from (select tz_code11, sum(year_2016) as emp_2016 from alu16_2011_2056_emp_forat group by tz_code11) as a
join (select tz_code11, sum(year_2016) as erp_2016 from alu16_2011_2056_erp_forat group by tz_code11) as b on a.tz_code11 = b.tz_code11) as c join 
(select tz_code11, sum(spd_2016) as spd_2016, sum(opd_2016) as opd_2016 from aopd_spd_tz11_forat group by tz_code11) as d on c.tz_code11 = d.tz_code11) as e