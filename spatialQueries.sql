-- query to update attribute based on spatial join 
update oppSites set old_zoning = existing.zoning from 
(
select oppSites.id as id , zoning_existing.sym_code as zoning from zoning_existing, oppSites where st_within(st_centroid(oppSites.geom), zoning_existing.geom)
) existing
where existing.id = oppSites.id;



-- query that joins 3 tables on transport code BTS
select tz_nsw_2011.geom, tz_nsw_2011.tz_code11::int, (pop.pop/st_area(tz_nsw_2011.geom)) as pop, (emp.emp/st_area(tz_nsw_2011.geom)) as emp from 
tz_nsw_2011 join 
(
select tz11, sum(emp) as emp from abts_employment_forecasts_dataset_2011_2041 where year = 2011 group by tz11
) as emp
on tz_nsw_2011.tz_code11 = emp.tz11 join
(
select tz11, sum(erp) as pop from abts_population_forecasts_erp_opd_2011_2041 where year = 2011 group by tz11
) as pop
on tz_nsw_2011.tz_code11 = pop.tz11